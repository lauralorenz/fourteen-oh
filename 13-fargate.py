from prefect.environments.storage import S3
from prefect.environments import FargateTaskEnvironment
from prefect import task, Flow, Parameter
import prefect

STORAGE = S3(bucket="demo-prefect-flows-14")

ENVIRONMENT = FargateTaskEnvironment(
		networkMode="awsvpc",
		family="13-fargate", 
		taskDefinition="13-fargate", 
		memory="512", 
		cpu="256", 
		cluster="prefect-demo-cluster",
	 	networkConfiguration={'awsvpcConfiguration': {'assignPublicIp': 'ENABLED', 'subnets': ['subnet-7410175c'], 'securityGroups': []}},
	 	taskRoleArn="arn:aws:iam::136638793011:role/prefect-demo-fargate-task-role",
 		executionRoleArn="arn:aws:iam::136638793011:role/ecsTaskExecutionRole",
	  	metadata={"image":'prefecthq/prefect:all_extras-0.13.19'})

@task
def hi():
   logger = prefect.context.get('logger')
   logger.info("Hello!")


with Flow("prefect-13", storage=STORAGE, environment=ENVIRONMENT) as flow:
	hi()

flow.register("14-demo")

#########
# agent #
#########

from prefect.agent.fargate import FargateAgent

AGENT = FargateAgent(labels=["s3-flow-storage"],
	cpu="256", 
	memory="512",
	cluster="prefect-demo-cluster", 
	networkConfiguration={'awsvpcConfiguration': {'assignPublicIp': 'ENABLED', 'subnets': ['subnet-7410175c'], 'securityGroups': []}}, 
	taskRoleArn="arn:aws:iam::136638793011:role/prefect-demo-fargate-task-role",
 	executionRoleArn="arn:aws:iam::136638793011:role/ecsTaskExecutionRole")

AGENT.start()
