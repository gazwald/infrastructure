#!/usr/bin/env python3
import os
from aws_cdk import core

from vpcs.shared_vpc_stack import SharedVPCStack
from ecs_clusters.shared_ecs_cluster import SharedECSClusterStack

from services.si_wordpress_stack import SIWordpressStack

app = core.App()

ap_southeast_2 = dict()
ap_southeast_2['env'] = {'account': os.getenv('AWS_ACCOUNT', os.getenv('CDK_DEFAULT_ACCOUNT', '')),
                         'region': os.getenv('AWS_DEFAULT_REGION', os.getenv('CDK_DEFAULT_REGION', 'ap-southeast-2'))}

ap_southeast_2['vpc'] = SharedVPCStack(app, "SharedVPCStack", env=ap_southeast_2['env'])
ap_southeast_2['ecs'] = SharedECSClusterStack(app, "SharedECSClusterStack", vpc=ap_southeast_2['vpc'].vpc, env=ap_southeast_2['env'])

SIWordpressStack(app, "SIWordpressStack", cluster=ap_southeast_2['ecs'].cluster, env=ap_southeast_2['env'])

app.synth()
