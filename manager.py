#!/usr/bin/env python2.7

from __future__ import print_function
import os
import subprocess
import sys
import local_settings

tempfile = ".managerprocs"
persisted = eval( file(tempfile).read() if os.path.exists(tempfile) else "{}" )

setting = lambda name, default: default if not name in dir(local_settings) else local_settings.__dict__.get(name)

def mysql():
    pass

def memcached():
    args = setting("MEMCACHED_ARGS", "")
    run("memcached " + args, name="memcached", waitForExit=False)

def solr():
    run("java -jar start.jar", name="solr", waitFor="Started", cwd="solr/example")

def runserver():
    run("python manage.py runserver 0.0.0.0:2869", name="server", waitSeconds=3, waitForExit=False)

def start_all():
    startApp(mysql)
    startApp(memcached)
    startApp(solr)
    startApp(runserver)
    import time
    time.sleep(60)

def startApp(command):
    name = command.__name__
    if app_pid(command):
        print("%s is already running with pid: %d" % (name, app_pid(command)))
    else:
        command()

def killApp(command):
    pid = app_pid(command)
    if pid:
        run("kill %d" % pid)
        updatepid(command.__name__, None)
    else:
        error("Don't have a pid for %s" % command.__name__)

def app_pid(command):
    name = command.__name__
    if name in persisted:
        if "pid" in persisted[name]:
            return persisted[name]["pid"]
    return None

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
    run("python manage.py migrate polls")

def error(msg, err=""):
    print("OUT: %s\nERR: %s" % (msg,err))
    sys.exit(-1)

def run(cmd, name=None, waitForExit=True, waitFor=None, waitSeconds=1, **kwargs):
    print("Running: %s" % cmd, end="")

    p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr = subprocess.PIPE, **kwargs)
    print(" has pid: %d" % p.pid)

    if name: updatepid(name, p.pid)

    if not waitFor and waitForExit:
        out,err = p.communicate()
        sys.stdout.write(out)
        sys.stderr.write(err)
        return out,err

    elif waitSeconds:

        import time
        start_time = time.clock()

        if p.stdout and p.stderr:

            #From stackoverflow non-blocking reading
            #http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
            from threading import Thread
            from Queue import Queue, Empty

            def enqueue_output(out, queue):
                for line in iter(out.read, b''):
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


            def keeploop():
                if waitFor:
                    return time.clock() - start_time <= 5
                else:
                    return time.clock() - start_time <= waitSeconds

            while p.poll() is None and keeploop():
                try: outline = out_queue.get_nowait()
                except Empty:
                    pass
                else:
                    sys.stdout.write(outline)
                    if waitFor and waitFor in outline:
                        break

                try: errline = err_queue.get_nowait()
                except Empty:
                    pass
                else:
                    sys.stderr.write(errline)
                    if waitFor and waitFor in errline:
                        break
        else:
            while p.poll() is None and time.time() - start_time <= waitSeconds:
                #Yes... this is a busy wait... But we don't want to wait longer than we have to.
                time.sleep(0.1)


        sys.stdout.flush()
        sys.stderr.flush()
        if not p.poll() is None: #The process should not have terminated...
            if name: updatepid(name, None)
            error("command: \"%s\" with pid: %d exited with exit code: %d" % (cmd, p.pid, p.returncode))

        return None

def updatepid(name, pid):
    old = {}
    if name in persisted:
        old = persisted[name]
    else:
        persisted["name"] = {}
    old.update({"pid": pid})
    persisted[name] = old

    f = open(tempfile, "w")
    f.write("%r" % persisted)
    f.close()

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] not in "start,kill,update,restart".split(","):
        raise ValueError("Don't understand command: %s" % args[0])

    if args[0] != "update" and args[1] not in "runserver,mysql,memcached,solr,all".split(","):
        raise ValueError("Don't understand program: %s" % args[1])

    if args[0] == "update":
        update()
        exit()

    if args[0] == "start" and args[1] == "all":
        start_all()
        exit()

    command = globals()[args[1]]
    if args[0] == "kill":
        killApp(command)
    else:
        command()

