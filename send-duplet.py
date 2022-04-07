#!/usr/bin/python3

import copy
import os
import requests

import threading
import time

from requests.packages.urllib3.exceptions import SubjectAltNameWarning
from uyuni.common.context_managers import cfg_component

requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)

NTHREADS = 2
TMOUT = 30
TMOUT_MAX = 240
printLock = threading.Lock()
threads = []
hosts = ["vz-uyuni-s153.tf.local"]
mods = [["hardware.profileupdate"], ["certs", "channels", "util.systeminfo"]]
outs = ["hardware.profileupdate", "pkg_|-mgr_absent_ca_package_|-rhn-org-trusted-ssl-cert_|-removed"]

with cfg_component("server") as CFG:
    salt_secret = CFG["secret_key"]

data = {'tgt': [], 'roster': 'uyuni', 'eauth': 'file', 'refresh_cache': True, 'kwarg': {'mods': [], 'queue': True},
        'password': salt_secret, 'ignore_host_keys': False,
        'tgt_type': 'list', 'ssh_sudo': False, 'client': 'ssh', 'ssh_priv': '/srv/susemanager/salt/salt_ssh/mgr_ssh_id',
        'fun': 'state.apply', 'username': 'admin'}

log = open("duplet.log", "w")

def thrprint(*args, **kwargs):
    printLock.acquire()
    tms = "[{}] ".format(time.asctime())
    print(tms, *args, **kwargs)
    log.write(tms)
    log.write(*args, **kwargs)
    log.write("\n")
    printLock.release()

def thrworker(name, host, mods, outs):
    snd_data = copy.deepcopy(data)
    snd_data["tgt"].append(host)
    snd_data["kwarg"]["mods"] = mods
    response = requests.post('https://localhost:9080/run', json=snd_data)
    txt = "OK" if outs in response.text else "FAIL"
    thrprint("{}[{}]: {}".format(name, response.status_code, txt))

hosts_len = len(hosts)
mods_len = len(mods)

for i in range(NTHREADS):
    tnm = "Thread-{}".format(i)
    host = copy.deepcopy(hosts[i % hosts_len])
    mod = copy.deepcopy(mods[i % mods_len])
    out = copy.deepcopy(outs[i % mods_len])
    thrprint("Starting {}: '{}' for mods: {}".format(tnm, host, mod))
    thr = threading.Thread(target=thrworker, args=(tnm, host, mod, out, ))
    threads.append(thr)
    thr.start()

for thr in threads:
    thr.join()
