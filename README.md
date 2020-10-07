# nbcli NetBox Command-line Client

Extensible command-line interface for [Netbox](https://netbox.readthedocs.io/en/stable/) 
using the [pynetbox](https://pynetbox.readthedocs.io/en/latest/) module. 

***nbcli is still in development!*** 
***Syntax of commands are subject to change!***


[![asciicast](https://asciinema.org/a/348204.svg)](https://asciinema.org/a/348204)

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

## Core Commands

- [init](docs/commands/init.rst)
- [search](docs/commands/nbsearch.rst)
- [filter](docs/commands/filter.rst)
- [shell](docs/commands/shell.rst)

## Extend and Customize

- [Views](docs/extend/views.rst)
- [Commands](docs/extend/commands.rst)

## Testing

Instructions for setting up a test environment are [here](docs/test-env.rst).

## Basic Usage

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

Show device with id 2.

```
$ nbcli show dcim.devices 2
server02
========

Device
------
Site:   AMS 2
Rack:   rack-02
Position:       2
Tenant: None
Device Type:    Other
Serial Number:
Asset Tag:      None

Management
----------
Role:   None
Platform:       None
Status: Active
Primary IPv4:   None
Primary IPv6:   None

Custom Fields
-------------
select_field:   None
select_field_auto_weight:       None
boolean_field:  None
date_field:     None
text_field:     Description

Tags
----


Comments
--------


Interfaces
----------
Name         LAG  Description  MTU  Mode  Cable  Connection
to-server01  -    -            -    -     -      -           -
```

Show Prefix 10.1.1.0/24

```
$ nbcli show ipam.prefixes prefix=10.1.1.0/24
id: 1
family: IPv4
prefix: 10.1.1.0/24
site: AMS 1
vrf: None
tenant: tenant1
vlan: vlan1
status: Active
role: None
is_pool: False
description: prefix1
tags: []
custom_fields: {'text_field': None}
created: 2020-07-31
last_updated: 2020-07-31T21:09:11.947263Z
```

List all IP Addresses with pynb (pynetbox wrapper)

```
$ nbcli pynb ipam.ip_addresses all
ID  IP Address              Vrf   Status    Role  Tenant   Parent    Interface    DNS Name  Description
1   10.1.1.1/24             vrf1  Active    -     -        server01  to-server02  -         -
3   10.1.1.2/24             -     Active    -     -        server02  to-server01  -         -
5   10.1.1.10/24            -     Reserved  -     tenant1  -         -            -         reserved IP
2   2001:db8:a000:1::1/64   vrf1  Active    -     -        server01  to-server02  -         -
4   2001:db8:a000:1::2/64   -     Active    -     -        server02  to-server01  -         -
6   2001:db8:a000:1::10/64  -     Reserved  -     tenant1  -         -            -         reserved IP
```
