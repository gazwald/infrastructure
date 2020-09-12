from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds

class SIDatabaseStack(core.Stack):

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 vpc: ec2.Vpc,
                 **kwargs) -> None:

        super().__init__(scope, id, **kwargs)
   
        engine = rds.DatabaseClusterEngine.aurora_mysql(
            version=rds.AuroraMysqlEngineVersion.VER_2_08_1
        )

        master_user = rds.Login(
            username='master'
        )

        self.cluster = rds.DatabaseCluster(
            self,
            "SIDatabase",
            engine=engine,
            master_user=master_user,
            default_database_name='MyDatabase',
            instance_props={
                "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                                     ec2.InstanceSize.MICRO),
                "vpc_subnets": {
                    "subnet_type": ec2.SubnetType.ISOLATED
                },
                "vpc": vpc
            },
            instances=1
        )

        cfn_cluster = self.cluster.node.default_child
        cfn_cluster.add_override("Properties.EngineMode", "serverless")
        cfn_cluster.add_override("Properties.ScalingConfiguration", { 
            'AutoPause': True, 
            'MaxCapacity': 4, 
            'MinCapacity': 1, 
            'SecondsUntilAutoPause': 600
        }) 
        self.cluster.node.try_remove_child('Instance1')
        self.cluster.add_rotation_single_user()
        
