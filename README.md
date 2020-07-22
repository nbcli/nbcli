# NetBox Client

Extensible command-line interface for Netbox using pynetbox module. 

[![asciicast](https://asciinema.org/a/348204.svg)](https://asciinema.org/a/348204)

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

## Quickstart

```
$ pip install nbcli
$ nbcli init
Edit pynetbox 'url' and 'token' entries in user_config.py:
        ~/.nbcli/user_config.py
```

At the very minimum, you need to specify a url and token in the user_config.py file

```python
pynetbox = dict(
    url='http://localhost:8080',                        # your netbox url
    token='0123456789abcdef0123456789abcdef01234567')   # your API token
```

If you need to disable SSL verification

```python
requests = dict(verify=False)
```

## Notable Features

- [Search](https://github.com/ericgeldmacher/nbcli/blob/release/docs/search.md) Netbox instance from command line
- [Show](https://github.com/ericgeldmacher/nbcli/blob/release/docs/show.md) detail view of objects
- [pynb](https://github.com/ericgeldmacher/nbcli/blob/release/docs/pynb.md) Command line wrapper for pynetbox
- [Shell](https://github.com/ericgeldmacher/nbcli/blob/release/docs/shell.md) with preloaded pynetbox endpoints
    - Run scripts in shell environment.
- [Coustemizable](https://github.com/ericgeldmacher/nbcli/blob/release/docs/views.md) table/detail views
- [Extensable](https://github.com/ericgeldmacher/nbcli/blob/release/docs/commands.md) by adding custom commands
