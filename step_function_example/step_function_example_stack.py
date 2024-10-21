from aws_cdk import (Stack, aws_stepfunctions as sfn, aws_stepfunctions_tasks as tasks, aws_lambda as _lambda)
from constructs import Construct

class StepFunctionExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        producer = _lambda.Function(self, "Producer",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/producer"))

        consumer = _lambda.Function(self, "Consumer",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/consumer"))

        producer_task = tasks.LambdaInvoke(self, "ProducerTask", 
            lambda_function=producer,
            output_path="$.Payload")

        consumer_task = tasks.LambdaInvoke(self, "ConsumerTask", 
            lambda_function=consumer)

        definition = producer_task.next(consumer_task)

        sfn.StateMachine(self, "ProducerConsumerSfn", definition=definition)
