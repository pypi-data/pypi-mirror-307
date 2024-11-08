import json
import sys
from csv import DictReader, DictWriter, writer
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, field_validator
from rich import print, print_json
from rich.progress import track
from rich.table import Table
from typer import Argument, Context, FileText, FileTextWrite, Option, Typer

from aesop.commands.common.enums.output_format import OutputFormat
from aesop.commands.common.exception_handler import exception_handler
from aesop.commands.common.options import OutputFormatOption
from aesop.commands.documents.utils import (
    Directory,
    attach_document_to_namespace,
    create_data_document,
    create_namespace,
    get_user_id,
)
from aesop.config import AesopConfig

app = Typer(help="Manages glossary documents.")


class Columns(BaseModel):
    name: str = Field(
        description="The name of the glossary term. Should be a non-empty string."
    )
    content: str = Field(
        description="The content for the glossary term. Should be a non-empty string."
    )
    hashtags_: Union[Optional[List[str]], str] = Field(
        default=None,
        alias="hashtags",
        description="The hashtags to append to the glossary term. Should be a list "
        "of strings, or null if there is no hashtag.",
    )

    @field_validator("hashtags_", mode="after")
    @classmethod
    def validate_optional_field(cls, value: Any) -> Optional[Any]:
        if isinstance(value, str):
            return None
        return value

    @property
    def hashtags(self) -> Optional[List[str]]:
        if isinstance(self.hashtags_, str):
            raise ValueError
        if not self.hashtags_:
            return None
        return self.hashtags_


@exception_handler("generate glossary template")
@app.command(help="Generates a template of glossary CSV file with some example values.")
def gen_template(
    file: FileTextWrite = Argument(
        default="biz_glossary.csv", help="The file to write to."
    )
) -> None:
    writer = DictWriter(file, [v.alias or k for k, v in Columns.model_fields.items()])
    writer.writeheader()
    writer.writerow(
        Columns(name="john.doe", content="some content").model_dump(by_alias=True)
    )
    writer.writerow(
        Columns(
            name="jane.doe", content="some other content", hashtags=["tag1", "tag2"]
        ).model_dump(by_alias=True)
    )
    print(f"Wrote template to {file.name}")


@exception_handler("print glossary schema")
@app.command(help="Prints the expected schema for a glossary CSV file.")
def schema(output: OutputFormat = OutputFormatOption) -> None:
    if output is OutputFormat.JSON:
        print_json(json.dumps(Columns.model_json_schema()))

    else:
        if output is OutputFormat.CSV:
            spamwriter = writer(sys.stdout)
            spamwriter.writerow(["Name", "Description"])
            for name, field in Columns.model_fields.items():
                spamwriter.writerow([field.alias or name, field.description])
        if output is OutputFormat.TABULAR:
            table = Table(
                "Name",
                "Description",
                show_lines=True,
            )
            for name, field in Columns.model_fields.items():
                table.add_row(field.alias or name, field.description)
            print(table)


@exception_handler("import glossary")
@app.command(
    help="Imports a local business glossary file to Metaphor's data document storage. "
    "To see the schema or a simple template file, use `schema` or `gen-template` "
    "subcommands.",
    name="import",
)
def import_(
    ctx: Context,
    input_file: FileText = Argument(
        help="The business glossary to import to Metaphor."
    ),
    author: Optional[str] = Option(
        help="Author of the glossary items. Can be either an email or a Metaphor ID. "
        "If unset, a user representing the API key in use will be the documents' "
        "author.",
        default=None,
    ),
    directory: str = Option(
        help="The directory to import the file to. Should be in the format of a "
        "single slash-separated string. Any nonexisting subdirectory will be created.",
        default="",
    ),
    publish: bool = Option(
        help="Whether to publish the imported file or not.", default=True
    ),
) -> None:
    """
    1. Looks for the user id representing the author.
    2. Creates the target namespace if it does not exist already.
    3. Creates the data document.
    4. Attaches the data document to the target namespace.
    """
    config: AesopConfig = ctx.obj
    client = config.get_graphql_client()
    user_id = get_user_id(client, author) if author else None
    namespace_id = create_namespace(client, Directory(dir=directory))

    columns = [
        Columns.model_validate(row) for row in DictReader(input_file.readlines())
    ]
    print(f"{len(columns)} documents to import.")
    document_ids: List[str] = []
    for column in track(columns, "Importing..."):
        document_id = create_data_document(
            client, column.name, column.content, column.hashtags, publish, user_id
        )
        document_ids.append(document_id)

    if not namespace_id:
        print(f"Created {len(document_ids)} files.")
    else:
        namespace_url = config.url / "documents" / "directories" / namespace_id
        print("Attaching documents to namespace")
        attach_document_to_namespace(client, namespace_id, document_ids)
        print(f"Created {len(document_ids)} files: {namespace_url.human_repr()}")
