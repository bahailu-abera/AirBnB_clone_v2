#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

import os
from datetime import datetime
from fabric.api import env, run, put

# Web servers IP addresses
env.hosts = ['54.157.167.29', '18.235.255.184']
# SSH user
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]

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

        print("New version deployed!")
        return True

    except Exception:
        return False
