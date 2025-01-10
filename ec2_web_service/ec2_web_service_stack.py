from aws_cdk import (
    Stack,
    aws_ec2 as ec2
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

