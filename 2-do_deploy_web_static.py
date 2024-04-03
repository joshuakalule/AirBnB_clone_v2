#!/usr/bin/python3
"""Distribute archive created to web-01 and web-02 servers"""
from fabric.api import env, put, run, env, hosts
import os

env.hosts = ['52.206.61.240', '54.144.158.52']


def do_deploy(archive_path):
    """deploy tarball on server"""
    a_list = archive_path.split("/")
    filename = a_list[-1]
    extension_list = filename.split(".")
    no_extension = extension_list[0]
    exists = os.path.isfile('{}'.format(archive_path))
    if not exists:
        return False
    try:
        put(archive_path, "/tmp/")
        run("rm -rf /data/web_static/releases/")
        run("mkdir -p /data/web_static/releases/" + no_extension)
        run("tar xzf /tmp/" + filename + " -C " +
            "/data/web_static/releases/" + no_extension)
        run("rm -f /tmp/" + filename)
        run("unlink /data/web_static/current")
        run("ln -s /data/web_static/releases/" + no_extension +
            " /data/web_static/current")
        run("mv -f /data/web_static/releases/" +
            no_extension + "/web_static/* /data/web_static/releases/" +
            no_extension)
        return True
    except Exception:
        return False
