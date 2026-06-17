#!/usr/bin/python3
"""Fabric script that distributes an archive to the web servers."""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['23.23.29.130', '52.1.33.100']
env.user = 'ubuntu'


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
