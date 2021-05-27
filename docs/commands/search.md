# nbcli search

```
$ nbcli search -h
usage: nbcli search [-h] [-v] [-q] [obj_type] searchterm

Search Netbox objects with the given searchterm.

The List of search objects can be modified in:
$CONF_DIR/user_config.yml

positional arguments:
  obj_type       Object type to search
  searchterm     Search term

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show more logging messages
  -q, --quiet    Show fewer logging messages

Run a search of Netbox objects and show a table view of results.

Usage Examples:

- Search all object types for 'server1':
  $ nbcli search server1

- Search the interface object type for 'eth 1':
  $ nbcli search interface 'eth 1'
```

The `search` command is designed to emulate the main search bar that can be found
at the top of the home page of the Netbox web interface.

By default it will search through a predefined list of object types and return
up to 15 results for each object type. If more then 15 results are found, it
will display the filter command to show all the results.

If your search term needs to contain a space, make sure to wrap it in quotes.

```
nbcli search 'web server'
```

If you only want to search one object type you can specify if before the search
term. `nbcli search [obj_type] searchterm`.

* Searching all object types for `server1`:

    ```
    nbcli search server1
    ```

* Searching only devices for `server1`:

    ```
    nbcli search device server1
    ```

The list of predefined object types that will be searched can be modified by
editing the [user_config.yml](../init/#config-file) file.

```yaml
nbcli:
#  search_objects:
#    - provider
#    - circuit
#    - site
#    - rack
#    - rack_group
#    - device_type
#    - device
#    - virtual_chassis
#    - cable
#    - power_feed
#    - vrf
#    - aggregate
#    - prefix
#    - address
#    - vlan
#    - secret
#    - tenant
#    - cluster
#    - virtual_machine
```

!!! info
    `nbcli search` relies on the `q` perameter being available for the GET
    method on the REST API endpoint. Make sure any object added to the
    `search_objects` list has the `q` perameter available for the GET method.

    Your Netbox instance API docs should be available at 
    https://your.netbox.url/api/docs
