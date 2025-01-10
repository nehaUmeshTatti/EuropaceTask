import unittest
from aws_cdk import App, assertions
from aws_cdk import aws_ec2 as ec2
from ec2_web_service.ec2_web_service_stack import Ec2WebServiceStack

class TestEc2WebServiceStack(unittest.TestCase):

    def setUp(self):
        # Initialize the CDK app and stack
        self.app = App()
        self.stack = Ec2WebServiceStack(self.app, 'TestStack')

    def test_vpc_created(self):
        # Assertion to verify VPC creation as expected
        template = assertions.Template.from_stack(self.stack)
        template.has_resource_properties('AWS::EC2::VPC', {
            'EnableDnsSupport': True,
            'EnableDnsHostnames': True,
    })
        template.resource_count_is('AWS::EC2::VPC', 1)
        template.resource_count_is('AWS::EC2::NatGateway', 0)

    def test_private_subnet_created(self):
        # Assertion to verify if a private subnet was created within the VPC
        template = assertions.Template.from_stack(self.stack)
        template.has_resource_properties('AWS::EC2::Subnet', {
        'MapPublicIpOnLaunch': False,   #Ensuring it is a private subnet
    })
    
    def test_security_group_created(self):
        # Assertion to check if the rules in the security group is created as expected
        template = assertions.Template.from_stack(self.stack)

        template.has_resource_properties('AWS::EC2::SecurityGroup', {
            'SecurityGroupIngress': assertions.Match.array_with([
                assertions.Match.object_like({
                    'CidrIp': '10.0.0.0/16',
                    'Description': 'Allow SSH traffic within VPC',
                    'FromPort': 22,
                    'IpProtocol': 'tcp',
                    'ToPort': 22    
                }),
                assertions.Match.object_like({
                    'CidrIp': '10.0.0.0/16',
                    'Description': 'Allow HTTPs traffic within VPC',
                    'FromPort': 443,
                    'IpProtocol': 'tcp',
                    'ToPort': 443
                })
        ])
    })
    
    def test_iam_role_with_managed_policy(self):
        # Assertion to check if the IAM role has the AmazonSSMManagedInstanceCore policy attached
        template = assertions.Template.from_stack(self.stack)

        template.has_resource_properties('AWS::IAM::Role', {
            'ManagedPolicyArns': assertions.Match.array_with([
                {
                    'Fn::Join': [
                        '',
                        [
                            'arn:',
                            {'Ref': 'AWS::Partition'},
                            ':iam::aws:policy/AmazonSSMManagedInstanceCore'
                        ]
                    ]
                }
        ])
    })

    def test_ec2_instance_created(self):
        # Assertion to verify if the EC2 instance is created with the correct instance type and image
        template = assertions.Template.from_stack(self.stack)

        template.has_resource_properties('AWS::EC2::Instance', {
            'InstanceType': assertions.Match.string_like_regexp('(t2|t3).micro'),
            'ImageId': assertions.Match.any_value(),
            'KeyName': 'Web-Service-EC2',
    })

if __name__ == '__main__':
    unittest.main()