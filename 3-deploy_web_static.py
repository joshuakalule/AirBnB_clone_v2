#!/usr/bin/python3
""" create .tgz file and deploy away to server """
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['100.26.17.58', '35.168.8.71']


def deploy():
    """creates and deploys .tgz archive to remote servers"""
    source_dir = 'web_static'
    target_dir = 'versions'

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

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
    else:
        print("Failed to create the archive.")
        return False

    release_name = archive_name.split('.')[0]
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

    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False

    print("New version deployed!")
    return True
