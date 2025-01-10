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
        ec2.KeyPair.from_key_pair_attributes(self, 'KeyPair',
                                            key_pair_name='Web-Service-EC2',
                                            type=ec2.KeyPairType.RSA)
                                                                                            
        





