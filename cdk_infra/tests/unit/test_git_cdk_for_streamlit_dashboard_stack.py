import aws_cdk as core
import aws_cdk.assertions as assertions
from git_cdk_for_streamlit_dashboard.git_cdk_for_streamlit_dashboard_stack import GitCdkForStreamlitDashboardStack


def test_sqs_queue_created():
    app = core.App()
    stack = GitCdkForStreamlitDashboardStack(app, "git-cdk-for-streamlit-dashboard")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = GitCdkForStreamlitDashboardStack(app, "git-cdk-for-streamlit-dashboard")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
