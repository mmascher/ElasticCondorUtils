import sys
import boto
from collections import namedtuple
from boto.ec2.connection import EC2Connection


class AwsEC2(object):

    def __init__(self, **config):
        """Initializer"""

        self.config = namedtuple('config', config)(**config)
        self.conn = boto.ec2.connect_to_region('us-west-2',
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key)

    def checkConfig(self, config, json):
        """Check json configuration for images"""

        return True

    def create_instance(
        self,
        instImage,
        instCount=1,
        instType='t1.micro',
        dryRun=False,
        ):
        """Create N instances with image
....       instCount (How many to create). Default 1
           instImage (Specify image). No default, comes from config
           instType (Type of instance) Default t1.micro
           dryRun (Run command without persisting the result) Default False#TODO
        """

        # Might need to wrap with try: except, but not sure what it can throw

        self.conn.run_instances(instImage, instCount, instType)

    def check_status(self):
        """Check created instances.
           TODO: Need to define what to do when.
        """

        print 'Checking current status and which instances are ready'
        try:
            for inst in self.conn.get_all_instances():
                print 'Booted instance: %s STATUS: %s' % (inst.id,
                        inst.status)
        except boto.exception.EC2ResponseError, re:
            print re
            sys.exit(1)