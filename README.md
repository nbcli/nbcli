# nbcli NetBox Command-line Client

Extensible command-line interface for [Netbox](https://netbox.readthedocs.io/en/stable/) 
using the [pynetbox](https://pynetbox.readthedocs.io/en/latest/) module. 

***nbcli is still in development!*** 
***Syntax of commands are subject to change!***


[![asciicast](https://asciinema.org/a/348204.svg)](https://asciinema.org/a/348204)

## Quickstart

The full nbcli documentation can be found [here](https://ericgeldmacher.github.io/nbcli/).

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

Run a search of Netbox objects and show a table view of results.

```
$ nbcli search server

dcim.devices
============
ID  Name      Status  Tenant  Site    Rack     Role    Type   IP Address
1   server01  Active  -       AMS 1   rack-01  server  Other  -
2   server02  Active  -       AMS 2   rack-02  server  Other  -
3   server03  Active  -       SING 1  rack-03  server  Other  -

```
