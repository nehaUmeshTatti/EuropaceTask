from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class Ec2WebServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        #create VPC and private subnet for the Ec2 instance
        webservice_vpc = ec2.Vpc(self, 'WebServiceVpc',
                                 nat_gateways=0,
                                 subnet_configuration=[
                                     ec2.SubnetConfiguration(name='WebServicePrivateSubnet',
                                                             subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, 
                                                             cidr_mask=24)])
        
        # The security group inbound and outbound rules can be enhanced depending on the requirements
        # Assuming in the current scenario https and ssh connection is required, and the webservice runs on a private subnet the following is added
        # create security group for EC2
        ec2_security_group = ec2.SecurityGroup(self, 'WebServiceSecurityGroup',
                                               vpc=webservice_vpc,
                                               allow_all_outbound=False)
        
        #allow inbound ssh connection through a specific IP range
        ec2_security_group.add_ingress_rule(ec2.Peer.ipv4('10.0.0.0/16'),
                                            ec2.Port.tcp(22),  
                                            'Allow SSH traffic within VPC')
        
        #allow inbound https connection through a specific IP range
        ec2_security_group.add_ingress_rule(ec2.Peer.ipv4('10.0.0.0/16'),  
                                            ec2.Port.tcp(443),  
                                            'Allow HTTPs traffic within VPC')
        
        #allow outbound https connection through a specific IP range
        ec2_security_group.add_egress_rule(ec2.Peer.ipv4('10.0.0.0/16'),  
                                           ec2.Port.tcp(443),  
                                           'Allow HTTPs traffic within VPC')
        
        # IAM Role for the EC2 instance
        ec2_iam_role = iam.Role(self, 'WebserviceEc2Role',
                                assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'))

        #adding policies to the role, this can be enhanced based on the requirement                                                                  
        ec2_iam_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore')
        )

        ec2_iam_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMPatchAssociation')
        )

        #Use an existing key-pair for the EC2 instance 
        #Access to the instance can be managed via SSM without SSH access, however keeping this for debugging flexibility using SSH
        webservice_key_pair =  ec2.KeyPair.from_key_pair_attributes(self, 'KeyPair',
                                                                    key_pair_name='Web-Service-EC2',
                                                                    type=ec2.KeyPairType.RSA)
        
        #create an EC2 instance with vpc, subnet, security group, Iam role and key pair
        ec2_instance = ec2.Instance(self, 'WebServiceInstance',
                                    instance_type=ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2,
                                                                    instance_size=ec2.InstanceSize.MICRO),
                                    machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                    vpc=webservice_vpc,
                                    security_group=ec2_security_group,
                                    key_pair=webservice_key_pair,
                                    user_data_causes_replacement=False)
        
        # user data for bootstrapping and downloading dependencies at the time of launching the instance
        # An example of user data is shown below
        ec2_instance.add_user_data(
            '#!/bin/bash',
            'sudo yum update -y',
            'sudo yum install -y httpd',
            'sudo systemctl start httpd',
            'sudo systemctl enable httpd'
        )
                                                                                            
        





