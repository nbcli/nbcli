```
nbcli shell -h
usage: nbcli shell [-h] [-v] [-q] [-i] [-s {python,ipython}] [--skip] [script]

Launch Interactive Shell with pynetbox objects preloaded.

positional arguments:
  script                Script to run

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show more logging messages
  -q, --quiet           Show fewer logging messages
  -i                    inspect interactively after running script
  -s {python,ipython}, --interactive-shell {python,ipython}
                        Specifies interactive shell to use
  --skip                Skip loading models.

Run Shell enviornment.

Example usage:
$ nbcli shell -i myscript.py
$ nbcli shell -s python
```
