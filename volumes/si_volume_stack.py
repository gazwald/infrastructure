from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_efs as efs

class SIVolumeStack(core.Stack):

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 vpc: ec2.Vpc,
                 **kwargs) -> None:

        super().__init__(scope, id, **kwargs)
        
        self.file_system = efs.FileSystem(self, "SIEFSVolume",
            vpc=vpc,
            lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            throughput_mode=efs.ThroughputMode.BURSTING
        )
