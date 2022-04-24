# (!) This script is for your convenience only. Use at your own risk.

import os
from subprocess import Popen
import sys

print('===============================\nPress enter to stop the servers\n===============================\n')

os.chdir(os.path.dirname(os.path.abspath(__file__)))

env = os.environ.copy()

ps = []

env['FLASK_APP'] = 'reverse_proxy'
ps.append(Popen(['flask', 'run', '--port', '5000', '--reload'], cwd=os.getcwd(), env=env))
env['FLASK_APP'] = 'auth_server'
ps.append(Popen(['flask', 'run', '--port', '5001', '--reload'], cwd=os.getcwd(), env=env))
env['FLASK_APP'] = 'app_server'
ps.append(Popen(['flask', 'run', '--port', '5002', '--reload'], cwd=os.getcwd(), env=env))
ps.append(Popen(['python', '-m', 'http.server', '5003'], cwd=os.getcwd()))

input()

for p in ps:
    p.terminate()
    p.wait()

print('Done')
sys.exit(0)
