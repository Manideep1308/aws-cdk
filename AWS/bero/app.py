#!/usr/bin/env python3
import os

import aws_cdk as cdk

from bero.bero_stack import BeroStack

#add stack


app = cdk.App()
BeroStack(app, "BeroStack", env=cdk.Environment(account='659046966626', region='us-east-1'))

    



































app.synth()
