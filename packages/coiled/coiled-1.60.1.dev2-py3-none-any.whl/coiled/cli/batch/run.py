import os
import re
import shlex

import click

from coiled.cli.curl import sync_request
from coiled.cli.run import dict_from_key_val_list

from ..utils import CONTEXT_SETTINGS, fix_path_for_upload

# Be fairly flexible in how we parse options in header, i.e., we allow:
# "#COILED"
# "# COILED"
# then ":" and/or " "
# then you can specify key as "key" or "--key"
# key/val pair as "key val" or "key=val"
# or just "key" if it's a flag
HEADER_REGEX = re.compile(r"^\s*(# ?COILED)[\s:-]+([\w_-]+)([ =](.+))?")


def parse_array_string(array):
    try:
        return [int(array)]
    except ValueError:
        ...

    if "," in array:
        result = []
        for a in array.split(","):
            result.extend(parse_array_string(a))
        return result

    array_range = array.split("-")
    if len(array_range) == 2:
        start, end = array_range
        skip = 1
        try:
            if len(end.split(":")) == 2:
                end, skip = end.split(":")
                skip = int(skip)
            start = int(start)
            end = int(end)
        except ValueError:
            ...
        else:
            # no value error so far
            if start > end:
                # can't have this inside the try or else it would be caught
                raise ValueError(
                    f"Unable to parse '{array}' as a valid array range, start {start} is greater than end {end}."
                )
            return list(range(start, end + 1, skip))

    raise ValueError(f"Unable to parse '{array}' as a valid array range. Valid formats are `n`, `n-m`, or `n-m:s`.")


def handle_possible_implicit_file(implicit_file):
    if os.path.exists(implicit_file) and os.path.isfile(implicit_file):
        with open(implicit_file) as f:
            file_content = f.read()

        remote_rel_dir, remote_base = fix_path_for_upload(local_path=implicit_file)

        return {
            "local_path": implicit_file,
            "path": f"{remote_rel_dir}{remote_base}",
            "remote_path": f"/scratch/{remote_rel_dir}{remote_base}",
            "content": file_content,
        }


def search_content_for_implicit_files(f: dict):
    content = f["content"]
    implicit_files = []
    for line in content.split("\n"):
        if "python" in line or ".sh" in line:
            line_parts = shlex.split(line.strip())
            for part in line_parts:
                implicit_file = handle_possible_implicit_file(part)
                if implicit_file:
                    # TODO handle path translation?
                    implicit_files.append(implicit_file)
    return implicit_files


def get_kwargs_from_header(f: dict, click_params: list):
    click_lookup = {}
    for param in click_params:
        for opt in param.opts:
            lookup_key = opt.lstrip("-")
            click_lookup[lookup_key] = param

    kwargs = {}
    content = f["content"]
    for line in content.split("\n"):
        match = re.fullmatch(HEADER_REGEX, line)
        if match:
            kwarg = match.group(2).lower()
            val = match.group(3)
            val = val.strip().strip('"') if val else val

            if kwarg not in click_lookup:
                raise ValueError(f"Error parsing header in {f['path']}:\n{line}\n  {kwarg} is not valid argument")

            param = click_lookup[kwarg]
            val = True if param.is_flag else param.type.convert(val, param=param, ctx=None)
            key = param.name

            if param.multiple:
                if key not in kwargs:
                    kwargs[key] = []
                kwargs[key].append(val)
            else:
                kwargs[key] = val
    return kwargs


