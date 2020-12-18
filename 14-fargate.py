from prefect.storage import GitHub
from prefect.run_configs import ECSRun
from prefect import task, Flow, Parameter
import prefect

STORAGE = GitHub(repo="lauralorenz/fourteen-oh", ref="main", path="/14-fargate.py")

RUN_CONFIG = ECSRun(
	run_task_kwargs={
		#"networkMode":"awsvpc",
		#"taskDefinition":"14-fargate",
		"cluster":"prefect-demo-cluster",
	 	"networkConfiguration": {'awsvpcConfiguration': {'assignPublicIp': 'ENABLED', 'subnets': ['subnet-7410175c'], 'securityGroups': []}},
 		#"executionRoleArn": "arn:aws:iam::136638793011:role/ecsTaskExecutionRole"
 		},
	task_role_arn="arn:aws:iam::136638793011:role/prefect-demo-fargate-task-role",
	#image='prefecthq/prefect:all_extras-0.13.19',
	memory="512", 
	cpu="256")

@task
def hi():
   logger = prefect.context.get('logger')
   logger.info("Hello!")


with Flow("prefect-14", storage=STORAGE, run_config=RUN_CONFIG) as flow:
	hi()

flow.register("14-demo")

#########
# agent #
#########

if __name__ == '__main__':
	from prefect.agent.ecs.agent import ECSAgent

	AGENT = ECSAgent(#labels=["s3-flow-storage"],
		#cpu="256", 
		#memory="512",
		cluster="prefect-demo-cluster", 
		#networkConfiguration={'awsvpcConfiguration': {'assignPublicIp': 'ENABLED', 'subnets': ['subnet-7410175c'], 'securityGroups': []}}, 
		task_role_arn="arn:aws:iam::136638793011:role/prefect-demo-fargate-task-role",
	 	#executionRoleArn="arn:aws:iam::136638793011:role/ecsTaskExecutionRole"
	 	)

	AGENT.start()
