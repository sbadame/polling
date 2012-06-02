#!/usr/bin/env python2.7

from __future__ import print_function
import os
import subprocess
import sys
import local_settings

argument_prefix = "cmd_"

""" For every entry in the tasks array there needs to be a function with that name that starts that process and stores
it's pid """
tasks = ["memcached", "solr", "runserver", "jobs"]

tempfile = ".managerprocs"
persisted = eval( file(tempfile).read() if os.path.exists(tempfile) else "{}" )

setting = lambda name, default: default if not name in dir(local_settings) else local_settings.__dict__.get(name)

def memcached():
    args = setting("MEMCACHED_ARGS", "")
    run("memcached " + args, name="memcached", waitForExit=False)

def solr():
    run("java -jar start.jar", name="solr", waitFor="Started", cwd="solr/example")

def runserver():
    # Really python? This is the only way to launch a non-child proc?
    pid = os.fork()
    if pid == 0:
        address = "0.0.0.0:%d" % setting("PORT", 2869)
        os.execvp("python", ["", "manage.py", "runserver", address])
    else:
        updatepid("runserver", pid)

def jobs():
    pid = os.fork()
    if pid == 0:
        import time
        while True:
            run("python manage.py update_random")
            run("python manage.py update_newest")
            run("python manage.py update_mostvoted")
            time.sleep(setting("JOB_TIME_MINUTES", 5) * 60)
    else:
        updatepid("jobs", pid)

def cmd_stat(args):
    '''
    [all|<any process>]
        Prints the currently known pid of every running process or None
        if the process is not running
    '''
    if len(args) < 2 or args[1] == "all":
        for cmd in [runserver, solr, memcached]:
            print(cmd.__name__ + ": " + str(app_pid(cmd)))
    else:
        command = globals()[args[1]]
        print(command.__name__ + ": " + str(app_pid(command)))

def cmd_start(args):
    '''
    [all|<any process>]
        Starts any of the available processes.
        Using the "all" option starts all of the processes required to get
        polling up and running in order checking for failed starts.
    '''
    if "all" in args:
        if len(args) == 1:
            cmd_start(tasks)
        else:
            print("Check your arguments! Can't start everything AND a process!")
    else:
        for arg in args:
            if app_pid(arg):
                print("%s is already running with pid: %d" % (arg, app_pid(arg)))
            else:
                globals()[arg]()

def cmd_stop(commands):
    '''
    [all|<any process>]
        Kills the processes passed in or all of the known running processes.
    '''
    if commands == ["all"]:
        cmd_stop(tasks)
    else:
        for command in commands:
            pid = app_pid(command)
            if pid:
                run("kill %d" % pid)
                updatepid(command, None)
            else:
                error("Don't have a pid for %s" % command)

def app_pid(command):
    name = command
    if name in persisted:
        if "pid" in persisted[name]:
            # A long-winded way of doing: ps -ef | grep <pid> | grep -v grep
            # To find out if proc with the given pid is alive
            pid = persisted[name]["pid"]
            p1 = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["grep", str(pid)], stdin=p1.stdout, stdout=subprocess.PIPE)
            p3 = subprocess.Popen(["grep", "-v", "grep"], stdin=p2.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()
            p2.stdout.close()
            out, err = p3.communicate()
            if str(pid) in out:
                return pid
            else:
                updatepid(name, None)
    return None

def cmd_update(args):
    '''
    <ignores any arguments>
        Runs the following operations stopping if an operation fails. Does
        not undo steps that completed succesfully.
        1. update source code
          git pull
        2. update pip requirements
          pip install -r requirements.txt
        3. perform any schema/daaa migrations
          python manage.py migrate polls
    '''
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

def cmd_update_solr_schema(args):
    out, _ = run('/usr/bin/env python2.7 manage.py build_solr_schema')
    f = open('solr/example/solr/conf/schema.xml', 'w')
    f.write(out)

def error(msg, err=""):
    print("OUT: %s\nERR: %s" % (msg,err))
    sys.exit(-1)

def run(cmd, name=None, waitForExit=True, waitFor=None, waitSeconds=1, verbose=True, **kwargs):
    if verbose: print("Running: %s" % cmd, end="")

    p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr = subprocess.PIPE, **kwargs)
    if verbose: print(" has pid: %d" % p.pid)

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
    '''
    Writes the given pid for the given process name to the .managerprocs 
    file
    '''
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

def unknownArgs(args):
    print("Couldn't understand the arguments: \"%s\"" % " ".join(args))
    cmd_printHelp()
    exit(1)

#Commands are functions that start with "argument_prefx"
#They can be directly called from the commandline by using their name
#without the prefix so: ./manager.py foo apple banana
#Assume that cmd_foo(args) exists and it will be called like so:
#cmd_foo(["apple","banana"])
#
#The usage string for help for that command is the function's
#docstring. So just document your code and all is good :)
available_commands = dict(
        (k[len(argument_prefix):],v)
        for (k,v) in globals().iteritems()
        if k.startswith(argument_prefix))

def format_command(name, function):
    doc = function.__doc__ if function.__doc__ else ""
    return  "%s %s\n" % (name, doc.strip())

def cmd_printHelp():
    commands = [ format_command(n, c)  for (n,c) in  available_commands.items() ]
    usage = "\n".join(commands)
    print(usage)

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] not in available_commands.keys():
        unknownArgs(args)
    else:
        try:
            available_commands[args[0]](args[1:])
        except KeyError:
            unknownArgs(args)

    if args[0] == "help" or args[0] == "-h":
        cmd_printHelp()
        exit()
