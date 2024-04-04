#!/usr/bin/python3
"""Distributes an archive to your web servers."""
from fabric.api import run, local, put, env
from pathlib import Path

env.hosts = ['100.26.17.58', '35.168.8.71']


def do_deploy(archive_path):
    """Method to execte distribution."""

    if not Path(archive_path).exists():
        return False

    name = Path(archive_path).name
    name_no_ext = Path(archive_path).stem
    releases_path = "/data/web_static/releases/"
    current_path = "/data/web_static/current"
    dest_folder = Path(releases_path) / name_no_ext

    try:
        put(archive_path, "/tmp/", use_sudo=True)

        run(f"sudo rm -rf {dest_folder}")
        run(f"sudo mkdir -p {dest_folder}")
        run(f"sudo tar -xzf /tmp/{name} -C {dest_folder}")
        run(f"sudo rm /tmp/{name}")

        run(f"sudo mv {dest_folder}/web_static/* {dest_folder}")
        run(f"sudo rm -rf {dest_folder}/web_static")

        run(f"sudo rm -rf {current_path}")
        run(f"sudo ln -sf {dest_folder} {current_path}")

        print("New version deployed!")
        return True
    except Exception as e:
        print("Error: {}".format(e))

    return False
