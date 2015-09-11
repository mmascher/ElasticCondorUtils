import time
import htcondor
from Plugins.AwsEC2 import AwsEC2
from Functions.Additional import parse_args, getIdleJobs, get_config


def main():

    # Prepared to pass arguments file with defined parameters

    (opts, args) = parse_args()
    config = get_config(opts.config)

    coll = htcondor.Collector()
    autoType = 't1.micro'

    # Key name must be always unique. Adding timestamp

    aws = AwsEC2(**config)
    aws.checkStatus()
    aws.createInstance('ami-7fc59d4f', 1, 't1.micro', True)
    while True:
        IdleJobInfo = {}
        print 'Querying collector and getting schedulers...'
        schedd_ads = coll.query(htcondor.AdTypes.Schedd, '', ['Name',
                                'MyAddress', 'ScheddIpAddr'])
        for ad in schedd_ads:
            print 'Querying schedds and getting idle jobs'
            IdleJobInfo = getIdleJobs(ad, IdleJobInfo, autoType)
        print 'Queries done. If i have idle jobs, will proceed requesting VM`s'
        for group in IdleJobInfo.keys():
            for vmtype in IdleJobInfo[group].keys():
                print '---- Group %s, VMType %s, IdleJobs %s' % (group,
                        vmtype, IdleJobInfo[group][vmtype])
                if group == 'None':
                    print '------ Found group None!'
                else:
                    print '------ Time to boot up some VM`s'
        print 'Checking status of VM`s'
        aws.checkStatus()
        print 'Waiting 500s for next cycle...'
        time.sleep(5)


if __name__ == '__main__':
    main()