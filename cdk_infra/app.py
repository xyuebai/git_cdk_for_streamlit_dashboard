#!/usr/bin/env python3

import aws_cdk as cdk

from git_cdk_for_streamlit_dashboard.git_cdk_for_streamlit_dashboard_stack import AppStack


app = cdk.App()
AppStack(app, "git-cdk-for-streamlit-dashboard")

app.synth()
