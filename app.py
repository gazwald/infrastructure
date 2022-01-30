#!/usr/bin/env python3
import os
from aws_cdk import core

from vpcs.shared_vpc_stack import SharedVPCStack
from ecs_clusters.shared_ecs_cluster import SharedECSClusterStack
from albs.shared_alb_stack import SharedALBStack

app = core.App()

ap_southeast_2 = dict()
ap_southeast_2["env"] = {
    "account": os.getenv("AWS_ACCOUNT", os.getenv("CDK_DEFAULT_ACCOUNT", "")),
    "region": "ap-southeast-2"
}

ap_southeast_2["vpc"] = SharedVPCStack(app, "SharedVPCStack", env=ap_southeast_2["env"])

ap_southeast_2["ecs"] = SharedECSClusterStack(
    app,
    "SharedECSClusterStack",
    vpc=ap_southeast_2["vpc"].vpc,
    env=ap_southeast_2["env"],
)

# ap_southeast_2["alb"] = SharedALBStack(
#     app, "SharedALBStack", vpc=ap_southeast_2["vpc"].vpc, env=ap_southeast_2["env"]
# )

app.synth()
