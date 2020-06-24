from aws_cdk import core
import aws_cdk.aws_ecs as ecs


class SIWordpressStack(core.Stack):

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 cluster: ecs.Cluster,
                 **kwargs) -> None:

        super().__init__(scope, id, **kwargs)
     
        sixty_seconds = core.Duration.seconds(60)

        database_hostname = 'si-mariadb' 
        database_name = 'siwordpress'
        database_username= 'wordpress_user'
        database_password = 'wordpress_pass'

        port_80 = ecs.PortMapping(container_port=80) 
        port_3306 = ecs.PortMapping(container_port=3306) 

        wordpress_task = ecs.Ec2TaskDefinition(
            self,
            "SIWordpressTask"
        )

        wordpress_container = wordpress_task.add_container(
            "SIWordpressContainer",
            image=ecs.ContainerImage.from_registry("docker.io/wordpress:latest"),
            memory_limit_mib=256,
            environment={
                'WORDPRESS_DB_HOST': database_hostname,
                'WORDPRESS_DB_USER': database_username,
                'WORDPRESS_DB_PASSWORD': database_password,
                'WORDPRESS_DB_NAME': database_name
            },
            start_timeout=sixty_seconds,
            stop_timeout=sixty_seconds
        )

        mariadb_container = wordpress_task.add_container(
            "SIMariaDBContainer",
            image=ecs.ContainerImage.from_registry("docker.io/mariadb:latest"),
            memory_limit_mib=256,
            hostname=database_hostname,
            environment={
                'MYSQL_ROOT_PASSWORD': 'password',
                'MYSQL_DATABASE': database_name,
                'MYSQL_USER': database_username,
                'MYSQL_PASSWORD': database_password
            },
            start_timeout=sixty_seconds,
            stop_timeout=sixty_seconds
        )

        wordpress_container.add_port_mappings(port_80)

        ecs_service = ecs.Ec2Service(self, "Service",
            cluster=cluster,
            task_definition=wordpress_task
        )
