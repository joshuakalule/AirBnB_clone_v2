#!/usr/bin/python3
""" distributes an archive to your web servers, using the function do_deploy """
from fabric.api import *
import os


env.hosts = ['100.26.213.55', '54.236.45.113']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Deploys the provided archive to the web servers.

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print(f"Error: Archive file not found: {archive_path}")
        return False

    for server in env.hosts:
        try:
            print(f"Uploading archive to {server}: /tmp/{os.path.basename(archive_path)}")
            put(archive_path, "/tmp/")
        except Exception as e:
            print(f"Error uploading archive to {server}: {e}")
            return False

    for server in env.hosts:
        with settings(host_string=server):
            try:
                archive_filename = os.path.basename(archive_path)
                extract_dir = f"/data/web_static/releases/{archive_filename[:-4]}"
                run(f"mkdir -p {extract_dir}")
                run(f"tar -xzf /tmp/{archive_filename} -C {extract_dir}")

                run(f"rm /tmp/{archive_filename}")

                run(f"rm -rf /data/web_static/current")

                run(f"ln -s {extract_dir} /data/web_static/current")
                print(f"Successfully deployed to {server}")
            except Exception as e:
                print(f"Error deploying to {server}: {e}")
                return False

    return True
