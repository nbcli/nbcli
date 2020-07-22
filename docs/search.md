```
$ nbcli search -h
usage: nbcli search [-h] [-v] [-q] [app_model] searchterm

Search Netbox objects with the given searchterm.

The List of search models can be modified in:
$HOME/$CONF_DIR/config.py

positional arguments:
  app_model      Model location to search (app.model)
  searchterm     Search term

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show more logging messages
  -q, --quiet    Show fewer logging messages

Run a search of Netbox objects and show a table view of results.

Usage Examples:

- Search all search modelss for 'server1':
  $ nbcli search server1

- Search the dcim.interfaces model for 'eth 1':
  $ nbcli search dcim.interfaces 'eth 1'
```
