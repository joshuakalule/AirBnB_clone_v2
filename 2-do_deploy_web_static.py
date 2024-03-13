#!/usr/bin/python3
"""Deploy archive created to web-01 and web-02 servers"""
from fabric.api import env, put, run
import os

env.hosts = ['100.26.213.55', '54.236.45.113']
env.user = 'ubuntu'
env.key_filename = os.path.expanduser('~/.ssh/school')


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

        run(f'mkdir -p {release_path}{release_name}/')
        run(f'tar -xzf /tmp/{archive_name} -C '
            f'{release_path}{release_name}/')

        run(f'rm /tmp/{archive_name}')

        run(f'mv {release_path}{release_name}/web_static/* '
            f'{release_path}{release_name}/')

        run(f'rm -rf {release_path}{release_name}/web_static')

        run('rm -rf /data/web_static/current')

        run(f'ln -s {release_path}{release_name} '
            f'/data/web_static/current')

    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False

    print("New version deployed!")
    return True
