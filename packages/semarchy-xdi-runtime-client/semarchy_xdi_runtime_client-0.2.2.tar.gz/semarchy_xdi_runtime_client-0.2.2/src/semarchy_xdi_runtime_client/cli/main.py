"""This module use click to create a CLI wrapper around the client."""

import click
from semarchy_xdi_runtime_client.client.client import XDIApiClient


@click.group()
@click.option("--runtime-url", help="The URL of the XDI runtime to use", type=str)
@click.option(
    "--disable-ssl-verify",
    help="Disable SSL cert verification",
    is_flag=True,
    default=False,
)
@click.pass_context
def cli(ctx: click.core.Context, runtime_url: str, disable_ssl_verify: bool):
    """The main CLI entrypoint and base command

    Args:
        ctx (click.core.Context): Click context
        runtime_url (str): runtime url
        disable_ssl_verify (bool): disable ssl verification when requesting the runtime API
    """
    ctx.ensure_object(dict)
    ctx.obj["runtime_url"] = runtime_url
    ctx.obj["disable_ssl_verify"] = disable_ssl_verify


@cli.command()
@click.argument("job-name", required=True)
@click.argument("job-vars", required=True)
@click.pass_context
def launch_delivery(ctx: click.core.Context, job_name: str, job_vars: str):
    """Subcommand to launch a delivery job

    Args:
        ctx (click.core.Context): Click context
        job_name (str): The XDI job name to launch
        job_vars (str): The variable to pass to the job
    """
    client = XDIApiClient(
        runtime_host=ctx.obj.get("runtime_url"),
        verify_host=(not ctx.obj.get("disable_ssl_verify")),
    )
    client.launch_delivery(job_name=job_name, job_vars=job_vars)
