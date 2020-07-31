# NetBox Client

Extensible command-line interface for Netbox using pynetbox module. 

[![asciicast](https://asciinema.org/a/348204.svg)](https://asciinema.org/a/348204)

## Notable Features

- [init](https://nbcli.readthedocs.io/en/release/init.html)
- [search](https://nbcli.readthedocs.io/en/release/nbsearch.html)
- [show](https://nbcli.readthedocs.io/en/release/show.html)
- [pynb](https://nbcli.readthedocs.io/en/release/pynb.html)
- [shell](https://nbcli.readthedocs.io/en/release/shell.html)

## Extend and Customize

- [Views](https://nbcli.readthedocs.io/en/release/views.html)
- [Commands](https://nbcli.readthedocs.io/en/release/commands.html)

## Quickstart

The full nbcli documentation on [Read the Docs](https://nbcli.readthedocs.io/en/release/)

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

## Basic Usage



## Testing

Instructions for setting up a test environment are [here](https://nbcli.readthedocs.io/en/release/test-env.html).
