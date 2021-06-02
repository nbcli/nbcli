import os
from pathlib import Path

source_path = Path('initializers')
dest_path = Path('nbcli_initializers')

if not (source_path.exists() and source_path.is_dir()):
    raise RuntimeError('source_path does not exist or is not a directory')

dest_path.mkdir(exist_ok=True)

for f in os.listdir(source_path):
    sfh = open(source_path.joinpath(f), 'r')
    dfh = open(dest_path.joinpath(f), 'w')

    for line in sfh.readlines():
        if line.startswith('# '):
            dfh.write(line[2:])

    sfh.close()
    dfh.close()
