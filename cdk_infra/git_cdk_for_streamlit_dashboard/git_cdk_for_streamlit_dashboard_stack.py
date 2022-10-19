from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_certificatemanager as acm,
    aws_ecs_patterns as ecs_patterns,
    aws_sns_subscriptions as subs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_route53_targets as targets,
    aws_route53 as route53,
)


class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        project_prefix = "streamlit_demo"
        acm_cert_arn = self.node.try_get_context("acm_cert_arn")
        zone_name = self.node.try_get_context("zone_name")
        hosted_zone_id =  self.node.try_get_context("hosted_zone_id")

        CfnOutput(self, "DomainName", value=zone_name)
        CfnOutput(self, "ACMCertification", value=acm_cert_arn)

        acm_cert = acm.Certificate.from_certificate_arn(
            self, "cert", acm_cert_arn)

        vpc_id = "vpc_" + project_prefix
        app_vpc = ec2.Vpc(
            self,
            vpc_id,
            max_azs=2,
            cidr="10.55.0.0/16",
            # subnet_configuration=subnet_list,
        )

        ecs_id = "ecs_" + project_prefix
        # ECS Cluster with a VPC is created. Add the fargate task and service defn for launch.
        app_cluster = ecs.Cluster(self, ecs_id, vpc=app_vpc)
       
        # image from dockerhub at the moment
        ui_repository = ecr.Repository.from_repository_name(self, "streamlit-repo", "streamlit-congnito-tutorial")
        CfnOutput(
            self,
            "repo_name",
            value=ui_repository.repository_name
        )
        image_opt = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_ecr_repository(
                ui_repository),
            container_name="streamlit-congnito-tutorial",
            container_port=8501
        )
        
        fargate_service_id = "fargate_service_" + project_prefix
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            fargate_service_id,
            cluster=app_cluster,
            # vpc=app_vpc, # Vpc is already defined in the cluster config, no need to define here.
            assign_public_ip=True,
            cpu=1024,
            memory_limit_mib=2048,
            task_image_options=image_opt,
            protocol=elbv2.ApplicationProtocol.HTTPS,
            certificate=acm_cert,
            redirect_http=True
        )

        lb = fargate_service.load_balancer
        lb.connections.allow_to_any_ipv4(ec2.Port.tcp(
            443), "Allow ALB to communicate with Cognito IdP endpoint")


        fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(app_vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(80),
            description="Allow http inbound from VPC",
        )
        
        # Setup AutoScaling policy
        scaling = fargate_service.service.auto_scale_task_count(max_capacity=2)

        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=75,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )

        route53_hosted_zone_id = "route53_" + project_prefix
        r53_zone = route53.PublicHostedZone.from_public_hosted_zone_attributes(
            self, route53_hosted_zone_id,
            zone_name=zone_name,
            hosted_zone_id=hosted_zone_id
        )

         # Create A record for LB
        lb_A_record_id = "lb_A_record" + project_prefix
        lb_record_name = "cdk." + zone_name
        lb_record = route53.ARecord(self, lb_A_record_id,
                                    record_name=lb_record_name,
                                    zone=r53_zone,
                                    target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(lb)))
        lb_record.node.add_dependency(r53_zone)
        lb_record.node.add_dependency(fargate_service)




