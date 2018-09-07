import subprocess as sp
import time
import datetime as dt
import pytz
import os
import signal
dir_path = os.path.dirname(os.path.abspath( __file__ ))
github_shellstr = '''git fetch --all; git reset --hard origin/master; git pull origin master'''
_=sp.check_output(github_shellstr, shell=True)
shelllst=['python3',
          os.path.join(dir_path, 'subscriber.py')]

proc = sp.Popen(shelllst)
print('running')
try:
    while True:
        time.sleep(300)
        print('---------------------killing------------------------')
        proc.send_signal(signal.SIGINT)
        #proc.kill()
        # Sync to github
        print('Sync to github.....')
        retry = 2
        while retry>0:
            try:
                _=sp.check_output(github_shellstr, shell=True)
                break
            except sp.CalledProcessError as e:
                print(e)
                retry -= 1
                if retry == 0:
                    raise
                time.sleep(5)
        time.sleep(5)
        proc = sp.Popen(shelllst)
        poll = proc.poll()
        if poll is not None:
            raise RuntimeError('Error')
except KeyboardInterrupt:
    proc.kill()
    exit(0)

