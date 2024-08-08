#!/usr/bin/python3
# coding=utf-8

"""Usage: ensure_pkg_installed.py PKG...

Ensure listed packages are installed. if they are not, try install them using
apt-get.

If running in docker environment, auto clean apt-get update cache.

"""

import sys
import os
import subprocess
import glob

import apt


CACHE = None


def get_cache():
    global CACHE    # pylint: disable=global-statement
    if CACHE is None:
        CACHE = apt.Cache()
    return CACHE


def is_installed(pkg_name):
    cache = get_cache()
    if pkg_name not in cache:
        return False
    pkg = cache[pkg_name]
    return pkg.is_installed


class CommandRunner:
    """Run commands with sudo if necessary.

    """

    def __init__(self):
        self.is_root = os.getuid() == 0
        self._in_docker = None

    def in_docker(self):
        """Return True if running in docker or any CRI runtime.

        """
        if self._in_docker is None:
            with open('/proc/1/cgroup') as f:
                content = f.read()
            self._in_docker = 'docker' in content or 'kubepod' in content
        return self._in_docker

    def run(self, args):
        """Run commands using subprocess.call().

        If current user is not root, run commands with sudo.

        Args:
            args: a list of program name and arguments.

        """
        return subprocess.call(args if self.is_root else ["sudo"] + args)


def main():
    args = sys.argv[1:]
    pkgs_to_install = [pkg for pkg in args if not is_installed(pkg)]
    if not pkgs_to_install:
        return

    cr = CommandRunner()
    if cr.in_docker:
        cr.run(["apt-get", "update"])
        os.makedirs("/usr/share/man/man1")
        os.makedirs("/usr/share/man/man7")
    cr.run(["apt-get", "install", "-y",
            "--no-install-recommends", "--no-install-suggests"] +
           pkgs_to_install)
    if cr.in_docker:
        cr.run(["rm", "-rf"] + glob.glob("/var/lib/apt/lists/*"))


if __name__ == '__main__':
    main()
