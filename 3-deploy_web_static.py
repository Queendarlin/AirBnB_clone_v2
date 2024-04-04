#!/usr/bin/python3
"""
Fabric script to deploy an archive to web servers.
"""

from fabric.api import env, put, run
import os
from fabric.api import local
from datetime import datetime

# Define the list of web servers
env.hosts = ['18.204.16.143', '54.236.53.174']


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    # Get the current date and time as a string
    date_time_str = datetime.now().strftime('%Y%m%d%H%M%S')

    # Create the archive name based on current date and time
    archive_name = f'versions/web_static_{date_time_str}.tgz'

    # Compress the web_static folder into the archive
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -czvf {} web_static".format(archive_name)).failed is True:
        return None
    return archive_name


def do_deploy(archive_path):
    """
        Deploy an archive to the web servers.

        :param archive_path: (str) Path to the archive file to deploy.
        :return: True if deployment is successful, False otherwise.
    """

    # Check if the archive file exists
    if not os.path.exists(archive_path):
        print(f"Error: Archive file {archive_path} not found.")
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the filename without extension from the archive_path
        archive_filename = os.path.basename(archive_path).split('.')[0]

        # Create the folder for the new version
        run('mkdir -p /data/web_static/releases/{}'.format(archive_filename))

        # Uncompress the archive to the folder on the web server
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.format(
            archive_filename, archive_filename))

        # Delete the archive from the web server
        run('rm /tmp/{}.tgz'.format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version of your code
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_filename))

        print('New version deployed!')
        return True
    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
