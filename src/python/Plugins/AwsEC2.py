import boto


class AwsEC2(object):
    def __init__(self, config):
        """Initializer"""
        self.config = config
        self.ec2 = boto.connect_ec2()
        self.keyName = self.config['keyName']
        key_pair = self.ec2.create_key_pair(self.keyName)
        key_pair.save('~/.ssh/')
      
    def checkConfig(self, config, json):
        """Check json configuration for images"""
        return True
        
    def createInstance(self, instImage, instCount=1, instType='t1.micro', dryRun=False):
	"""Create N instances with image
	  instCount (How many to create). Default 1
	  instImage (Specify image). No default, comes from config
	  instType (Type of instance) Default t1.micro
	  dryRun (Run command without persisting the result) Default False#TODO"""
	#Might need to wrap with try: except, but not sure what it can throw
        creation = self.ec2.run_instances(image_id=instImage, key_name=self.keyName, instance_type=instType, min_count = instCount, max_count = instCount, dry_run=dryRun, security_group_ids=['sg-dd5737b8'], security_groups=['aws_hep'], instance_initiated_shutdown_behavior='terminate')

    def checkStatus(self):
	"""Check created instances.
	TODO: Need to define what to do when.
	"""
        print 'Checking current status and which instances are ready'
	for inst in self.ec2.get_all_instances():
	    print 'Booted instance: %s STATUS: %s' % (inst.id, inst.status)
