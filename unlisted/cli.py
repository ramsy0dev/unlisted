import os
import sys
import json
import typer

from queue import Queue

from rich import print
from rich.console import Console

from unlisted import constants
from unlisted.src.messages import info, errors

from unlisted.src.utils.check_url import is_url
from unlisted.src.utils.create_channel_url import channel_url
from unlisted.src.utils.banner import banner

from unlisted.src.dig import Dig
from unlisted.src.proxy import ProxyHandler

# init cli
cli = typer.Typer()

@cli.command()
def version():
    """ Unlisted's current version """
    print(f"Version [bold cyan]{constants.VERSION}[bold white]")

@cli.command()
def dig(
    channel_identifier: str = None,
    open_search: bool = typer.Option(False, "--open", help="Dig unlisted videos for all channels"),
    threads: int = typer.Option(3, "--threads", help="Threads to use"),
    output_file_path: str = typer.Option("./", "--output", help="Path to a file to save the results in"),
    ignore_uids_from_result: str = typer.Option(None,
    "--ignore-uids-from-result", help="Ignore used videos UIDs from a result file")
):
    """ Digs a channel's unlisted videos, or it can be set to open to dig for all channels """
    console = Console()
    console._log_render.omit_repeated_times = False

    current_channel_url = None

    if channel_identifier is None and not open_search:
        console.log(errors.CHANNEL_IDENTIFIER_REQUIRED)
        sys.exit(1)

    if channel_identifier is not None:
        if is_url(text=channel_identifier):
            console.log(errors.CHANNEL_IDENTIFIER_SHOULD_NOT_BE_A_URL)
            sys.exit(1)

        current_channel_url = channel_url(channel_name=channel_identifier)

    if not os.path.exists(output_file_path):
        console.log(errors.OUTPUT_FILE_PATH_NOT_FOUND)
        sys.exit(1)

    data = None # List of data from an output file

    if ignore_uids_from_result is not None:
        if not os.path.isfile(ignore_uids_from_result) or not os.path.exists(ignore_uids_from_result):
            console.log(errors.RESULT_FILE_PATH_NOT_FOUND)
            sys.exit(1)

        with open(ignore_uids_from_result, "r") as result_file:
            data = json.load(result_file)

    regular_result_keys = [
        "package",
        "version",
        "author",
        "channel_name",
        "unlisted_videos_data",
        "used_videos_uid"
    ]

    for key in regular_result_keys:
        if data is not None and key not in data.keys():
            console.log(errors.RESULT_FILE_IS_CORRUPTED)
            sys.exit(1)

    # Queue
    status_updates = Queue() # for status bar messages
    console_log_msgs = Queue() # for log messages

    def update_status(msg: str):
        status_updates.put(msg)

    def console_log(log_msg: str):
        console_log_msgs.put(log_msg)

    with console.status(info.FETCHING_AND_VALIDATING_PROXIES) as status:
        proxy_handler = ProxyHandler()

        # Fetching and validating proxies
        proxy_handler.fetch()

        dig = Dig(
            channel_identifier=channel_identifier,
            channel_url=current_channel_url,
            proxy_handler=proxy_handler,
            threads=threads,
            status=status,
            output_file_path=output_file_path,
            is_open_search=open_search,
        )

        dig.used_videos_uid = data["used_videos_uid"] if data is not None else [] # empty list for used uids if the `data` is None

        if current_channel_url is not None:
            # Check the channel_url
            status.update(info.CHECKING_CHANNEL_URL(channel_url=current_channel_url))

            if not dig.check_channel_url():
                console.log(info.CHANNEL_URL_IS_NOT_VALID(channel_url=current_channel_url))
                sys.exit(1)

        # Start digging unlisted videos
        dig_status_msg = None
        if not open_search:
            dig_status_msg = f"Digging unlisted videos from channel [bold green]'{channel_identifier}'[bold white]..."
        else:
            dig_status_msg = "Digging unlisted videos for [bold green]all[bold white] channels..."

        status.update(dig_status_msg)

        dig.start(
            console_log=console_log,
            update_status=update_status,
            dig_status_msg=dig_status_msg
        )

        while not dig.exit_flag.is_set():
            # Update the status bar
            status_msg = status_updates.get()
            status.update(status_msg)

            # Log out the log messages
            if not console_log_msgs.empty():
                log_msg = console_log_msgs.get()
                console.log(log_msg)

        console.log(f"[bold green][ ! ] [bold white]Results saved to [bold yellow]'{dig.output_file_path}'[bold white]")

def run():
    """ Runs Unlisted """
    banner()
    cli()

if __name__ == "__main__":
    run()
