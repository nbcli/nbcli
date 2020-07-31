# nbcli pynb

```
$ nbcli pynb -h
usage: nbcli pynb [-h] [-v] [-q] [--view {table,detail,json}]
                  [--view-model VIEW_MODEL] [--cols [COLS [COLS ...]]] [--nh]
                  [-D | -u UD-ARGS [UD-ARGS ...] | --de DE DE-METHOD]
                  [--dea [DE-ARGS [DE-ARGS ...]]]
                  endpoint method [args [args ...]]

positional arguments:
  endpoint              App endpoint
  method                Endpoint Method
  args                  Argumnet to pass to func

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
  -D, --delete          Delete Object retrieved by get method
  -u UD-ARGS [UD-ARGS ...], --update UD-ARGS [UD-ARGS ...]
                        Update object with given kwargs
  --de DE DE-METHOD, --detail-endpoint DE DE-METHOD
                        Get the detail endpoint of object
  --dea [DE-ARGS [DE-ARGS ...]], --de-args [DE-ARGS [DE-ARGS ...]]
                        Argumets to pass to the de-action
```
