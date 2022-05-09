#!/usr/bin/env python3
import os

from aws_cdk import App, Environment

from ecs_clusters.shared_ecs_cluster import SharedECSClusterStack
from vpcs.shared_vpc_stack import SharedVPCStack

app = App()
ap_southeast_2 = Environment(
    account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
    region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"]),
)

vpc = SharedVPCStack(app, "SharedVPCStack", env=ap_southeast_2)

ecs = SharedECSClusterStack(
    app, "SharedECSClusterStack", vpc=vpc.vpc, env=ap_southeast_2
)

app.synth()
