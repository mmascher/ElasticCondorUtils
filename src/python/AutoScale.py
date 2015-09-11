import time
import htcondor
from plugins.awsec2 import AwsEC2
from functions.additional import parse_args, get_idle_jobs, get_config


def main():

    # Prepared to pass arguments file with defined parameters

    (opts, args) = parse_args()
    config = get_config(opts.config)

    coll = htcondor.Collector()
    autoType = 't1.micro'

    # Key name must be always unique. Adding timestamp

    aws = AwsEC2(**config)
    aws.check_status()
    aws.create_instance('ami-7fc59d4f', 1, 't1.micro', True)
    while True:
        idle_job_info = {}
        print 'Querying collector and getting schedulers...'
        schedd_ads = coll.query(htcondor.AdTypes.Schedd, '', ['Name',
                                'MyAddress', 'ScheddIpAddr'])
        for ad in schedd_ads:
            print 'Querying schedds and getting idle jobs'
            idle_job_info = get_idle_jobs(ad, idle_job_info, autoType)
        print 'Queries done. If i have idle jobs, will proceed requesting VM`s'
        for group in idle_job_info.keys():
            for vmtype in idle_job_info[group].keys():
                print '---- Group %s, VMType %s, IdleJobs %s' % (group,
                        vmtype, idle_job_info[group][vmtype])
                if group == 'None':
                    print '------ Found group None!'
                else:
                    print '------ Time to boot up some VM`s'
        print 'Checking status of VM`s'
        aws.check_status()
        print 'Waiting 500s for next cycle...'
        time.sleep(5)


if __name__ == '__main__':
    main()