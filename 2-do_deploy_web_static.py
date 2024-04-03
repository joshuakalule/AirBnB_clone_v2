#!/usr/bin/python3
"""Distribute archive created to web-01 and web-02 servers"""
from fabric.api import env, put, run
from pathlib import Path

env.hosts = ['52.206.61.240', '54.144.158.52']
env.user = 'ubuntu'
env.key_filename = Path.home() / '.ssh' / 'school'


def do_deploy(archive_path):
    """Deploys archive."""
    if not Path(archive_path).exists():
        return False

    release_name = Path(archive_path).stem
    release_path = f"/data/web_static/releases/"

    try:
        put(archive_path, '/tmp/')

        run(f'sudo mkdir -p {release_path}{release_name}/')

        tar_path = f'/tmp/{archive_name}'
        dir_path = f'{release_path}{release_name}/'
        run(f'sudo tar -xzf {tar_path} -C {dir_path}')

        run(f'sudo rm /tmp/{archive_name}')

        sources = f'{release_path}{release_name}/web_static/*'
        dest_dir = f'{release_path}{release_name}/'
        run(f'sudo mv {sources} {dest_dir}')

        run(f'sudo rm -rf {release_path}{release_name}/web_static')

        run('sudo rm -rf /data/web_static/current')

        sym_link = f'{release_path}{release_name}'
        run(f'sudo ln -s {sym_link} /data/web_static/current')
        return True

    except Exception as e:
        return False
