import json
import os
import pwd
import re
import subprocess
import sys

from flask import Flask, request, redirect
app = Flask(__name__)

def _run_command(command):
    """Runs the specified command, specified as a list. Returns stdout, stderr and return code                                                                         
    """
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode

def cache_list_to_string(cache_list):
    comma_list = ""
    for cache in cache_list:
        comma_list += cache + ","
    return comma_list

@app.route('/')
def nearest_cache():
    CACHE_LIST = ["mwt2-stashcache.campuscluster.illinois.edu", "its-condor-xrootd1.syr.edu","osg-kansas-city-stashcache.nrp.internet2.edu","osg-chicago-stashcache.nrp.internet2.edu","osg-new-york-stashcache.nrp.internet2.edu","sc-cache.chtc.wisc.edu","osg-gftp.pace.gatech.edu"]
    OASIS_HOST = "oasis-replica.opensciencegrid.org"
    UserIP = request.remote_addr

    comma_list = cache_list_to_string(CACHE_LIST)
    cmd = ["curl", "http://%s:8000/cvmfs/dwd.test/api/v1.0/geo/%s/%s" % (OASIS_HOST, UserIP, comma_list)]
    (order_list_caches, stderr, errcode) = _run_command(cmd)
    order_list_caches = order_list_caches.split(",")

    nearest_cache = CACHE_LIST[int(order_list_caches[0])-1]
    return nearest_cache

if __name__ == '__main__':
    app.run()