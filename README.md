# NetBox Client

Extensible command-line interface for Netbox using pynetbox module. 


```
$ pip install nbcli
$ nbcli init
Edit pynetbox 'url' and 'token' entries in user_config.py:
        ~/.nbcli/user_config.py

```

```
$ nbcli -h
usage: nbcli [-h] <command> ...

Run main cli app with sys.argv from command line.

optional arguments:
  -h, --help  show this help message and exit

Commands:
  <command>
    init      Initialize nbcli.
    search    Search Netbox Objects
    show      Show detail view of Netbox Object
    shell     Launch interactive shell
    pynb      Wrapper for pynetbox
    lsmodels  List Netbox Models
    hello     Say hello

General Options:
  -h, --help           show this help message and exit
  -v, --verbose        Show more logging messages
  -q, --quiet          Show fewer logging messages
```
