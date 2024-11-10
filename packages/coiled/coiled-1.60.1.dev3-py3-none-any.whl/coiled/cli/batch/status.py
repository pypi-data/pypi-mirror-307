from typing import Optional

import click
from rich import print

import coiled
from coiled.cli.curl import sync_request

from ..cluster.utils import find_cluster
from ..utils import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
def batch_status(
    cluster: str,
    account: Optional[str],
):
    with coiled.Cloud(account=account) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        cluster_id = cluster_info["id"]

        url = f"{cloud.server}/api/v2/jobs/cluster/{cluster_id}"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="get",
            data=None,
            json_output=True,
        )

        print(response)
