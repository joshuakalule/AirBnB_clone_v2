#!/usr/bin/python3
"""deploy archive created to web-01 and web-02 servers"""
from fabric.api import env, local, put, run
from fabric.operations import exists
import os
import sys

env.hosts = ['100.26.213.55', '54.236.45.113']


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

    put(archive_path, '/tmp/')

    run(f'mkdir -p {release_path}{release_name}')
    run(f'tar -xzf /tmp/{archive_name} -C {release_path}{release_name}/')

    run(f'rm /tmp/{archive_name}')

    run('rm -rf /data/web_static/current')

    run(f'ln -s {release_path}{release_name}/ /data/web_static/current')

    print("New version deployed!")
    return True


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg.startswith('archive_path='):
            archive_path = arg.split('=')[1]
            break
        else:
            print("The archive_path argument was not provided.")
            return False
    if do_deploy(archive_path):
        print("Deployment successful.")
    else:
        print("Deployment failed.")
