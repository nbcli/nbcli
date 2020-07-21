from glob import glob

files = glob('initializers/*.yml')

for f in files:
    fh = open(f, 'r')
    lines = fh.readlines()
    fh.close()
    fh = open('nbcli_' + f, 'w')
    for line in lines:
        if line.startswith('# '):
            fh.write(line[2:])
        else:
            fh.write(line)
    fh.close()
