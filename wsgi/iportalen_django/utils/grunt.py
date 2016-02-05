from django.conf import settings
import subprocess
import os
import signal
import atexit


class GruntProcess:
    def __init__(self):
        self.grunt_process = None

    def start_grunt(self):
        #  Only start the process once!
        if self.grunt_process is not None:
            return
        print('>>> Starting grunt! :)')
        self.grunt_process = subprocess.Popen(
            ['npm install {0}'.format(os.path.join(settings.BASE_DIR, 'grunt')),
             'grunt --gruntfile={0}/Gruntfile.js --base=.'.format(os.path.join(settings.BASE_DIR, 'grunt'))],
            shell=True,
        )
        print('>>> Gruntprocess on pid {0}'.format(self.grunt_process.pid))

        #  When this instance is killed/terminated also kill the subprocess.
        atexit.register(kill_grunt_process, self.grunt_process.pid)


def kill_grunt_process(pid):
    print('>>> Closing grunt process')
    os.kill(pid, signal.SIGTERM)

