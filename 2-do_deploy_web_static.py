#!/usr/bin/python3
"""deploy archive created to web-01 and web-02 servers"""
from fabric.api import env, local, put, run
import os
import sys

env.hosts = ['100.26.213.55', '54.236.45.113']
env.user = 'ubuntu'
env.key_filename = os.path.expanduser('~/.ssh/school')


def do_deploy(archive_path):
    """
    function to deploy archive

    Returns: False if archive_path does not exist
    """
    if not os.path.exists(archive_path):
        print("The file at the path does not exist.")
        return False

    archive_name = os.path.basename(archive_path)
    release_name = os.path.splitext(archive_name)[0]
    release_path = f"/data/web_static/releases/"

    try:
        put(archive_path, '/tmp/')

        run(f'sudo mkdir -p {release_path}{release_name}')
        run(f'sudo tar -xzf /tmp/{archive_name} -C\
        {release_path}{release_name}/')

        run(f'sudo rm /tmp/{archive_name}')

        run('sudo rm -rf /data/web_static/current')

        run(f'sudo ln -s {release_path}{release_name}/\
        /data/web_static/current')
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    print("New version deployed!")
    return True
