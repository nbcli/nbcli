# nbcli filter

```
$ nbcli filter -h
usage: nbcli filter [-h] [-v] [-q] [--view {table,detail,json}]
                    [--view-model VIEW_MODEL] [--cols [COLS [COLS ...]]]
                    [--nh] [-g] [-c | -D | -u UD-ARGS [UD-ARGS ...]]
                    [--de DE-ARGS [DE-ARGS ...]]
                    model [args [args ...]]

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
  -g, --get             Get single result. Raise error if more are returned
  -c, --count           Return the count of objects in filter.
  -D, --delete          Delete Object(s) retrieved by get method
  -u UD-ARGS [UD-ARGS ...], --update UD-ARGS [UD-ARGS ...]
                        Update object(s) with given kwargs
  --de DE-ARGS [DE-ARGS ...], --detail-endpoint DE-ARGS [DE-ARGS ...]
                        List results from detail endpoint With optional kwargs
```
