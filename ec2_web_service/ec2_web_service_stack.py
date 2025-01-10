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
        


