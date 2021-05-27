# nbcli filter

```
$ nbcli filter -h
usage: nbcli filter [-h] [-v] [-q] [--view {table,detail,json}]
                    [--view-model VIEW_MODEL] [--cols [COLS [COLS ...]]] [--nh]
                    [-c | -D | --ud [UD [UD ...]]] [--de [DE [DE ...]]]
                    model [args [args ...]]

Filter Netbox objects by searchterm and object properties.

Optionally update and delete objects returned by the filter.
Control output view and listed columns.

positional arguments:
  model                 NetBox model
  args                  Argumnet(s) to filter results.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show more logging messages
  -q, --quiet           Show fewer logging messages
  --view {table,detail,json}
                        Output view.
  --view-model VIEW_MODEL
                        View model to use
  --cols [COLS [COLS ...]]
                        Custome columns for table output.
  --nh, --no-header     Disable header row in results
  -c, --count           Return the count of objects in filter.
  -D, --delete          Delete Object(s) returned by filter [WIP]
  --ud [UD [UD ...]], --update [UD [UD ...]]
                        Update object(s) returned by filter with given kwargs [WIP]
  --de [DE [DE ...]], --detail-endpoint [DE [DE ...]]
                        List results from detail endpoint With optional kwargs [WIP]

Filter Netbox objects by a searchterm and object properties.

Usage Examples:

- Filter IP Addresses with searchterm '192.168.1.1':
  $ nbcli filter address 192.168.1.1

- Filter devices by serial number using keyword arguments:
  $ nbcli filter device serial=123456

- Filter devices types by manufacturer using auto-resolve arguments:
  $ nbcli filter device_type manufacturer:ACME

- Update tenant on devices returned by filter:
  $ nbcli filter device name=server1 -ud tenant:tenant2

- Delete IP addresses returned by filter:
  $ nbcli filter address 192.168.1.1 -D
```

The `filter` command is designed to emulate the "list view" of the Netbox web
interface. Results can be refined with a search term, keyword,
"auto-resolve", and "compound-resolve" arguments.

Objects returned by the filter can optionally updated or deleted.

## Basic usage

The simplest way to use the `filter` command is just to pass a search term.
Any argument not containing an `=` or `:` will be considered a search term
argument.

```
nbcli filter device webserver
```

Multiple search terms can be passed to the `filter` command, but only the first
will be used. If your search term needs to contain a space, make sure to wrap
it in quotes.

```
nbcli filter device 'web server'
```

Search term arguments can be mixed and matched with any combination of keyword,
auto-resolve, and compound-resolve arguments to refine your filter.

## Keyword arguments

Any argument containing an `=` will be considered a keyword argument in the
form of `key=value`. 

```
nbcli filter device serial=123456
```

!!! note
    Keyword arguments are passed to the given REST API endpoint via
    [pynetbox](https://pynetbox.readthedocs.io/en/latest/endpoint.html#pynetbox.core.endpoint.Endpoint.filter)
    so a familiarity with the Netbox's REST API will help.  
    You can find your Netbox instances API docs at https://your.netbox.url/api/docs  
    You may also want to have a look at 
    [Netbox's Documentation](https://netbox.readthedocs.io/en/stable/rest-api/filtering/)
    on REST API Filtering

Multiple keyword arguments can be passed to the `filter` command and all will
be used to refine the filter.

```
nbcli filter address parent=192.168.1.0/24 status=reserved
```

Some keyword arguments can be "stacked" where multiple values can be passed for
the same key. (This only applies if it is supported by the given parameter of
the REST API endpoint.)

```
nbcli filter address status=dhcp status=reserved
```


## Auto-resolve arguments [WIP]

Any argument containing a `:` will be considered an auto-resolve argument in
the form of `object:name`.

The following will list all devices in rack 1.1

```
nbcli filter device rack:1.1
```

These can also be combined to refine the filter.

```
nbcli filter device rack:1.1 device_type:R840
```

And stacked to include more results

```
nbcli filter device rack:1.1 rack:1.2
nbcli filter device rack:1.1:1.2
```

!!! note
    Behind the sceans, auto-resolve arguments are essantally running another
    `filter` command and passing the `id` values of the results as to the main
    `filter` command.  
    So `nbcli filter device rack:1.1` is running:
    ```
    nbcli filter rack name=1.1
    ```
    and then modifying the origenal `filter` command to be:
    ```
    nbcli filter device rack_id=1
    ```
    For most object types value after the `:`, is applyed to the key `name`.  
    You can override this behavior by inserting a keyword argument after the `:`  
    The following command should return all devices in racks with the status `reserved`:
    ```
    nbcli filter device rack:status=reserved
    ```

## Compound-resolve arguments [WIP]


## Updating and Deleting [WIP]


## Controlling output

The following optional arguments can change how the results of the filter
command are displayed.

```
  --view {table,detail,json}
                        Output view.
  --view-model VIEW_MODEL
                        View model to use
  --cols [COLS [COLS ...]]
                        Custome columns for table output.
  --nh, --no-header     Disable header row in results
```

### --view


### ---view-model


### --cols


### --nh, --no-header
