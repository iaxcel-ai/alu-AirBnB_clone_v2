#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_static folder."""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generate a .tgz archive from the contents of web_static."""
    now = datetime.now()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    if not os.path.exists("versions"):
        local("mkdir -p versions")

    result = local("tar -cvzf {} web_static".format(file_name))

    if result.failed:
        return None
    return file_name
