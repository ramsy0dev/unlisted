# ------------- info messages ---------------
# NOTE: Please do not change any of the following
# info messages unless their was a typo or some
# of them where hard to understand by the users

CHECKING_CHANNEL_URL = lambda channel_url: f"[bold white]Checking channel URL [bold green]'{channel_url}'[bold white]..."
CHANNEL_URL_IS_NOT_VALID = lambda channel_url: f"[bold red][ - ] [bold white]Invalid channel URL [bold yellow]{channel_url}[bold white]. Please verify the channel URL and try again."

FETCHING_AND_VALIDATING_PROXIES = "[bold white]Fetching and validating proxies [bold yellow](this may require a few minutes, please wait)[bold white]...[bold white]"

FOUND_UNLISTED_VIDEO_FOR_CURRENT_CHANNEL = lambda video_url, channel_name, thread_index: f"[bold green][ + ] [bold white]THREAD [bold red]#{thread_index}[bold white]: [bold white]Found an unlisted video URL [bold green]'{video_url}'[bold white] for the current channel [bold green]'{channel_name}'[bold white]"
FOUND_UNLISTED_VIDEO_FOR_OTHER_CHANNEL = lambda video_url, channel_name, thread_index: f"[bold green][ + ] [bold white]THREAD [bold red]#{thread_index}[bold white]: [bold white]Found an unlisted video URL [bold green]'{video_url}'[bold white] for channel [bold green]'{channel_name}'[bold white]"
