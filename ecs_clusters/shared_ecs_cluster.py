from aws_cdk import core

import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ec2 as ec2


class SharedECSClusterStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        cluster_name = "SharedECSCluster"

        self.cluster = ecs.Cluster(
            self,
            cluster_name,
            cluster_name=cluster_name,
            enable_fargate_capacity_providers=True,
            vpc=vpc,
        )
