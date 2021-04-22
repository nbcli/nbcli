# nbcli create

```
$ nbcli create -h
usage: nbcli create [-h] [-v] [-q] [--dr] [-u] file

Create and/or Update objects defined in YAML file.

positional arguments:
  file               YAML file.

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      Show more logging messages
  -q, --quiet        Show fewer logging messages
  --dr, --dry-run    Dry run.
  -u, --update-only  Do not create object not found with the lookup key schema.

Run command.

See documentation for YAML file reference and examples.
https://nbcli.readthedocs.io/en/release/create.html

Usage Examples:

- Create/Update objects defined in YAML file
  $ nbcli create file.yml
``` 
