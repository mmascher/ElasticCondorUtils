import os
import sys
import json
import optparse
import htcondor


def get_config(config):
    if config:
        if not os.path.exists(config):
            print >> sys.stderr, 'Config file %s does not exist.' \
                % config
            sys.exit(1)
        with open(config) as fd:
            return json.load(fd)
    elif os.path.exists('config.json'):
        with open('config.json') as fd:
            return json.load(fd)


def parse_args():
    """Parse additional arguments"""

    parser = optparse.OptionParser()
    parser.add_option('-c', '--config', help='Configuration file',
                      dest='config', default=None)
    (opts, args) = parser.parse_args()
    if args:
        parser.print_help()
        print >> sys.stderr, '%s takes no arguments.' % sys.args[0]
        sys.exit(1)

    return (opts, args)


def get_logger():
    """Create logging instance"""

    return True


def get_idle_jobs(ad, idle_job_info, auto_type):
    schedd = htcondor.Schedd(ad)
    try:
        jobs = schedd.xquery('JobStatus=?=1', ['RequestMemory',
                             'MaxWallTimeMins', 'QDate', 'AutoCloudType'
                             , 'AutoCloudGroup'])
    except Exception, e:
        print 'Failed querying', ad['Name']
        print e
        return
    for job in jobs:
        auto_cloud_group = 'None'
        auto_cloud_type = auto_type
        if 'AutoCloudType' in job.keys():
            auto_cloud_type = job['AutoCloudType']
        if 'AutoCloudGroup' in job.keys():
            auto_cloud_group = job['AutoCloudGroup']

    # Double checking that it does not exists and add what is needed

        if auto_cloud_group not in idle_job_info.keys():
            idle_job_info[auto_cloud_group] = {}
        if auto_cloud_type not in idle_job_info[auto_cloud_group].keys():
            idle_job_info[auto_cloud_group][auto_cloud_type] = 0
        idle_job_info[auto_cloud_group][auto_cloud_type] += 1
    return idle_job_info