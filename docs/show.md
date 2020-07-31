# nbcli show

```
$ nbcli show -h
usage: nbcli show [-h] [-v] [-q] app_model args [args ...]

positional arguments:
  app_model      Model location to search (app.model)
  args           Search argumnets

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show more logging messages
  -q, --quiet    Show fewer logging messages

Show Detail view of object.

Usage Examples:

- Show Site with id 1
  $ nbcli show dcim.sites 1

- Show Device with name server01
  $ nbcli show dcim.devices name=server01

- Show Prefix 10.1.1.0/24
  $ nbcli show ipam.prefixes prefix=10.1.1.0/24
```
