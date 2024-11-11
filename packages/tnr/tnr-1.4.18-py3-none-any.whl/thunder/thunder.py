import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    import rich_click as click
    import rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
    from thunder import auth, auth_helper
    import os
    from os.path import join
    from scp import SCPClient
    import paramiko
    import subprocess
    import time
    import platform

    from thunder import utils
    from thunder.get_latest import get_latest

    try:
        from importlib.metadata import version
    except Exception as e:
        from importlib_metadata import version

    import requests
    from packaging import version as version_parser
    from yaspin import yaspin


PACKAGE_NAME = "tnr"
ENABLE_RUN_COMMANDS = True if platform.system() == "Linux" else False
INSIDE_INSTANCE = False
INSTANCE_ID = None


# Remove the DefaultCommandGroup class
DISPLAYED_WARNING = False
logging_in = False


def get_token():
    global logging_in, DISPLAYED_WARNING

    if "TNR_API_TOKEN" in os.environ:
        return os.environ["TNR_API_TOKEN"]

    token_file = auth_helper.get_credentials_file_path()
    if not os.path.exists(token_file):
        logging_in = True
        auth.login()

    with open(auth_helper.get_credentials_file_path(), "r") as f:
        lines = f.readlines()
        if len(lines) == 1:
            token = lines[0].strip()
            return token

    auth.logout()
    logging_in = True
    token = auth.login()
    return token


def init():
    global INSIDE_INSTANCE, INSTANCE_ID, ENABLE_RUN_COMMANDS

    if not ENABLE_RUN_COMMANDS:
        utils.setup_config(get_token())
        config = utils.read_config()
    else:
        config = {}

    deployment_mode = config.get("deploymentMode", "public")

    if deployment_mode == "public":
        if ENABLE_RUN_COMMANDS:
            utils.setup_instance(get_token())

        # Determine if we are currently in a TC instance
        INSTANCE_ID = utils.get_instance_id(get_token())
        if INSTANCE_ID == -1:
            exit(1)

        INSIDE_INSTANCE = INSTANCE_ID is not None

    elif deployment_mode == "on-prem":
        pass

    elif deployment_mode == "test":
        ENABLE_RUN_COMMANDS = True
        INSTANCE_ID = 0

    else:
        raise click.ClickException(
            "deploymentMode field in `~/.thunder/config.json` is set to an invalid value"
        )


init()

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.COMMAND_GROUPS = {
    "cli": [
        (
            {
                "name": "Instance management",
                "commands": ["create", "delete", "start", "stop"],
            }
            if not INSIDE_INSTANCE
            else {}
        ),
        {
            "name": "Utility",
            "commands": (
                ["device", "status", "scp"]
                if INSIDE_INSTANCE
                else ["connect", "status", "scp", "resize"]
            ),
        },
        (
            {
                "name": "Account management",
                "commands": ["login", "logout"],
            }
            if not INSIDE_INSTANCE
            else {}
        ),
    ]
}

COLOR = "green" if INSIDE_INSTANCE else "cyan"
click.rich_click.STYLE_OPTION = COLOR
click.rich_click.STYLE_COMMAND = COLOR

main_message = (
    f":link: [bold {COLOR}]You're connected to a Thunder Compute instance. Any process you run will automatically use a GPU on-demand.[/]"
    if INSIDE_INSTANCE
    else f":laptop_computer: [bold {COLOR}]You're in a local environment, use these commands to manage your Thunder Compute instances.[/]"
)


