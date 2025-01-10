import unittest
from aws_cdk import App, assertions
from aws_cdk import aws_ec2 as ec2
from ec2_web_service.ec2_web_service_stack import Ec2WebServiceStack

class TestWebServerEc2Stack(unittest.TestCase):

    def setUp(self):
        # Initialize the CDK app and stack
        self.app = App()
        self.stack = Ec2WebServiceStack(self.app, "TestStack")

    def test_vpc_created(self):
        # Assertion to verify VPC creation as expected
        template = assertions.Template.from_stack(self.stack)
        template.has_resource_properties('AWS::EC2::VPC', {
            'EnableDnsSupport': True,
            'EnableDnsHostnames': True,
        })
        template.resource_count_is('AWS::EC2::VPC', 1)
        template.resource_count_is('AWS::EC2::NatGateway', 0)
