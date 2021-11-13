import os
import pathlib

BASE = os.path.join(os.getcwd())
DB = os.path.join(BASE, 'DB', 'weatherinfo.db')
LOG = os.path.join(BASE, 'Logs', 'Log.log')
# SERVERURL = '192.168.1.5'
SERVERURL = '0.0.0.0'
SERVERPORT = '8051'
#192.168.137.20
#192.168.137.207
