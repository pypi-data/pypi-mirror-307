from pydantic import BaseModel
from temporalio import workflow

class PlaygroundInput(BaseModel):
    function_name: str
    task_queue: str
    input: any

@workflow.defn
class PlaygroundWorkflow:
    @workflow.run
    async def run(self, params: PlaygroundInput):
        result = await workflow.execute_activity(
            activity=params.function_name,
            task_queue=params.task_queue,
            args=[params.input]
        )
        return result