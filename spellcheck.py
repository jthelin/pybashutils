#!/usr/bin/env python
"""
Ctrl \  to abort
"""
from subprocess import check_call
from pathlib import Path

MAXSIZE = 20e6  # [bytes]


def findtext(root, globext):
    if isinstance(globext, (Path, str)):
        globext = [globext]

    for e in globext:
        # in case "ext" is actually a specific filename
        e = Path(e).expanduser()
        if e.is_file():
            spellchk([e])
        else:  # usual case
            spellchk(Path(root).expanduser().rglob(str(e)))


def spellchk(flist):
    for f in flist:
        try:
            check_call(['aspell', 'check', str(f)])
        except Exception as e:  # catch-all for unexpected error
            print(f, e)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(
        description='searches for TEXT under DIR and echos back filenames')
    p.add_argument('glob', help='glob pattern', nargs='?',
                   default=['*.rst', '*.txt', '*.md', '*.tex'])
    p.add_argument('rdir', help='root dir to search', nargs='?', default='.')
    p.add_argument('-v', '--verbose', action='store_true')
    p = p.parse_args()

    try:
        findtext(p.rdir, p.glob)
    except KeyboardInterrupt:
        pass
