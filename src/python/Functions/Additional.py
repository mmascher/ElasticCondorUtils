import re
import os
import sys
import json
import time
import optparse
import htcondor
import ConfigParser

def parse_args():
    """Parse additional arguments"""
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", help="Configuration file", dest="config", default=None)
    opts, args = parser.parse_args()
    if args:
        parser.print_help()
        print >> sys.stderr, "%s takes no arguments." % sys.args[0]
        sys.exit(1)

    cp = ConfigParser.ConfigParser()
    if opts.config:
        if not os.path.exists(opts.config):
            print >> sys.stderr, "Config file %s does not exist." % opts.config
            sys.exit(1)
        cp.read(opts.config)
    elif os.path.exists("config.conf"):
        cp.read("config.conf")

    return opts, args

def get_logger():
    """Create logging instance"""
    return True

def getIdleJobs(ad, IdleJobInfo, autoType):
    schedd = htcondor.Schedd(ad)
    try:
        jobs = schedd.xquery("JobStatus=?=1", ["RequestMemory", "MaxWallTimeMins", "QDate", "AutoCloudType", "AutoCloudGroup"])
    except Exception, e:
        print "Failed querying", ad["Name"]
        print e
        return
    for job in jobs:
	autoCloudGroup = "None"
	autoCloudType = autoType
	if 'AutoCloudType' in job.keys():
	    autoCloudType = job['AutoCloudType']
	if 'AutoCloudGroup' in job.keys():
	    autoCloudGroup = job['AutoCloudGroup']

	#Double checking that it does not exists and add what is needed
	if autoCloudGroup not in IdleJobInfo.keys():
            IdleJobInfo[autoCloudGroup] = {}
	if autoCloudType not in IdleJobInfo[autoCloudGroup].keys():
	    IdleJobInfo[autoCloudGroup][autoCloudType] = 0
	IdleJobInfo[autoCloudGroup][autoCloudType] += 1
    return IdleJobInfo