@click.group(
    cls=click.RichGroup,
    help=main_message,
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.version_option(version=version(PACKAGE_NAME))
def cli():
    meets_version, versions = does_meet_min_required_version()
    if not meets_version:
        raise click.ClickException(
            f'Failed to meet minimum required tnr version to proceed (current=={versions[0]}, required=={versions[1]}), please run "pip install --upgrade tnr" to update'
        )
    utils.validate_config()


if ENABLE_RUN_COMMANDS:

    @cli.command(
        help="Runs process on a remote Thunder Compute GPU. The GPU type is specified in the ~/.thunder/dev file. For more details, please go to thundercompute.com",
        context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
        hidden=True,
    )
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    def run(args):
        if not args:
            raise click.ClickException("No arguments provided. Exiting...")

        token = get_token()
        endpoint = f"https://api.thundercompute.com:8443/uid"
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {token}"})

        if response.status_code != 200:
            raise click.ClickException(
                "Failed to get info about user, is the API token correct?"
            )
        uid = response.text

        # Run the requested process
        if not INSIDE_INSTANCE:
            message = "[yellow]Attaching to a remote GPU from a non-managed instance - this will hurt performance. If this is not intentional, please connect to a managed CPU instance using tnr create and tnr connect <INSTANCE ID>[/yellow]"
            panel = Panel(
                message,
                title=":warning:  Warning :warning: ",
                title_align="left",
                highlight=True,
                width=100,
                box=box.ROUNDED,
            )
            rich.print(panel)

        config = utils.read_config()
        if "binary" in config:
            binary = config["binary"]
            if not os.path.isfile(binary):
                raise click.ClickException(
                    "Invalid path to libthunder.so in config.binary"
                )
        else:
            binary = get_latest("client", "~/.thunder/libthunder.so")
            if binary == None:
                raise click.ClickException("Failed to download binary")

        device = config.get("gpuType", "t4")

        os.environ["SESSION_USERNAME"] = uid
        os.environ["TOKEN"] = token
        os.environ["__TNR_RUN"] = "true"
        os.environ["IP_ADDR"] = "0.0.0.0"
        if device.lower() != "cpu":
            os.environ["LD_PRELOAD"] = f"{binary}"

        # This should never return
        try:
            os.execvp(args[0], args)
        except FileNotFoundError:
            raise click.ClickException(f"Invalid command: \"{' '.join(args)}\"")
        except Exception as e:
            raise click.ClickException(f"Unknown exception: {e}")

    @cli.command(
        help="If device_type is empty, displays the current GPU and a list of available GPUs. If device_name has a value, switches to the specified device. Input billing information at console.thundercompute.com to use devices besides NVIDIA T4s",
        hidden=not INSIDE_INSTANCE,
    )
    @click.argument("device_type", required=False)
    @click.option("-n", "--ngpus", type=int, help="Number of GPUs to use")
    @click.option("--raw", is_flag=True, help="Output raw device information")
    def device(device_type, ngpus, raw):
        config = utils.read_config()
        supported_devices = set(
            [
                "cpu",
                "t4",
                "v100",
                "a100",
                "l4",
                "p4",
                "p100",
                "h100",
            ]
        )

        if device_type is None:
            # User wants to read current device
            device = config.get("gpuType", "t4")
            gpu_count = config.get("gpuCount", 1)

            if raw is not None and raw:
                if gpu_count == 1:
                    click.echo(device.upper())
                else:
                    click.echo(f"{gpu_count}x{device.upper()}")
                return

            if device.lower() == "cpu":
                click.echo(
                    click.style(
                        "📖 No GPU selected - use `tnr device <gpu-type>` to select a GPU",
                        fg="white",
                    )
                )
                return

            console = Console()
            if gpu_count == 1:
                console.print(f"[bold green]📖 Current GPU:[/] {device.upper()}")
            else:
                console.print(
                    f"[bold green]📖 Current GPUs:[/][white] {gpu_count} x {device.upper()}[/]"
                )

            utils.display_available_gpus()
            return

        if device_type.lower() not in supported_devices:
            raise click.ClickException(
                f"Unsupported device type: {device_type}. Please select one of CPU, T4, V100, A100, L4, P4, P100, or H100"
            )

        if device_type.lower() == "cpu":
            config["gpuType"] = "cpu"
            config["gpuCount"] = 0

            click.echo(
                click.style(
                    f"✅ Device set to CPU, you are now disconnected from any GPUs",
                    fg="green",
                )
            )
        else:
            config["gpuType"] = device_type.lower()

            gpu_count = ngpus if ngpus is not None else 1
            config["gpuCount"] = gpu_count
            click.echo(
                click.style(
                    f"✅ Device set to {gpu_count} x {device_type.upper()}", fg="green"
                )
            )
        utils.write_config(config)

else:

    @cli.command(hidden=True)
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    def run(args):
        raise click.ClickException(
            "tnr run is supported within Thunder Compute instances. Create one with 'tnr create' and connect to it using 'tnr connect <INSTANCE ID>'"
        )

    @cli.command(hidden=True)
    @click.argument("device_type", required=False)
    @click.option("-n", "--ngpus", type=int, help="Number of GPUs to use")
    @click.option("--raw", is_flag=True, help="Output raw device information")
    def device(device_type, ngpus, raw):
        raise click.ClickException(
            "tnr device is supported within Thunder Compute instances. Create one with 'tnr create' and connect to it using 'tnr connect <INSTANCE ID>'"
        )


@cli.command(hidden=True)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def launch(args):
    return run(args)


if INSIDE_INSTANCE:
    @cli.command(
        help="Lists details of your current Thunder Compute instance and any actively running GPU processes"
    )
    def status():
        token = get_token()

        # Retrieve IP address and active sessions in one call
        current_ip, active_sessions = utils.get_active_sessions(token)

        # Extract storage information
        storage_total = (
            subprocess.check_output("df -h / | awk 'NR==2 {print $2}'", shell=True)
            .decode()
            .strip()
        )
        storage_available = (
            subprocess.check_output("df -h / | awk 'NR==2 {print $4}'", shell=True)
            .decode()
            .strip()
        )

        disk_space_text = Text(
            f"Disk Space: {storage_available} / {storage_total} (Available / Total)"
        )

        # Format INSTANCE_ID and current_ip as Text objects with a specific color (e.g., white)
        instance_id_text = Text(f"ID: {INSTANCE_ID}", style="white")
        current_ip_text = Text(f"Public IP: {current_ip}", style="white")

        # Console output for instance details
        console = Console()
        console.print(Text("Instance Details", style="bold green"))
        console.print(instance_id_text)
        console.print(current_ip_text)
        console.print(disk_space_text)
        console.print()

        # GPU Processes Table
        gpus_table = Table(
            title="Active GPU Processes",
            title_style="bold green",
            title_justify="left",
            box=box.ROUNDED,
        )

        gpus_table.add_column("GPU Type", justify="center")
        gpus_table.add_column("Duration", justify="center")

        # Populate table with active sessions data
        for session_info in active_sessions:
            gpus_table.add_row(
                f'{session_info["count"]} x {session_info["gpu"]}',
                f"{session_info['duration']}s",
            )

        # If no active sessions, display placeholder
        if not active_sessions:
            gpus_table.add_row("--", "--")

        # Print table
        console.print(gpus_table)

else:

    @cli.command(
        help="Lists details of Thunder Compute instances associated with your account"
    )
    def status():
        token = get_token()
        success, error, instances = utils.get_instances(token)
        if not success:
            raise click.ClickException(f"Status command failed with error: {error}")

        instances_table = Table(
            title="Thunder Compute Instances",
            title_style="bold cyan",
            title_justify="left",
            box=box.ROUNDED,
        )

        instances_table.add_column("ID", justify="center")
        instances_table.add_column("Status", justify="center")
        instances_table.add_column("Address", justify="center")
        instances_table.add_column("Disk Size", justify="center")
        instances_table.add_column("Creation Date", justify="center")

        for instance_id, metadata in instances.items():
            # Set status color based on status
            if metadata["status"] == "RUNNING":
                status_color = "green"
            elif metadata["status"] == "STOPPED":
                status_color = "red"
            else:
                status_color = "yellow"

            # Handle missing IP addresses
            ip_entry = metadata["ip"] if metadata["ip"] else "--"

            # Convert all entries to strings to avoid NotRenderableError
            instances_table.add_row(
                str(instance_id),
                Text(metadata["status"], style=status_color),
                str(ip_entry),
                f"{metadata['storage']}GB",
                str(metadata["createdAt"]),
            )


        # If there are no instances, display placeholders
        if len(instances) == 0:
            instances_table.add_row("--", "--", "--", "--", "--")

        console = Console()
        console.print(instances_table)


@cli.command(
    help="Create a new Thunder Compute instance",
    hidden=INSIDE_INSTANCE,
)
def create():
    token = get_token()
    success, error = utils.create_instance(token)
    if success:
        click.echo(
            click.style(
                "Successfully created a Thunder Compute instance! View this instance with 'tnr status'",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to create Thunder Compute instance: {error}"
        )


@cli.command(
    help="Permanently deletes a Thunder Compute instance. This action is not reversible",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def delete(instance_id):
    token = get_token()
    success, error = utils.delete_instance(instance_id, token)
    if success:
        click.echo(
            click.style(
                f"Successfully deleted Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )

        utils.remove_instance_from_ssh_config(f"tnr-{instance_id}")
    else:
        raise click.ClickException(
            f"Failed to delete Thunder Compute instance {instance_id}: {error}"
        )
    
@cli.command(
    help="Increases the disk size of a Thunder Compute instance",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
@click.argument("new_size", required=True, type=int)
def resize(instance_id, new_size):

    if new_size > 1024:
        raise click.ClickException(
            f"❌ The requested size ({new_size}GB) exceeds the 1TB limit."
        )
    
    token = get_token()
    success, error, instances = utils.get_instances(token)
    if not success:
        raise click.ClickException(f"Failed to list Thunder Compute instances: {error}")

    metadata = instances.get(instance_id)
    if not metadata or metadata["ip"] is None:
        raise click.ClickException(
            f"Instance {instance_id} is not available to connect or has no valid IP."
        )

    ip = metadata["ip"]
    keyfile = utils.get_key_file(metadata["uuid"])
    if not os.path.exists(keyfile):
        if not utils.add_key_to_instance(instance_id, token):
            raise click.ClickException(
                f"Unable to find or create SSH key file for instance {instance_id}."
            )

    # Step 1: Establish SSH connection with retries
    start_time = time.time()
    connection_successful = False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while time.time() - start_time < 60:
        try:
            ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=10)
            connection_successful = True
            break
        except Exception:
            time.sleep(5)  # Brief wait before retrying

    if not connection_successful:
        raise click.ClickException(
            "Failed to connect to the Thunder Compute instance within a minute. Please retry this command or contact support@thundercompute.com if the issue persists."
        )

    # Step 2: Get current disk size using SSH
    current_size = utils.get_current_disk_size_ssh(ssh)
    if current_size is None:
        click.echo(click.style("❌ Unable to retrieve the current disk size.", fg="red"))
        ssh.close()
        return

    # Step 3: Check if resizing is needed
    if current_size >= new_size:
        click.echo(click.style(
            f"❌ The current disk size ({current_size}GB) is already greater than or equal to the requested size ({new_size}GB). No resize needed.",
            fg="yellow"
        ))
        ssh.close()
        return

    # Step 3.5: Verify that user wants to resize disk
    message = "[yellow]This action cannot be undone, persistent disk size can only be increased.[/yellow]"
    panel = Panel(
        message,
        title=":warning:  Warning :warning: ",
        title_align="left",
        highlight=True,
        width=100,
        box=box.ROUNDED,
    )
    rich.print(panel)
    if not click.confirm("Would you like to continue?"):
        click.echo(
            click.style(
            "The operation has been cancelled. No changes to the instance have been made.",
            fg="cyan",
            )
        )
        return
    
    # Step 4: Resize the disk
    success, error = utils.resize_instance(instance_id, new_size, token)
    if success:
        _, stdout, stderr = ssh.exec_command("""
            sudo apt install -y cloud-guest-utils
            sudo growpart /dev/sda 1
            sudo resize2fs /dev/sda1
        """)
        # Wait for standard output, otherwise this won't complete correctly
        stdout.read().decode()
        stderr.read().decode()
        click.echo(
            click.style(
                f"Successfully resized the persistent disk for instance {instance_id} to {new_size}GB.",
                fg="cyan",
            )
        )
    else:
        ssh.close()
        raise click.ClickException(
            f"Failed to resize the persistent disk on Thunder Compute instance {instance_id}: {error}"
        )


@cli.command(
    help="Starts a stopped Thunder Compute instance",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def start(instance_id):
    token = get_token()
    success, error = utils.start_instance(instance_id, token)
    if success:
        click.echo(
            click.style(
                f"Successfully started Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to start Thunder Compute instance {instance_id}: {error}"
        )


@cli.command(
    help="Stops a running Thunder Compute instance. Stopped instances have persistent storage and can be restarted at any time",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def stop(instance_id):
    token = get_token()
    success, error = utils.stop_instance(instance_id, token)
    if success:
        click.echo(
            click.style(
                f"Successfully stopped Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to stop Thunder Compute instance {instance_id}: {error}"
        )


@cli.command(
    help="Connects to the Thunder Compute instance with the specified instance_ID",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=False)
def connect(instance_id=None):
    # Set default instance_id to '0' if not provided
    instance_id = instance_id or "0"
    click.echo(
        click.style(
            f"Connecting to Thunder Compute instance with instance_id: {instance_id}...",
            fg="cyan",
        )
    )
    token = get_token()
    success, error, instances = utils.get_instances(token)
    if not success:
        raise click.ClickException(f"Failed to list Thunder Compute instance: {error}")

    for curr_instance_id, metadata in instances.items():
        if curr_instance_id == instance_id:
            if metadata["ip"] == None:
                raise click.ClickException(
                    f"Instance {instance_id} is not available to connect"
                )

            ip = metadata["ip"]

            if ip is None or ip == "":
                raise click.ClickException(
                    f"Unable to connect to instance {instance_id}, is the instance running?"
                )

            keyfile = utils.get_key_file(metadata["uuid"])
            if not os.path.exists(keyfile):
                if not utils.add_key_to_instance(instance_id, token):
                    raise click.ClickException(
                        f"Unable to find or create ssh key file for instance {instance_id}"
                    )

            start_time = time.time()
            connection_successful = False
            while start_time + 60 > time.time():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=10)
                    connection_successful = True
                    break
                except Exception as e:
                    continue

            if not connection_successful:
                raise click.ClickException(
                    "Failed to connect to the Thunder Compute instance within one minute. Please retry this command or contant the developers at support@thundercompute.com if this issue persists"
                )

            basedir = join(os.path.expanduser("~"), ".thunder")
            ssh.exec_command("mkdir -p ~/.thunder && chmod 700 ~/.thunder")
            stdin, stdout, stderr = ssh.exec_command("pip install --upgrade tnr")
            stdout.read().decode()  # Forces the command to get executed

            scp = SCPClient(ssh.get_transport())

            if os.path.exists(join(basedir, "token")):
                scp.put(join(basedir, "token"), remote_path="~/.thunder/token")

            # Update ~/.ssh/config
            host_alias = f"tnr-{instance_id}"
            exists, prev_ip = utils.get_ssh_config_entry(host_alias)
            if not exists:
                utils.add_instance_to_ssh_config(ip, keyfile, host_alias)
            else:
                if ip != prev_ip:
                    utils.update_ssh_config_ip(host_alias, ip)

            if platform.system() == "Windows":
                subprocess.run(
                    [
                        "ssh",
                        "-q",  # Quiet mode, suppresses warnings
                        f"ubuntu@{ip}",
                        "-o",
                        "StrictHostKeyChecking=accept-new",  # Accepts new hosts permanently without asking
                        "-i",
                        rf"{keyfile}",
                        "-t",
                        f"{'export TNR_API_TOKEN=' + os.environ['TNR_API_TOKEN'] + ';' if 'TNR_API_TOKEN' in os.environ else ''} exec /home/ubuntu/.local/bin/tnr run /bin/bash",
                    ],
                    shell=True,
                )
            else:
                subprocess.run(
                    [
                        f"ssh -q ubuntu@{ip} -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null -i {keyfile} -t '{'export TNR_API_TOKEN=' + os.environ['TNR_API_TOKEN'] + ';' if 'TNR_API_TOKEN' in os.environ else ''} exec /home/ubuntu/.local/bin/tnr run /bin/bash'"
                    ],
                    shell=True,
                )
            click.echo(click.style("⚡ Exiting thunder instance ⚡", fg="green"))
            return

    raise click.ClickException(
        f"Unable to find instance {instance_id}. Check available instances with `tnr status`"
    )


@cli.command(help="Copy data from local machine to a thunder instance")
@click.argument("src", required=True)
@click.argument("dst", required=True)
def scp(src, dst):
    token = get_token()
    success, error, instances = utils.get_instances(token)
    if not success:
        raise click.ClickException(f"Failed to list Thunder Compute instance: {error}")

    # Determine direction and instance
    src_split = src.split(":")
    dst_split = dst.split(":")
    if len(src_split) > 1:
        src_candidate_instance = src_split[0]
    else:
        src_candidate_instance = None

    if len(dst_split) > 1:
        dst_candidate_instance = dst_split[0]
    else:
        dst_candidate_instance = None

    for instance_id, metadata in instances.items():
        if (
            instance_id == src_candidate_instance
            or instance_id == dst_candidate_instance
        ):
            local_to_remote = True if instance_id == dst_candidate_instance else False
            local_path = src if local_to_remote else dst
            remote_path = dst_split[1] if local_to_remote else src_split[1]
            if remote_path == "":
                remote_path = "~/"

            if metadata["ip"] == None:
                raise click.ClickException(
                    f"Instance {instance_id} is not available. Check 'tnr status' to ensure the instance status is 'RUNNING'"
                )

            ip = metadata["ip"]

            if ip is None or ip == "":
                raise click.ClickException(
                    f"Unable to connect to instance {instance_id}. Check 'tnr status' to ensure the instance status is 'RUNNING'"
                )

            keyfile = utils.get_key_file(metadata["uuid"])
            if not os.path.exists(keyfile):
                if not utils.add_key_to_instance(instance_id, token):
                    raise click.ClickException(
                        f"Unable to find or create ssh key file for instance {instance_id}"
                    )

            start_time = time.time()
            connection_successful = False
            while start_time + 60 > time.time():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=10)
                    connection_successful = True
                    break
                except Exception as e:
                    continue

            if not connection_successful:
                raise click.ClickException(
                    "Failed to connect to the Thunder Compute instance within a minute. Please retry this command or contant the developers at support@thundercompute.com if this issue persists"
                )

            if local_to_remote:
                waiting_text = f"Copying {local_path} to {remote_path} on remote instance {instance_id}"
            else:
                waiting_text = (
                    f"Copying {remote_path} from instance {instance_id} to {local_path}"
                )

            with yaspin(text=waiting_text, color="blue") as spinner:
                transport = ssh.get_transport()
                transport.use_compression(True)

                with SCPClient(transport) as scp:
                    if local_to_remote:
                        scp.put(local_path, remote_path, recursive=True)
                    else:
                        scp.get(remote_path, local_path, recursive=True)

                spinner.ok("✅")
            return

    raise click.ClickException(
        f"Unable to find instance to copy to/from in {src} or {dst}"
    )


@cli.command(
    help="Logs in to Thunder Compute with an API token generated at console.thundercompute.com. Saves the API token to ~/.thunder/token",
    hidden=INSIDE_INSTANCE,
)
def login():
    if not logging_in:
        auth.login()


@cli.command(
    help="Logs out of Thunder Compute and deletes the saved API token",
    hidden=INSIDE_INSTANCE,
)
def logout():
    auth.logout()


def does_meet_min_required_version():
    try:
        current_version = version(PACKAGE_NAME)
        response = requests.get(
            f"https://api.thundercompute.com:8443/min_version", timeout=10
        )
        json_data = response.json() if response else {}
        min_version = json_data.get("version")
        if version_parser.parse(current_version) < version_parser.parse(min_version):
            return False, (current_version, min_version)

        return True, None

    except Exception as e:
        click.echo(
            click.style(
                "Warning: Failed to fetch minimum required tnr version",
                fg="yellow",
            )
        )
        return True, None


if __name__ == "__main__":
    cli()
