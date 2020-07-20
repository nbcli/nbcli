# NetBox Client

Extensible command-line interface for Netbox using pynetbox module. 

[![asciicast](https://asciinema.org/a/348204.svg)](https://asciinema.org/a/348204)

```
$ pip install nbcli
$ nbcli init
Edit pynetbox 'url' and 'token' entries in user_config.py:
        ~/.nbcli/user_config.py

```

```
usage: nbcli [-h] <command> ...

Extensible CLI for Netbox

optional arguments:
  -h, --help  show this help message and exit

Commands:
  <command>
    init      Initialize nbcli.
    search    Search Netbox Objects
    show      Show detail view of Netbox Object
    shell     Launch interactive shell
    pynb      Wrapper for pynetbox
    nbmodels  List Netbox Models

General Options:
  -h, --help           show this help message and exit
  -v, --verbose        Show more logging messages
  -q, --quiet          Show fewer logging messages
```
