#!/usr/bin/python3
"""Fabric script that distributes an archive to the web servers."""
from fabric.api import env, put, run
import os

env.hosts = ['23.23.29.130', '52.1.33.100']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distribute an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    no_ext = os.path.splitext(file_name)[0]
    release_path = "/data/web_static/releases/{}".format(no_ext)

    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}/".format(release_path))
        run("tar -xzf /tmp/{} -C {}/".format(file_name, release_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(release_path))
        return True
    except Exception:
        return False
