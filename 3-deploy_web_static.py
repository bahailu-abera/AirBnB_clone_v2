#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents of web_static folder
"""

import os
from fabric.api import env, run, put, local
from datetime import datetime


# Web servers IP addresses
env.hosts = ['54.157.167.29', '18.235.255.184']
# SSH user
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(current_time)

    local("mkdir -p versions")
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not archive_path:
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_no_ext = archive_name.split('.')[0]

        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to /data/web_static/releases/<archive_no_ext>/
        run('mkdir -p /data/web_static/releases/{}'.format(archive_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_name, archive_no_ext))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_name))

        # Move the uncompressed files to the proper location
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'
            .format(archive_no_ext, archive_no_ext))

        # Remove the unnecessary directory
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_no_ext))

        # Delete the existing symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_no_ext))

        # Add the missing files to the current directory
        run('mv /data/web_static/current/0-index.html \
            /data/web_static/current/my_index.html')

        print("New version deployed!")
        return True

    except Exception:
        return False


def deploy():
    """
    Deploys the web server
    """
    path = do_pack()

    if not path:
        return False

    return do_deploy(path)
