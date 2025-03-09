import os
import re
import json
import random
import signal
import string
import requests
import threading

from rich.console import Console
from pytube import (
    Channel,
    YouTube
)
from user_agent import generate_user_agent

from unlisted import constants

# Costum proxy handler
from unlisted.proxy_handler import ProxyHandler

# Log info level messages
from unlisted.log_msgs import info

# Costum Thread task
from unlisted.thread_task import ThreadTask

class Dig(object):
    """ Unlisted videos digger """
    public_videos_uid   :   list     =   list()
    used_videos_uid     :   list     =   list()

    unlisted_videos     :   list     =   list()
    unlisted_videos_data:   list     =   list()

    channel_name: str = None

    running_threads     :   list     =   list()
    exit_flag           :   threading.Event     =   threading.Event()

    faild_attempts: int = 0

    def __init__(self, channel_identifier: str, channel_url: str, proxy_handler: ProxyHandler, status: Console.status, threads: int | None = 3, output_file_path: str | None = None, is_open_search: bool | None = False) -> None:
        self.channel_identifier = channel_identifier
        self.channel_url = channel_url
        self.proxy_handler = proxy_handler
        self.threads = threads
        self.status = status
        self.output_file_path = output_file_path
        self.is_open_search = is_open_search

    def check_channel_url(self) -> bool:
        """ Checks if the `channel_url` exists """
        # The following regex will check for YouTube urls that leads to a
        # YouTube channel. it will look for URLs that contain "youtube.com"
        # followed by either "c/", "user/", or "channel/", and then capturing
        #  the channel identifier (username) using the ([a-zA-Z0-9_-]+) group.
        url_regex = r'\bhttps?://(?:www\.)?youtube\.com/(?:c/|user/|channel/|@)([a-zA-Z0-9_-]+)\b'

        urls = re.findall(url_regex, self.channel_url) # The result should be a list containing one item wich is the `self.channel_url` in case it's a valid YouTube channel url

        if len(urls) != 1:
            return False

        # Check if the channel exists or not
        headers = {
            "User-Agent": generate_user_agent()
        }

        response = requests.get(
            self.channel_url,
            headers=headers,
            proxies=self.proxy_handler.get_random_proxy()
        )

        if response.status_code != 200:
            return False

        return True

    def start(self, console_log, update_status, dig_status_msg: str) -> None:
        """ Starts the `dig` function in multipule threads """
        # Fetch all the UIDs that are used in the public videos
        # of the channel
        if not self.is_open_search:
            channel = Channel(
                self.channel_url,
                proxies=self.proxy_handler.get_random_proxy()
            )

            self.public_videos_uid = self._fetch_public_videos(
                channel=channel
            )
            self.channel_name = self._channel_author(
                channel=channel
            )

        signal.signal(signal.SIGINT, self._signal_handler)

        self._initiate_file_output()

        for _ in range(self.threads):
            thread_task = ThreadTask(
                target_function=self.dig,
                args=(console_log, update_status, dig_status_msg, _)
            )
            thread_task.start()
            self.running_threads.append(thread_task)

    def dig(self, console_log, update_status, dig_status_msg: str, thread_index: int) -> None:
        """ Digs all the unlisted videos in a channel """
        url = "https://youtube.com/watch?v="

        while not self.exit_flag.is_set():
            video_uid = self._generate_video_uid()
            video_url = f"{url}{video_uid}"

            self.used_videos_uid.append(video_uid)

            video = YouTube(
                video_url,
                proxies=self.proxy_handler.get_random_proxy()
            )

            try:
                video.check_availability()

                video_data = {
                    "video_uid": video_uid,
                    "video_url": video.watch_url,
                    "video_title": video.title,
                }

                if self.channel_name is not None:
                    if video.author == self.channel_name:
                        # In case the video belongs to the channel that we are looking
                        # we will be adding it to the `self.unlisted_videos` list
                        console_log(info.FOUND_UNLISTED_VIDEO_FOR_CURRENT_CHANNEL(video_url=video.watch_url, channel_name=self.channel_name, thread_index=thread_index))
                        self.unlisted_videos.append(video_uid)
                    else:
                        # Other wise we are just going to inform the user that we found
                        # a valid video
                        console_log(info.FOUND_UNLISTED_VIDEO_FOR_OTHER_CHANNEL(video_url=video.watch_url, channel_name=self.channel_name, thread_index=thread_index))
                elif self.is_open_search:
                    video_data["channel_name"] = video.author # Adding the `channel_name` in case the user spesified to do an open search
                    console_log(info.FOUND_UNLISTED_VIDEO_FOR_OTHER_CHANNEL(video_url=video.watch_url, channel_name=self.channel_name, thread_index=thread_index))
                    self.unlisted_videos.append(video_uid)

                self.unlisted_videos_data.append(video_data)
            except Exception as error:
                self.faild_attempts += 1

            update_status(f"{dig_status_msg}\n[bold white]==> Results: [bold green]Found: {len(self.unlisted_videos)}, [bold yellow]Used video UID: {len(self.used_videos_uid)}, [bold red]Faild attempts: {self.faild_attempts}[bold white]")

    def _fetch_public_videos(self, channel: Channel) -> list[str]:
        """ Fetchs the channel's public videos urls """
        videos_uid = []
        public_videos_urls = channel.video_urls

        for video_url in public_videos_urls:
            # video_uid that is used for this video
            # the UID is present in the url. Usually
            # a video url is formated like so
            # https://www.youtube.com/watch?v=xxxxxxxxxxx
            # the UID in this exmaple is 'xxxxxxxxxxx'
            video_uid = video_url.split("=")[-1]
            videos_uid.append(video_uid)

        return videos_uid

    def _signal_handler(self, sig, frame):
        self.exit_flag.set()

        self._save_results() # Save the results before shuting down all the threads

        self.status.update("[bold white]CTRL+C Detected. [bold red]Exiting...[bold white]")

        for _ in self.running_threads:
            _.thread.join()

    def _channel_author(self, channel: Channel) -> str:
        """ Gets the channel author """
        return channel.channel_name

    def _generate_video_uid(self) -> str:
        """ Generates a video UID """
        # A cobination of lowecase and uppercase
        # alphabets conbined with numbers 0-9 and '-'
        chars = string.ascii_lowercase + string.ascii_uppercase + ''.join([str(i) for i in range(0, 10)]) + '-'

        video_uid = ""

        while True:
            for _ in range(11):
                video_uid += random.choice(chars)

            if video_uid not in self.public_videos_uid + self.used_videos_uid + self.unlisted_videos:
                break

            video_uid = ""

        return video_uid

    def _initiate_file_output(self) -> None:
        """ Save the primary template into an output file """
        data = constants.UNLISTED_VIDEOS_DATA

        if not self.is_open_search:
            data["channel_name"] = self.channel_name

        if os.path.isfile(self.output_file_path):
            pass
        elif self.output_file_path == "./":
            self.output_file_path = f"./unlisted-dig-results-{self.channel_name if self.channel_name is not None else random.choice([i for i in range(100000, 1000000)])}.json"
        else:
            if self.output_file_path.split("/")[-1] == "":
                self.output_file_path = "/".join(
                    self.output_file_path.split("/")[:-1]
                    ) + f"/unlisted-dig-results-{self.channel_name if self.channel_name is not None else random.choice([i for i in range(100000, 1000000)])}.json"
            else:
                self.output_file_path = "/".join(
                    self.output_file_path.split("/")
                    ) + f"/unlisted-dig-results-{self.channel_name if self.channel_name is not None else random.choice([i for i in range(100000, 1000000)])}.json"

        with open(self.output_file_path, "w") as output_file:
            output_file.write(json.dumps(data, indent=4))

    def _save_results(self) -> None:
        """ Saves the results into the `self.output_file_path` """
        output_file_data = None

        with open(self.output_file_path, "r") as output_file:
            output_file_data = json.load(output_file)

        output_file_data["unlisted_videos_data"]    =   self.unlisted_videos_data
        output_file_data["used_videos_uid"]         =   self.used_videos_uid

        with open(self.output_file_path, "w") as output_file:
            output_file.write(json.dumps(output_file_data, indent=4))
