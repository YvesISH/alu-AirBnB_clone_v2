#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers"""

import os
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists

env.hosts = ["54.226.54.247", "18.205.246.150"]
env.user = "ubuntu"
env.key = "~/.ssh/id_rsa"


def do_pack():
    """Create a .tgz archive from the web_static folder."""
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    archive_path = "versions/web_static_{}.tgz".format(time_stamp)
    local("tar -cvzf {} web_static".format(archive_path))
    if os.path.exists(archive_path):
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """Distribute the archive to web servers and deploy it."""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = "/data/web_static/releases/" + name
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(path_name))
        run('tar -xzf /tmp/{} -C {}/'.format(file_name, path_name))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(path_name, path_name))
        run("rm -rf {}/web_static".format(path_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(path_name))
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
