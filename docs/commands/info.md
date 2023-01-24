# nbcli info

```
$ nbcli info --help
usage: nbcli info [-h] [-v] [-q] [--detailed] [--models [MODELS]]

View Information about nbcli instance.

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      Show more logging messages
  -q, --quiet        Show fewer logging messages
  --detailed         Show more detailed info.
  --models [MODELS]  Display detailed info on given model.

View Information about nblci instance.

Example Usage:

- Show version info
  $ nbcli info

- Show more detailed info
  $ nbcli info --detailed

- List all supported models
  $ nbcli info --models

- Show information of device model
  $ nbcli info --models device
```
