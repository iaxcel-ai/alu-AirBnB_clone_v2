#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists

env.hosts = ['23.23.29.130', '52.1.33.100']
env.user = 'ubuntu'


def do_pack():
    """Generate a .tgz archive from the contents of web_static.

    Returns:
        str: path of the archive if successful, None otherwise.
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute an archive to the web servers.

    Args:
        archive_path (str): path to the archive to deploy.

    Returns:
        bool: True if all operations succeeded, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split('/')[-1]
        no_ext = file_name.split('.')[0]
        release = "/data/web_static/releases/{}".format(no_ext)

        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}/".format(release))
        run("tar -xzf /tmp/{} -C {}/".format(file_name, release))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(release, release))
        run("rm -rf {}/web_static".format(release))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute an archive to the web servers.

    Returns:
        bool: True if deploy succeeded, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
