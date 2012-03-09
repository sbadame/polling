#!/usr/bin/env python2.7

import os
import subprocess

usage = """usage: [mysql|memcache|solr|start|update]
    mysql:
    memcache:
    solr:
    start:
    update:
"""


def mysql():
    pass

def memcache():
    pass

def solr():
    pass

def django():
    pass

def start_app():
    pass

def update():
    out,err = run('git status')
    if not out.endswith("(working directory clean)\n"):
        print(out)
        error("Cannot update with dirty working directory. Commit or revert changes")
    out,err = run('git pull')

    if "CONFLICT" in out:
        error("Couldn't merge:\n%s" % out, err)

    if "VIRTUAL_ENV" not in os.environ or not os.environ["VIRTUAL_ENV"] or os.environ["VIRTUAL_ENV"] != "polling":
        error("You need to run 'workon polling'")

def error(msg, err=""):
    print(msg)
    print(err)
    sys.exit(-1)

def run(cmd):
    p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.communicate()


if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description='Does all of the ugly shell crap')
    parser.add_argument('program', choices=["update", "mysql", "memcache", "solr"])
    parser.add_argument('args', nargs='*')
    args = vars(parser.parse_args(sys.argv[1:]))
    if args["program"] in globals():
        globals()[args["program"]](*args['args'])


