#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""
from fabric.api import env
from fabric.api import put, run
import os
from datetime import datetime

env.hosts = ['23.23.29.130', '52.1.33.100']
env.user = 'ubuntu'


def do_pack():
    """Generate a .tgz archive from the contents of web_static."""
    from fabric.api import local
    now = datetime.now()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    if not os.path.exists("versions"):
        local("mkdir -p versions")

    result = local("tar -cvzf {} web_static".format(file_name))

    if result.failed:
        return None
    return file_name


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


def deploy():
    """Create and distribute an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
