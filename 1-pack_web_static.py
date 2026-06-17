#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_static folder."""
from fabric.api import local
from datetime import datetime
import os


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
