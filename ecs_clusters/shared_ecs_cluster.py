from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from constructs import Construct


class SharedECSClusterStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        cluster_name = "SharedECSCluster"

        self.cluster = ecs.Cluster(
            self,
            "ecs",
            cluster_name=cluster_name,
            enable_fargate_capacity_providers=True,
            vpc=vpc,
        )
