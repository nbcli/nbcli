# nbcli filter

```
$ nbcli filter -h
usage: nbcli filter [-h] [-v] [-q] [--json | --detail] [--view VIEW]
                    [--cols [COLS [COLS ...]]] [--nh] [--dl]
                    [-a | -c | -D | --ud [UD [UD ...]]] [--de [DE [DE ...]]]
                    [--pre PRE]
                    model [args [args ...]]

Filter Netbox objects by searchterm and object properties.

Optionally update and delete objects returned by the filter.
Control output view and listed columns.

positional arguments:
  model                 NetBox model.
  args                  Argument(s) to filter results.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show more logging messages
  -q, --quiet           Show fewer logging messages
  --json                Display results as json string.
  --detail              Display more detailed info for results.
  --view VIEW           View model to use
  --cols [COLS [COLS ...]]
                        Custom columns for table output.
  --nh, --no-header     Disable header row in results
  --dl, --disable-limit
                        Disable limiting number of results returned.
  -a, --all             List all object from endpoint.
  -c, --count           Return the count of objects in filter.
  -D, --delete          Delete Object(s) returned by filter. [WIP]
  --ud [UD [UD ...]], --update [UD [UD ...]]
                        Update object(s) returned by filter with given kwargs. [WIP]
  --de [DE [DE ...]], --detail-endpoint [DE [DE ...]]
                        List results from detail endpoint With optional kwargs. [WIP]
  --pre PRE, --stdin-prefix PRE
                        Prefix to add to stdin args.

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

!!! note
    The `filter` command will limit the number of returned results to 50 by default.
    Adding the `--dl` argument will return all results.

    The default can be changed in the `user_config.yml` file by editing the value for `filter_limit`.
    ```
        nbcli:
          filter_limit: 50
    ```

    This feature can be overridden completely by setting `filter_limit` to `0`

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
    For most object types, the  value after the `:`, is applyed to the key `name`.  
    You can override this behavior by inserting a keyword argument after the `:`  
    The following command should return all devices in racks with the status `reserved`:
    ```
    nbcli filter device rack:status=reserved
    ```

## Compound-resolve arguments [WIP]

Any argument containing a `::` will be considered a compound-resolve argument
in the form of `object::object:name`.

Compound-resolve arguments take the concept of auto-resolve further, by allowing
you to apply an auto-resolve to an auto-resolve. This allows you to put more
precise constraints on your auto-resolve arguments.

For instance you can list interfaces matching the search term 'eth' only on
devices in rack 1.1.

```
nbcli filter interface eth device::rack:1.1
```


## Modifying results

Results from the filter can be updated or deleted. You will always be prompted
to confirm when updating or deleting.

### Updating

Update objects returned by filter.
Values can be updated with keyword arguments and/or auto-resolve arguments.

```
$ nbcli filter rack tenant:ENCOM --ud status=reserved 'site:NY DC-1'
Update Racks with {'status': 'reserved', 'site': 2}?
* 1.1 (1)
* 1.2 (2)
(yes) to update: yes
1.1 (1) Updated!
1.2 (2) Updated!
```

### Deleting

Delete objects returned by filter.

```
$ nbcli filter device db -D
Delete Devices?
* db-1 (5)
* db-2 (6)
(yes) to delete: yes
db-1 (5) Deleted!
db-2 (6) Deleted!
```

## Detail Endpoint

pynetbox [DetailEndpoint](https://pynetbox.readthedocs.io/en/latest/endpoint.html#pynetbox.core.endpoint.DetailEndpoint)
objects can be access with the `--de` flag.

```
nbcli filter prefix 192.168.1.0/24 --de available_ips
```

## Controlling output

The following optional arguments can change how the results of the filter
command are displayed.

```
  --json                Display results as json string.
  --detail              Display more detailed info for results.
  --view VIEW           View model to use
  --cols [COLS [COLS ...]]
                        Custom columns for table output.
  --nh, --no-header     Disable header row in results
```

### --json

Display results as json string. Output should be similar (but may not be
exactly the same) as the contents from the `results` field when accessing the
Netbox API directly.

### --detail  

Display more detailed info for results.


### ---view

Override the default view model for the given object types with one defined by
a [User Custom View](../extend/views.md) or extention, by specifying it's Class
name.

```
nbcli filter device rack:1.1 --view MyDevicesView
```

### --cols

Specify object attributes to display in table view.

```
$ nbcli filter device tenant:ENCOM --cols name rack position device_type
name         rack  position  device_type
chassis-1    1.2   1         A-2U-C
compute-1    1.2   -         A-BL-S
compute-2    1.2   -         A-BL-S
compute-3    1.2   -         A-BL-S
compute-4    1.2   -         A-BL-S
web-1        1.1   2         A-1U-S
web-2        1.1   3         A-1U-S
web-3        1.1   4         A-1U-S
web-proxy-1  1.1   1         A-1U-S
```

!!! tip
    Looking at the json view will give you some insite on what attribues are
    available for a given object type.
    ```
    $ nbcli filter device compute-1 --json | jq
    ```
    or
    ```
    $ nbcli filter device compute-1 --json | python3 -m json.tool
    ```

If the attribute is an instance of another object type, you can `drill into`
that object to grab it's attributes

```
$ nbcli filter device tenant:ENCOM --cols name rack position parent_device parent_device.position parent_device.device_bay
name         rack  position  parent_device  parent_device.position  parent_device.device_bay
chassis-1    1.2   1         -              -                       -
compute-1    1.2   -         chassis-1      1                       1
compute-2    1.2   -         chassis-1      1                       2
compute-3    1.2   -         chassis-1      1                       3
compute-4    1.2   -         chassis-1      1                       4
web-1        1.1   2         -              -                       -
web-2        1.1   3         -              -                       -
web-3        1.1   4         -              -                       -
web-proxy-1  1.1   1         -              -                       -
```

`--cols` should fail gracefully, so if the attribute does not exist, or is
null, or and empty string the value will be displayed as an `-`

```
$ nbcli filter device tenant:ENCOM --cols name bad_attr bad_attr.child_attr
name         bad_attr  bad_attr.child_attr
chassis-1    -         -
compute-1    -         -
compute-2    -         -
compute-3    -         -
compute-4    -         -
web-1        -         -
web-2        -         -
web-3        -         -
web-proxy-1  -         -
```

### --nh, --no-header

Allows you to remove the header row in the table view.
(Useful for when piping to another shell command.)
