# nbcli: NetBox Command-Line Client

Extensible command-line interface for [Netbox](https://netbox.readthedocs.io/en/stable/>)
using the [pynetbox](https://pynetbox.readthedocs.io/en/latest/) module. 

!!! warning "nbcli is still in development. Syntax of commands are subject to change."

```
usage: nbcli [-h] <command> ...

Extensible CLI for Netbox

optional arguments:
  -h, --help  show this help message and exit

Commands:
  <command>
    init      Initialize nbcli.
    search    Search Netbox Objects
    filter    Filter NetBox objects.
    create    Create/Update objects with YAML file.
    shell     Launch interactive shell

General Options:
  -h, --help           show this help message and exit
  -v, --verbose        Show more logging messages
  -q, --quiet          Show fewer logging messages
```

## Notable Features

- Search Netbox instance

- Filter Netbox objects

- Create and update Netbox objects with YAML file

- Shell with preloaded pynetbox endpoints

    - Run scripts in shell environment

- Customizable table/detail views

- Extensible by adding custom commands

## Quick Start
