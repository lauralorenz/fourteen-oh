from prefect.storage import GitHub
from prefect.run_configs import ECSRun
from prefect.executors import DaskExecutor
from prefect import task, Flow, Parameter
import prefect

STORAGE = GitHub(repo="lauralorenz/fourteen-oh", ref="main", path="/14-fargate-executor.py")

RUN_CONFIG = ECSRun(
	run_task_kwargs={
		#"networkMode":"awsvpc",
		#"taskDefinition":"14-fargate",
		"cluster":"prefect-demo-cluster",
	 	"networkConfiguration": {'awsvpcConfiguration': {'assignPublicIp': 'ENABLED', 'subnets': ['subnet-7410175c'], 'securityGroups': []}},
 		#"executionRoleArn": "arn:aws:iam::136638793011:role/ecsTaskExecutionRole"
 		},
	task_role_arn="arn:aws:iam::136638793011:role/prefect-demo-fargate-task-role",
	image='prefecthq/prefect:0.14.0',
	memory="512", 
	cpu="256")

EXECUTOR = DaskExecutor(
    cluster_class="dask_cloudprovider.aws.FargateCluster",
    cluster_kwargs={"n_workers": 4, "image": 'prefecthq/prefect:0.14.0'})


@task
def hi():
   logger = prefect.context.get('logger')
   logger.info("Hello!")


with Flow("prefect-14-dask", storage=STORAGE, run_config=RUN_CONFIG, executor=EXECUTOR) as flow:
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
