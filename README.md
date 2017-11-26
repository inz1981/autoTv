# autoTv

The autoTv is a script written in python and is intended to organize the
downloaded content into appropriate folders. Basically, different contents will
be decompressed (RAR/ZIP) or copied or moved from the downloaded folder into a
media folder, where typically the users Media Player such as PLEX / KODI /
AppleTV etc. should read from.

The subcategories of the content that is supported is:

- Movies
- TV Series
- Music
- Pictures

## Table of contents

<details>

<!-- toc -->
- [Configuration file](#Configuration-file)
- [Example](#example)
<!-- tocstop -->

</details>


## Configuration file

The autoTV uses a configuration file in ini format and en example file is
located in the folder `cfg_examples/autotv.cfg`

## Example

```
python atv.py -h

Usage: atv.py -c FILE [--debug]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -c FILE, --config=FILE
                        the config file(e.g. autotv.cfg)
  --debug               print more info
```

