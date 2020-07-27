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

General Options:
  -h, --help           show this help message and exit
  -v, --verbose        Show more logging messages
  -q, --quiet          Show fewer logging messages
```

## Notable Features

- [Search](https://github.com/ericgeldmacher/nbcli/blob/release/docs/search.md) Netbox instance from command line
- [Show](https://github.com/ericgeldmacher/nbcli/blob/release/docs/show.md) detail view of objects
- [pynb](https://github.com/ericgeldmacher/nbcli/blob/release/docs/pynb.md) Command line wrapper for pynetbox
- [Shell](https://github.com/ericgeldmacher/nbcli/blob/release/docs/shell.md) with preloaded pynetbox endpoints
    - Run scripts in shell environment.
- [Customizable](https://github.com/ericgeldmacher/nbcli/blob/release/docs/views.md) table/detail views
- [Extensible](https://github.com/ericgeldmacher/nbcli/blob/release/docs/commands.md) by adding custom commands

## Quickstart

```
$ pip install nbcli
$ nbcli init
Edit pynetbox 'url' and 'token' entries in user_config.yml:
        ~/.nbcli/user_config.yml
```

At the very minimum, you need to specify a url and token in the user_config.yml file

```yaml
pynetbox:
  url: http://localhost:8080
  token: 0123456789abcdef0123456789abcdef01234567
```

If you need to disable SSL verification, add (or uncomment) the following to your user_config.yml file. 

```yaml
requests:
  verify: false
```

More configuration options can be found [here](https://github.com/ericgeldmacher/nbcli/blob/release/docs/init.md).

## Testing

Instructions for setting up a test environment are [here](https://github.com/ericgeldmacher/nbcli/blob/release/docs/test-env.md).
