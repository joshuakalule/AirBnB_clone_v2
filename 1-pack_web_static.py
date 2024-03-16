#!/usr/bin/python3
"""
script that generates a .tgz archive from the contents of web_static/

"""
from fabric.api import *
from datetime import datetime
import os


def do_pack():
    """ generate archive file (.tgz)"""
    source_dir = 'web_static'
    target_dir = 'versions'

    if not os.path.exists(target_dir):
        local("mkdir -p versions")

    now = datetime.now()
    formatted_now = now.strftime('%Y%m%d%H%M%S')

    archive_name = f"{source_dir}_{formatted_now}.tgz"
    archive_path = os.path.join(target_dir, archive_name)

    command = f"tar -czvf {archive_path} {source_dir}/"

    print(f"Packing web_static to {archive_path}")
    result = local(command, capture=False)

    if result.succeeded:
        mode_cmd = f"chmod 664 {archive_path}"
        mode_result = local(mode_cmd, capture=True)
        os_path = os.path.getsize(archive_path)
        print(
            f"web_static packed: {archive_path} -> {os_path}Bytes")
        return archive_path
    else:
        print("Failed to create the archive.")
        return None


if __name__ == "__main__":
    do_pack()
