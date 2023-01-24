# nbcli: NetBox Command-line Client

Extensible command-line interface for [Netbox](https://netbox.readthedocs.io/en/stable/) 
using the [pynetbox](https://pynetbox.readthedocs.io/en/latest/) module. 

***nbcli is still in development!*** 
***Syntax of commands are subject to change!***

[![asciicast](https://asciinema.org/a/525610.svg)](https://asciinema.org/a/525610)

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
$ nbcli search dmi01

Device
======
Name                    Status  Tenant                Site           Rack          Role           Type         IP Address
dmi01-akron-pdu01       Active  Dunder-Mifflin, Inc.  DM-Akron       Comms closet  PDU            AP7901       -
dmi01-akron-rtr01       Active  Dunder-Mifflin, Inc.  DM-Akron       Comms closet  Router         ISR 1111-8P  -
dmi01-akron-sw01        Active  Dunder-Mifflin, Inc.  DM-Akron       Comms closet  Access Switch  C9200-48P    -
dmi01-albany-pdu01      Active  Dunder-Mifflin, Inc.  DM-Albany      Comms closet  PDU            AP7901       -
dmi01-albany-rtr01      Active  Dunder-Mifflin, Inc.  DM-Albany      Comms closet  Router         ISR 1111-8P  -
dmi01-albany-sw01       Active  Dunder-Mifflin, Inc.  DM-Albany      Comms closet  Access Switch  C9200-48P    -
dmi01-binghamton-pdu01  Active  Dunder-Mifflin, Inc.  DM-Binghamton  Comms closet  PDU            AP7901       -
dmi01-binghamton-rtr01  Active  Dunder-Mifflin, Inc.  DM-Binghamton  Comms closet  Router         ISR 1111-8P  -
dmi01-binghamton-sw01   Active  Dunder-Mifflin, Inc.  DM-Binghamton  Comms closet  Access Switch  C9200-48P    -
dmi01-buffalo-pdu01     Active  Dunder-Mifflin, Inc.  DM-Buffalo     Comms closet  PDU            AP7901       -
dmi01-buffalo-rtr01     Active  Dunder-Mifflin, Inc.  DM-Buffalo     Comms closet  Router         ISR 1111-8P  -
dmi01-buffalo-sw01      Active  Dunder-Mifflin, Inc.  DM-Buffalo     Comms closet  Access Switch  C9200-48P    -
dmi01-camden-pdu01      Active  Dunder-Mifflin, Inc.  DM-Camden      Comms closet  PDU            AP7901       -
dmi01-camden-rtr01      Active  Dunder-Mifflin, Inc.  DM-Camden      Comms closet  Router         ISR 1111-8P  -
dmi01-camden-sw01       Active  Dunder-Mifflin, Inc.  DM-Camden      Comms closet  Access Switch  C9200-48P    -
*** See all 39 results: '$ nbcli filter device dmi01 --dl' ***
```
