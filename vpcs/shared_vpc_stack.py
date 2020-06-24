from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class SharedVPCStack(core.Stack):

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 **kwargs) -> None:

        super().__init__(scope, id, **kwargs)
       
        subnet_public = ec2.SubnetConfiguration(
            cidr_mask=24,
            name='shared_public',
            subnet_type=ec2.SubnetType.PUBLIC
        )

        self.vpc = ec2.Vpc(
            self,
            'SharedVPC',
            cidr='172.17.0.0/16',
            nat_gateways=0,
            max_azs=3,
            subnet_configuration=[subnet_public]
        )

        self.add_gateway_endpoint('s3')
        self.add_gateway_endpoint('dynamodb')

    def add_gateway_endpoint(self, endpoint):
        self.vpc.add_gateway_endpoint(
            endpoint + '_endpoint',
            service=ec2.GatewayVpcEndpointAwsService(endpoint)
        )
        