@click.command(context_settings={**CONTEXT_SETTINGS, "ignore_unknown_options": True})
@click.pass_context
# general cluster options
@click.option("--workspace", default=None, type=str)
@click.option("--software", default=None, type=str)
@click.option("--env", "-e", default=[], multiple=True)
@click.option(
    "--container",
    default=None,
    help=(
        "Docker container in which to run the batch job tasks; "
        "this does not need to have Dask (or even Python), "
        "only what your task needs in order to run."
    ),
)
@click.option(
    "--vm-type",
    default=[],
    multiple=True,
    help="VM type to use. Specify multiple times to provide multiple options.",
)
@click.option("--cpu", default=None, type=int, help="Number of cores per VM.")
@click.option("--memory", default=None, type=str, help="Memory per VM.")
@click.option(
    "--gpu",
    default=False,
    is_flag=True,
    help="Have a GPU available.",
)
@click.option(
    "--region",
    default=None,
    help="The cloud provider region in which to run the notebook.",
)
@click.option(
    "--disk-size",
    default=None,
    help="Use larger-than-default disk on VM, specified in GiB.",
)
# batch specific options
@click.option("--ntasks", default=None, type=int)
@click.option("--array", default=None, type=str)
@click.option("--max-workers", "-N", default=None, type=click.IntRange(1))
@click.argument("command", nargs=-1)
def batch_run(ctx, **kwargs):
    """
    Submit a batch job to run on Coiled.

    Batch Jobs is currently an experimental feature.
    """

    command = kwargs["command"]

    # Handle command as string case (e.g. `coiled run "python myscript.py"`)
    if len(command) == 1:
        command = shlex.split(command[0])
    # if user tries `coiled run foo.py` they probably want to run `python foo.py` rather than `foo.py`
    if len(command) == 1 and command[0].endswith(".py"):
        command = ["python", command[0]]

    # unescape escaped COILED env vars in command
    command = [part.replace("\\$COILED", "$COILED") for part in command]

    user_files = []
    kwargs_from_header = None

    # identify implicit files referenced in commands like "python foo.py" or "foo.sh"
    for idx, implicit_file in enumerate(command):
        f = handle_possible_implicit_file(implicit_file)
        if f:
            user_files.append(f)
            command[idx] = f["path"]
            # just get kwargs (if any) from the first file that has some in the header
            kwargs_from_header = kwargs_from_header or get_kwargs_from_header(f, ctx.command.params)

    # merge options from file header with options specified on command line
    # command line takes precedence
    if kwargs_from_header:
        for key, val in kwargs_from_header.items():
            # only use the option from header if command line opt was "default" (i.e., not specified by user)
            if ctx.get_parameter_source(key) == click.core.ParameterSource.DEFAULT:
                kwargs[key] = val
            elif isinstance(val, list) and isinstance(kwargs[key], (list, tuple)):
                kwargs[key] = [*kwargs[key], *val]

    # extra parsing/validation of options
    if kwargs["ntasks"] is not None and kwargs["array"] is not None:
        raise ValueError("You cannot specify both `--ntasks` and `--array`")

    if kwargs["ntasks"]:
        job_array_ids = list(range(kwargs["ntasks"]))
    elif kwargs["array"]:
        job_array_ids = parse_array_string(kwargs["array"])
    else:
        job_array_ids = [0]

    job_env_vars = dict_from_key_val_list(kwargs["env"])

    # identify implicit files referenced by other files
    # for example, user runs "coiled batch run foo.sh" and `foo.sh` itself runs `python foo.py`
    user_files_from_content = []
    for f in user_files:
        if "python " in f["content"] or ".sh" in f["content"]:
            more_files = search_content_for_implicit_files(f)
            if more_files:
                user_files_from_content.extend(more_files)
    if user_files_from_content:
        user_files.extend(user_files_from_content)

    max_workers = kwargs["max_workers"]
    n_task_workers = len(job_array_ids) if max_workers is None else min(len(job_array_ids), max_workers)
    print(f"Running job array of {len(job_array_ids)} tasks on {n_task_workers} VMs...")

    cluster_kwargs = {
        "workspace": kwargs["workspace"],
        "n_workers": n_task_workers,
        "software": kwargs["software"],
        # batch job can either run in normal Coiled software env (which defaults to package sync)
        # or can run in an extra container (which doesn't need to include dask)
        "batch_job_container": kwargs["container"],
        # if batch job is running in extra container, then we just need a pretty minimal dask container
        # so for now switch the default in that case to basic dask container
        # TODO would it be better to use a pre-built senv with our `cloud-env-run` container instead?
        "container": "daskdev/dask:latest" if kwargs["container"] and not kwargs["software"] else None,
        "region": kwargs["region"],
        "scheduler_options": {"idle_timeout": "520 weeks"},  # TODO allow job timeout?
        # use default scheduler VM type since we aren't running tasks on scheduler
        # "scheduler_vm_types": list(kwargs["vm_type"]) if kwargs["vm_type"] else None,
        # "scheduler_cpu": kwargs["cpu"],
        # "scheduler_memory": kwargs["memory"],
        # "scheduler_disk_size": kwargs["disk_size"],
        # "scheduler_gpu": kwargs["gpu"],
        "worker_vm_types": list(kwargs["vm_type"]) if kwargs["vm_type"] else None,
        "worker_cpu": kwargs["cpu"],
        "worker_memory": kwargs["memory"],
        "worker_disk_size": kwargs["disk_size"],
        # "tags": {**tags, **{"coiled-cluster-type": cluster_type_tag}},
        # "mount_bucket": mount_bucket,
    }

    import coiled

    with coiled.Cloud(workspace=kwargs["workspace"]) as cloud:
        # Create a job
        job_spec = {
            "user_command": shlex.join(command),
            "user_files": user_files,
            "workspace": cloud.default_workspace,
            "task_array": job_array_ids,
            "env_vars": job_env_vars,
        }

        url = f"{cloud.server}/api/v2/jobs/"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="post",
            data=job_spec,
            json=True,
            json_output=True,
        )

        job_id = response["id"]

        # Run the job on a cluster
        cluster = coiled.Cluster(
            cloud=cloud,
            batch_job_ids=[job_id],
            allow_ssh=True,
            **cluster_kwargs,
        )

    status_command = f"coiled batch status {cluster.cluster_id}"
    if kwargs.get("workspace"):
        status_command = f"{status_command} --workspace {kwargs['workspace']}"

    print()
    print(f"Cluster ID:      {cluster.cluster_id}")
    print(f"Cluster Details: {cluster.details_url}")
    print()
    print("To check job status, you can run:")
    print(f"  {status_command}")
