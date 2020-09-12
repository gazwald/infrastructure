from aws_cdk import core
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_efs as efs
import aws_cdk.aws_rds as rds
import aws_cdk.aws_elasticloadbalancingv2 as elbv2

class SIWordpressStack(core.Stack):

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 cluster: ecs.ICluster,
                 alb: elbv2.IApplicationLoadBalancer,
                 volume: efs.IFileSystem,
                 database: rds.IDatabaseCluster,
                 **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        self.cluster = cluster
        self.alb = alb
        self.efs = efs
        self.rds = rds
        self.sixty_seconds = core.Duration.seconds(60)

        self.database_hostname = '???'
        self.database_name = 'siwordpress'
        self.database_username = 'wordpress_user'
        self.database_password = 'wordpress_pass'

        port_80 = ecs.PortMapping(container_port=80) 

        self.task = ecs.Ec2TaskDefinition(
            self,
            "SIWordpressTask"
        )

        self.define_wordpress_container()

        self.wordpress_container.add_port_mappings(port_80)

        self.create_ec2_service()
        self.create_application_listener()

    def create_ec2_service(self):
        self.service = ecs.Ec2Service(
            self,
            "Service",
            cluster=self.cluster,
            task_definition=self.task
        )

    def create_application_listener(self):
        self.listener = elbv2.ApplicationListener(
            self,
            "SIWPListener",
            load_balancer=self.alb,
            port=80
        )

        self.listener.add_targets(
            "SIWPListernTarget",
            port=80,
            targets=[self.service]
        )

    def define_wordpress_container(self):
        self.wordpress_container = self.task.add_container(
            "SIWordpressContainer",
            image=ecs.ContainerImage.from_registry("docker.io/wordpress:latest"),
            memory_limit_mib=256,
            environment={
                'WORDPRESS_DB_HOST': self.database_hostname,
                'WORDPRESS_DB_USER': self.database_username,
                'WORDPRESS_DB_PASSWORD': self.database_password,
                'WORDPRESS_DB_NAME': self.database_name
            },
            start_timeout=self.sixty_seconds,
            stop_timeout=self.sixty_seconds
        )

    def add_efs_volume(self):
        efs_volume = ecs.EfsVolumeConfiguration(
            file_system_id=self.efs.file_system_id
        )
        self.task.add_volume(
            name='www',
            efs_volume_configuration=efs_volume
        )
