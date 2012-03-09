#!/usr/bin/env python2.7

import os
import subprocess
import sys

usage = """usage: [mysql|memcache|solr|start|update]
    mysql:
    memcache:
    solr:
    start:
    update:
"""


def mysql():
    pass

def memcached():
    out, err = run("memcached")
    if out or err:
        error("memcached: %s" % out, err)

def solr():
    out, err = run("java -jar start.jar", waitFor="Started", cwd="solr/example")

def django():
    pass

def start_app():
    mysql()
    memcached()
    solr()
    django()

def update():
    out,err = run('git status')
    if not out.endswith("(working directory clean)\n"):
        error("Cannot update with dirty working directory. Commit or revert changes")

    out,err = run('git pull')

    if "CONFLICT" in out:
        error("Couldn't merge:\n%s" % out, err)

    if "VIRTUAL_ENV" not in os.environ or not os.environ["VIRTUAL_ENV"]:
        error("You need to run 'workon polling'")

    run("pip install -r requirements.txt")

def error(msg, err=""):
    print(msg)
    print(err)
    sys.exit(-1)

def run(cmd, waitFor=None, **kwargs):
    print(("Running: %s" % cmd,))
    p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    print(" has pid: %d" % p.pid)
    if waitFor:
        #From stackoverflow non-blocking reading
        #http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
        from threading import Thread
        from Queue import Queue, Empty

        def enqueue_output(out, queue):
            for line in iter(out.readline, b''):
                queue.put(line)
            out.close()

        out_queue = Queue()
        out_thread = Thread(target=enqueue_output, args=(p.stdout, out_queue))
        out_thread.daemon = True
        out_thread.start()

        err_queue = Queue()
        err_thread = Thread(target=enqueue_output, args=(p.stderr, err_queue))
        err_thread.daemon = True
        err_thread.start()

        doneWaiting = False
        while not doneWaiting:
            try: line = out_queue.get_nowait()
            except Empty:
                pass
            else:
                sys.stdout.write(line)
                if waitFor in line:
                    break

            try: line = err_queue.get_nowait()
            except Empty:
                pass
            else:
                sys.stderr.write(line)
                if waitFor in line:
                    break

        return ('', '')
    else:
        out,err = p.communicate()
        sys.stdout.write(out)
        sys.stderr.write(err)
    return out,err


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Does all of the ugly shell crap')
    parser.add_argument('program', choices=["update", "mysql", "memcached", "solr"])
    parser.add_argument('args', nargs='*')
    args = vars(parser.parse_args(sys.argv[1:]))
    if args["program"] in globals():
        globals()[args["program"]](*args['args'])


