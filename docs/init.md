# nbcli init

```
$ nbcli init -h
usage: nbcli init [-h] [-v] [-q]

Initialize nbcli.

Default confg directory location $HOME/.nbcli.d
After running edit $HOME/.nbcli.d/config.py with your credentials.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show more logging messages
  -q, --quiet    Show fewer logging messages

Create nbcli config directory and related files.

Example Usage:

- Initialize nbcli
  $ nbcli init
```

## Config Directory 

The default nbcli directory is `$HOME/.nbcli/` this can be changed by setting
the NBCLI_DIR to a new directory

```
export NBCLI_DIR=/path/to/alt/directory
```

Values defined in the pynetbox dict will be directly used to create the pynetbox
[api instance](https://pynetbox.readthedocs.io/en/latest/#api).  
at minimum 'url' and 'token' need to be set.

```
pynetbox = dict(
    url='http://localhost:8080',                        # your netbox url
    token='0123456789abcdef0123456789abcdef01234567')   # your API token
```

Values defined in the requests dict will be used to create a
[custom requests Session](https://pynetbox.readthedocs.io/en/latest/advanced.html#custom-sessions)

If you need to disable SSL verification add the following to the user_config.py file.
```
requests = dict(verify=False)
```
