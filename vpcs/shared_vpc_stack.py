from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class SharedVPCStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        self.subnet_public = self.define_public_subnet()
        self.subnet_isolated = self.define_isolated_subnet()

        self.vpc = ec2.Vpc(
            self,
            "SharedVPC",
            cidr="172.17.0.0/16",
            nat_gateways=0,
            max_azs=3,
            subnet_configuration=[self.subnet_public, self.subnet_isolated],
        )

        self.add_gateway_endpoint("s3")
        self.add_gateway_endpoint("dynamodb")

    def add_gateway_endpoint(self, endpoint: str):
        self.vpc.add_gateway_endpoint(
            endpoint + "_endpoint", service=ec2.GatewayVpcEndpointAwsService(endpoint)
        )

    def define_public_subnet(self):
        return ec2.SubnetConfiguration(
            cidr_mask=24, name="shared_public", subnet_type=ec2.SubnetType.PUBLIC
        )

    def define_isolated_subnet(self):
        return ec2.SubnetConfiguration(
            cidr_mask=24,
            name="shared_isolated",
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
        )
