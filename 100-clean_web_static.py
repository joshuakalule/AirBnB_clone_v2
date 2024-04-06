#!/usr/bin/python3
"""Deletes out-of-date archives."""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['100.26.17.58', '35.168.8.71']


def do_clean(number=0):
    """
    Remove outdated archives.
    Requires:
        number - number of latest archives to keep
    """
    try:
        number = int(number)
    except ValueError as ve:
        return False

    ret = helper(number, 'local', 'versions')
    ret = helper(number, 'remote', '/data/web_static/releases')
    return ret


def helper(number, system, path):
    """Helper function to execute commands."""
    if system == 'remote':
        ls = run(f"ls -1 {path}")
    else:
        ls = local(f"ls -1 {path}", capture=True)

    if ls.failed:
        return False

    ls_list = [_f.strip() for _f in ls.split("\n") if _f]
    files = dict()
    for f in ls_list:
        dt_str = f.split('.')[0].split('_')[-1]
        dt = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
        files[f] = dt

    sorted_dts = sorted(files.values())
    if len(sorted_dts) == 0:
        return True

    remove = list()
    if number in [0, 1]:
        remove.extend(sorted_dts[1:])
    elif number:
        for n, dt in enumerate(sorted_dts):
            if n >= number:
                remove.append(dt)

    remove_str = ''
    for k, v in files.items():
        if v in remove:
            remove_str += f"{k} "
    if len(remove_str.strip()) == 0:
        return True

    if system == 'remote':
        run(f"cd {path}; sudo rm -rf {remove_str}")
    else:
        local(f"cd {path}; sudo rm -rf {remove_str}")
    return True
