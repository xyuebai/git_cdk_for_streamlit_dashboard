## Prerequest
- A registered domain and hosted on AWS route53.
- A public certificate required for the site.


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## How to run

```
cdk synth --context acm_cert_arn=<acm_cert_arn> --context zone_name=<zone_name> --context hosted_zone_id=<hosted_zone_id> 

cdk deploy
```