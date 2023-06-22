#!/usr/bin/python3
"""Fabric script for deploying the web_static content to servers"""
from fabric.api import env, put, run
import os
from datetime import datetime

env.hosts = ['54.82.5.102', '3.94.103.18']
env.user = 'ubuntu'


def do_pack():
    """Create a compressed archive of the web_static folder"""
    try:
        time_format = "%Y%m%d%H%M%S"
        current_time = datetime.utcnow().strftime(time_format)
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        if not os.path.exists("versions"):
            os.makedirs("versions")
        command = "tar -cvzf {} web_static".format(archive_path)
        local(command)
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(file_name)[0]
        remote_path = "/tmp/{}".format(file_name)
        releases_path = "/data/web_static/releases/{}/".format(name_no_ext)

        put(archive_path, remote_path)
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(remote_path, releases_path))
        run("rm {}".format(remote_path))

        # Add the three new lines
        run("rm -r {}/web_static/images/*".format(releases_path))
        run("rm -r {}/web_static/styles/*".format(releases_path))
        run("mv {}/web_static/* {}".format(releases_path, releases_path))

        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        return True
    except:
        return False

