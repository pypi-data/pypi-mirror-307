import os
import asyncio
from typing import Optional, Dict, Any, List
from temporalio.client import Client, ScheduleSpec
from temporalio.worker import Worker
from temporalio import workflow as temporal_workflow
from dataclasses import dataclass

from .playground.workflow import playgroundRun
from .observability import log_with_context, logger

@dataclass
class CloudConnectionOptions:
    engine_id: str
    api_key: str
    address: Optional[str] = "localhost:7233"
    temporal_namespace: Optional[str] = "default"

@dataclass
class ServiceOptions:
    rate_limit: Optional[int] = 100000
    max_concurrent_workflow_runs: Optional[int] = 3000
    max_concurrent_function_runs: Optional[int] = 1000

class Restack:
    api_key: Optional[str] = None
    client: Optional[Client] = None
    options: Optional[CloudConnectionOptions] = None
    functions: Optional[List[Any]] = None

    def __init__(self, options: Optional[CloudConnectionOptions] = None):
        super().__init__()
        self.client = None
        self.options = options
        log_with_context("DEBUG", "Restack instance initialized", options=str(options))

    def get_connection_options(self) -> Dict[str, Any]:
        target_host = self.options.address if self.options else 'localhost:7233'
        engine_id = self.options.engine_id if self.options else 'local'
        options = {
            "target_host": target_host,
            "metadata": {
                "restack-engineId": engine_id,
            }
        }
        if self.options and self.options.api_key:
            options["tls"] = not target_host.startswith("localhost")
            options["api_key"] = self.options.api_key
        return options
    
    async def connect(self, connection_options: Optional[CloudConnectionOptions] = None):
        if self.client:
            log_with_context("INFO", "Reusing existing client connection")
            return
        try:
            self.client = await self.create_client(connection_options)
            log_with_context("INFO", "Connected to Restack Engine")
        except Exception as e:
            log_with_context("ERROR", "Failed to connect to Restack Engine", error=str(e))
            raise e

    async def create_client(self, connection_options: Optional[CloudConnectionOptions] = None) -> Client:
        connect_options = connection_options or self.get_connection_options()
        namespace = self.options.temporal_namespace if self.options else 'default'

        return await Client.connect(
            connect_options['target_host'],
            namespace=namespace
        )

    async def create_service(self, workflows: Optional[List[Any]] = None, functions: Optional[List[Any]] = None, task_queue: Optional[str] = None,options: Optional[ServiceOptions] = None) -> Worker:
        try:
            log_with_context("INFO", "Starting service...")
            client = await self.create_client()
            engine_id = self.get_connection_options()['metadata']['restack-engineId']

            service = Worker(
                identity=f"{engine_id}-{os.getpid()}@{os.uname().nodename}",
                client=client,
                task_queue=task_queue or "restack",
                workflows=workflows or [],
                activities=functions or [],
                max_activities_per_second=options.rate_limit,
                max_concurrent_activities=options.max_concurrent_function_runs,
                max_concurrent_workflow_tasks=options.max_concurrent_workflow_runs,
            )
            log_with_context("INFO", "Service created successfully")
            return service
        except Exception as e:
            if e.__cause__ and "http.client.incompleteread.__mro_entries__".lower() in str(e.__cause__).lower():
                log_with_context("ERROR", "Failed to start service: Functions in workflow steps need to be imported with import_functions(). See docs at https://docs.restack.io/libraries/python/reference/workflows")
            else:
                log_with_context("ERROR", "Failed to start service", error=str(e))
            raise e

    async def run_service(self, service: Worker):
        try:
            if service.task_queue == "restack":
                log_with_context("INFO", "Creating playground service...")

                playground_service = Worker(
                    identity=f"{os.getpid()}@{os.uname().nodename}-playground",
                    client=service.client,
                    task_queue="playground",
                    workflows=[playgroundRun],
                )

                log_with_context("INFO", "Services ready to receive workflows and events")
                await asyncio.gather(service.run(), playground_service.run())
            else:
                log_with_context("INFO", "Service ready to receive workflows and events")
                await service.run()
        except Exception as e:
            log_with_context("ERROR", "Failed to run service", error=str(e))
            raise e

    async def start_service(
        self,
        workflows: Optional[List[Any]] = None,
        functions: Optional[List[Any]] = None,
        task_queue: Optional[str] = None,
        options: Optional[ServiceOptions] = None
    ):
        """
        Start a service with the specified configurations.

        Parameters:
        - workflows (Optional[List[Any]]): A list of workflows to be used.
        - functions (Optional[List[Any]]): A list of functions to be used. 
        - task_queue (Optional[str]): The task queue name. 
        - options (Optional[ServiceOptions]): Service options for rate limiting and concurrency.
        """
        service = await self.create_service(
            task_queue=task_queue,
            workflows=workflows,
            functions=functions or [],
            options=options or ServiceOptions()
        )
        await self.run_service(service)

    async def schedule_workflow(self, workflow_name: str, workflow_id: str, input: Optional[Dict[str, Any]] = None, schedule: Optional[ScheduleSpec] = None, task_queue: Optional[str] = 'restack') -> str:
        await self.connect()
        if self.client:
            try:
                connection_options = self.get_connection_options()
                engine_id = connection_options['metadata']['restack-engineId']

                if not schedule:
                    handle = await self.client.start_workflow(
                        workflow_name,
                        args=[input] if input else [],
                        id=f"{engine_id}-{workflow_id}",
                        memo={'engineId': engine_id},
                        search_attributes={'engineId': [engine_id]},
                        task_queue=task_queue,
                    )
                    log_with_context("INFO", "Workflow started immediately", run_id=handle.first_execution_run_id)
                    return handle.first_execution_run_id
                else:
                    scheduled = await self.client.create_schedule(
                        id=f"{engine_id}-{workflow_id}",
                        schedule=schedule,
                        action=Client.ScheduleActionStartWorkflow(
                            workflow_name,
                            args=[input] if input else [],
                        ),
                        memo={'engineId': engine_id},
                        search_attributes={'engineId': [engine_id]},
                        task_queue=task_queue,
                    )
                    log_with_context("INFO", "Workflow scheduled", schedule_id=scheduled.schedule_id)
                    return scheduled.schedule_id
            except Exception as e:
                log_with_context("ERROR", "Failed to start or schedule workflow", error=str(e))
                raise e
        else:
            raise Exception("Workflow result not retrieved due to failed connection.")

    async def get_workflow_handle(self, workflow_id: str, run_id: str):
        await self.connect()
        if self.client:
            try:
                connection_options = self.get_connection_options()
                engine_id = connection_options['metadata']['restack-engineId']
                return self.client.get_workflow_handle(f"{engine_id}-{workflow_id}", run_id=run_id)
            except Exception as e:
                log_with_context("ERROR", "Failed to get workflow result", error=str(e))
                raise e
        else:
            raise Exception("Workflow result not retrieved due to failed connection.")

    async def get_workflow_result(self, workflow_id: str, run_id: str) -> Any:
        handle = await self.get_workflow_handle(workflow_id, run_id)
        try:
            return await handle.result()
        except Exception as e:
            log_with_context("ERROR", "Failed to get workflow result", error=str(e))
            raise e

    async def get_workflow_memory(self, workflow_id: str, run_id: str, memory_name: str) -> Any:
        handle = await self.get_workflow_handle(workflow_id, run_id)
        try:
            return await handle.query(memory_name)
        except Exception as e:
            log_with_context("ERROR", "Failed to get workflow memory", error=str(e))
            raise e
    
    async def send_workflow_event(self, event_name: str, workflow_id: str, run_id: Optional[str] = None, event_input: Optional[Dict[str, Any]] = None):
        handle = await self.get_workflow_handle(workflow_id, run_id)
        try:
            return await handle.execute_update(event_name, event_input)
        except Exception as e:
            log_with_context("ERROR", "Failed to send workflow event", error=str(e))
            raise e