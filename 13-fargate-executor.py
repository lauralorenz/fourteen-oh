from prefect.environments.storage import S3
from prefect.environments import FargateTaskEnvironment
from prefect.engine.executors import DaskExecutor, LocalDaskExecutor
from prefect import task, Flow, Parameter
import prefect

STORAGE = S3(bucket="demo-prefect-flows-14")

ENVIRONMENT = FargateTaskEnvironment(
		networkMode="awsvpc",
		family="13-fargate-dask", 
		taskDefinition="13-fargate-dask",
		cpu="256",  
		memory="512", 
		cluster="prefect-demo-cluster",
	 	networkConfiguration={'awsvpcConfiguration': {'assignPublicIp': 'ENABLED', 'subnets': ['subnet-7410175c'], 'securityGroups': []}},
	 	taskRoleArn="arn:aws:iam::136638793011:role/prefect-demo-fargate-task-role",
 		executionRoleArn="arn:aws:iam::136638793011:role/ecsTaskExecutionRole",
	  	metadata={"image":'prefecthq/prefect:all_extras-0.13.19'},
	  	executor=DaskExecutor(cluster_class="dask_cloudprovider.aws.FargateCluster",
    			cluster_kwargs={"n_workers": 4, "image": "prefecthq/prefect:all_extras-0.13.19"}))

@task
def hi():
   logger = prefect.context.get('logger')
   logger.info("Hello!")


with Flow("prefect-13-dask", storage=STORAGE, environment=ENVIRONMENT) as flow:
	hi()

# if __name__ == '__main__':
# 	import logging
# 	import sys
# 	logger = logging.getLogger('distributed.scheduler')
# 	logger.setLevel('DEBUG')
# 	log_stream = logging.StreamHandler(sys.stdout)
# 	logger.addHandler(log_stream)


# 	flow.run()
	
	#flow.run(executor=DaskExecutor(cluster_kwargs={"n_workers": 4, "threads_per_worker": 2}))

flow.register("14-demo")

#########
# agent #
#########

if __name__ == "__main__":
	from prefect.agent.fargate import FargateAgent

	AGENT = FargateAgent(labels=["s3-flow-storage"],
		cpu="256", 
		memory="512",
		cluster="prefect-demo-cluster", 
		networkConfiguration={'awsvpcConfiguration': {'assignPublicIp': 'ENABLED', 'subnets': ['subnet-7410175c'], 'securityGroups': []}}, 
		taskRoleArn="arn:aws:iam::136638793011:role/prefect-demo-fargate-task-role",
	 	executionRoleArn="arn:aws:iam::136638793011:role/ecsTaskExecutionRole",
	 	enable_task_revisions=True)

	AGENT.start()
