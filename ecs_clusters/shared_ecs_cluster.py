from aws_cdk import core

import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_autoscaling as autoscaling


class SharedECSClusterStack(core.Stack):

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 vpc: ec2.Vpc,
                 **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        cluster_size = 1
        cluster_name = 'SharedECSCluster'

        self.cluster = ecs.Cluster(
            self,
            cluster_name,
            cluster_name=cluster_name,
            vpc=vpc,
        )

        self.asg = self.cluster.add_capacity(
            cluster_name + '_ASG_Capacity',
            instance_type=ec2.InstanceType('t3.micro'),
            max_capacity=6,
            min_capacity=cluster_size,
            task_drain_time=core.Duration.minutes(1),
            spot_price="0.0132",
            spot_instance_draining=True
        )

        self.asg.scale_on_cpu_utilization(
            "KeepCpuHalfwayLoaded",
            target_utilization_percent=50
        )
