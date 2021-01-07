from typing import Optional
from typing import Protocol

import base64

import boto3
import click

from perkeepy.blob import Blob
from perkeepy.blob import Ref
from perkeepy.blobserver.s3 import S3
from perkeepy.blobserver.s3 import S3Client
from perkeepy.schema import CamliType
from perkeepy.schema import Schema


@click.group()
@click.option("--bucket", type=str, required=True)
@click.pass_context
def cli(ctx: click.Context, *, bucket: str) -> None:
    s3_client: S3Client = boto3.client("s3")
    blobserver = S3(s3_client=s3_client, bucket=bucket)
    ctx.obj = blobserver


@cli.command("list")
@click.option("--only-schemas", is_flag=True)
@click.option("--schema-type", type=str)
@click.pass_obj
def list_(
    blobserver: S3, *, only_schemas: bool, schema_type: Optional[str]
) -> None:
    only_schemas = only_schemas or schema_type is not None
    camli_type: Optional[CamliType] = None
    if only_schemas:
        camli_type = CamliType(schema_type)

    for ref in blobserver.enumerate_blobs():

        if only_schemas:
            blob: Blob = blobserver.fetch(ref)
            try:
                schema: Schema = Schema.from_blob(blob)
            except Exception:
                continue

            if camli_type is not None and schema.get_type() != camli_type:
                continue

        click.echo(ref.to_str())


@cli.command("get")
@click.option("--ref", type=str, required=True)
@click.pass_obj
def get(blobserver: S3, *, ref: str) -> None:
    ref_: Ref = Ref.from_ref_str(ref)
    blob = blobserver.fetch(ref_)

    if blob.is_utf8():
        click.echo(blob.get_bytes().decode("utf-8"))
    else:
        click.echo(base64.b64encode(blob.get_bytes()))


if __name__ == "__main__":
    cli()
