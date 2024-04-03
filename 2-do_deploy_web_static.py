#!/usr/bin/python3
"""Distribute archive created to web-01 and web-02 servers"""
from fabric.api import env, put, run
import os

env.hosts = ['52.206.61.240', '54.144.158.52']
env.user = 'ubuntu'
env.key_filename = os.path.expanduser('~/.ssh/server_rsa')


def do_deploy(archive_path):
    """
    Function to deploy archive.

    Returns: False if archive_path does not exist.
    """
    if not os.path.exists(archive_path):
        print(f"The file at the path {archive_path} does not exist.")
        return False

    archive_name = os.path.basename(archive_path)
    release_name = os.path.splitext(archive_name)[0]
    release_path = f"/data/web_static/releases/"

    try:
        put(archive_path, '/tmp/')

        run(f'sudo mkdir -p {release_path}{release_name}/')
        run(f'sudo tar -xzf /tmp/{archive_name} -C '
            f'{release_path}{release_name}/')

        run(f'sudo rm /tmp/{archive_name}')

        run(f'sudo mv {release_path}{release_name}/web_static/* '
            f'{release_path}{release_name}/')

        run(f'sudo rm -rf {release_path}{release_name}/web_static')

        run('sudo rm -rf /data/web_static/current')

        run(f'sudo ln -s {release_path}{release_name} '
            f'/data/web_static/current')
        print("New version deployed!")
        return True

    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False
