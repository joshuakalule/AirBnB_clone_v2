#!/usr/bin/python3
"""
Script that generates a .tgz archive from the contents of web_static/

"""
from fabric.api import *
from pathlib import Path
import datetime


def do_pack():
    """ generate archive file (.tgz)"""
    source_dir = 'web_static'
    dest_dir = 'versions'

    if not Path(dest_dir).exists():
        local("mkdir versions", capture=True)

    now = datetime.datetime.now()
    suffix = now.strftime('%Y%m%d%H%M%S')
    archive_path = Path(dest_dir) / Path(f"{source_dir}_{suffix}.tgz")

    command = f"tar -czvf {archive_path} {source_dir}"
    print(f"Packing web_static to {archive_path}")
    result = local(command, capture=False)

    if result.succeeded:
        size = archive_path.stat().st_size
        print(f"web_static packed: {archive_path} -> {size}Bytes")
        return archive_path
    return None


if __name__ == "__main__":
    do_pack()
