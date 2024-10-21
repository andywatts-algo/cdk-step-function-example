from aws_cdk import (Stack, aws_stepfunctions as sfn, aws_stepfunctions_tasks as tasks, 
                     aws_lambda as _lambda, aws_dynamodb as ddb)
from constructs import Construct

class StepFunctionExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DYNAMODB TABLE
        table = ddb.Table(self, "ExampleTable",
            table_name="cdk_producer_consumer_example",
            partition_key=ddb.Attribute(name="id", type=ddb.AttributeType.STRING),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST)  # This line makes it on-demand

        # LAMBDA LAYER
        layer = _lambda.LayerVersion(self, "CDKProducerConsumerSharedLayer",
            code=_lambda.Code.from_asset("lambda/layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9])

        # LAMBDA FUNCTIONS
        producer = _lambda.Function(self, "Producer",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/producer"),
            environment={"TABLE_NAME": table.table_name},
            layers=[layer])

        consumer = _lambda.Function(self, "Consumer",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/consumer"),
            environment={"TABLE_NAME": table.table_name},
            layers=[layer])

        # DYNAMODB PERMISSIONS
        table.grant_read_write_data(producer)
        table.grant_read_data(consumer)

        # STEP FUNCTION
        definition = tasks.LambdaInvoke(self, "ProducerTask", 
            lambda_function=producer,
            output_path="$.Payload"
        ).next(tasks.LambdaInvoke(self, "ConsumerTask", 
            lambda_function=consumer))

        sfn.StateMachine(self, "ProducerConsumerSfn", 
            definition_body=sfn.DefinitionBody.from_chainable(definition))
