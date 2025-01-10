#!/usr/bin/env python3
import aws_cdk as cdk
from ec2_web_service.ec2_web_service_stack import Ec2WebServiceStack

app = cdk.App()
Ec2WebServiceStack(app, "Ec2WebServiceStack")
app.synth()
