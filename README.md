<div align="center">

# Unlisted

</div>

``` bash
                 _ _     _           _
     /\ /\ _ __ | (_)___| |_ ___  __| |
    / / \ \ '_ \| | / __| __/ _ \/ _` |
    \ \_/ / | | | | \__ \ ||  __/ (_| |
     \___/|_| |_|_|_|___/\__\___|\__,_| Version 0.1.0
                    made by `ramsy0dev`
```


# Table of content

* [What is Unlisted?](#what-is-unlisted)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [License](#license)

# What is Unlisted?

Unlisted is an open source tool that scraps YouTube looking for unlisted video for a specific YouTube channel. It works by randomly generating videos UID (this UID is different than the public videos UID of this channel and it doesn't repeat it self) that is then passed in to the `v` parameter in `https://youtube.com/watch?v=` then it checks first if this is a valid video UID, if that is the case then it's checks if the channel's name correspond to the one that is specified with the flag `--channel-identifier`.

# Prerequisites

* python3.10+
* poetry (python package)

# Installation

``` bash
git clone https://github.com/ramsy0dev/unlisted
cd unlisted
poetry build
pip install ./dist/unlisted-*.tar.gz (this will go ahead and download all the dependecies and unlisted to your system so you can use it as command)
```

# Usage

Using Unlisted is fairly simple as it's comes with only two commands wich you can see in the following help menu:

``` bash
                 _ _     _           _
     /\ /\ _ __ | (_)___| |_ ___  __| |
    / / \ \ '_ \| | / __| __/ _ \/ _` |
    \ \_/ / | | | | \__ \ ||  __/ (_| |
     \___/|_| |_|_|_|___/\__\___|\__,_| Version 0.1.0
                    made by `ramsy0dev`


 Usage: unlisted [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                         │
│ --help                        Show this message and exit.                                                                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ dig             Digs a channel's unlisted videos, or it can be set to open to dig for all channels                                                                     │
│ version         Unlisted's current version                                                                                                                             │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
The command `dig` is the primarly command in Unlisted, with it you can initiat a search for unlisted YouTube videos for a specific channel, it takes extra argument with are:

``` bash

                 _ _     _           _
     /\ /\ _ __ | (_)___| |_ ___  __| |
    / / \ \ '_ \| | / __| __/ _ \/ _` |
    \ \_/ / | | | | \__ \ ||  __/ (_| |
     \___/|_| |_|_|_|___/\__\___|\__,_| Version 0.1.0
                    made by `ramsy0dev`


 Usage: unlisted dig [OPTIONS]

 Digs a channel's unlisted videos, or it can be set to open to dig for all channels

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --channel-identifier             TEXT     [default: None]                                                                                                              │
│ --open                                    Dig unlisted videos for all channels                                                                                         │
│ --threads                        INTEGER  Threads to use [default: 3]                                                                                                  │
│ --output                         TEXT     Path to a file to save the results in [default: ./]                                                                          │
│ --ignore-uids-from-result        TEXT     Ignore used videos UIDs from a result file [default: None]                                                                   │
│ --help                                    Show this message and exit.                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
The most important flag here is `--channel-identifier` wich is the @tag for the channel that you are targeting if it's not valid then Unlisted will just exit with an error.
Additionally there is `--ignore-uids-from-result` wich comes in handy if you have canceled a search and then you want to resume it you could just pass in the path to the results file of that search to continue on. And there is also `--open` wich targets all channels (you don't have to pass in a `--channel-identifier`) and at last there is threads, i don't recommend setting like 17 threads if you have a bad internet connection because that wouldn't fix it, and also `--output` to specify where you want to save your output file or undear what file name should it be saved.

Here is a basic usage that you can test:

``` bash
unlisted dig --channel-identifier LinusTechTips --threads 7
```

>__Notice__ that we don't pass in the channel identifier with the `@` sign other wise it would fail.

# License

GPL-V3.0
