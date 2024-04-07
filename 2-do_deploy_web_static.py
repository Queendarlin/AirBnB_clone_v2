#!/usr/bin/python3
"""
Fabric script to deploy an archive to web servers.
"""

from fabric.api import env, put, run
from os.path import exists

# Define the list of web servers
env.hosts = ['18.204.16.143', '54.236.53.174']


def do_deploy(archive_path):
    """
        Deploy an archive to the web servers.

        :param archive_path: (str) Path to the archive file to deploy.
        :return: True if deployment is successful, False otherwise.
    """
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False
