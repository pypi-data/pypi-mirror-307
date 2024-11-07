""" Shared pipeline configuration utility. """
import uuid
from typing import List, Optional, Dict, Union
from ipulse_shared_base_ftredge import (DataActionType, DataSourceType, DatasetScope)


class PipelineTask:
    """
    Represents a single task in a pipeline.
    """
    def __init__(
        self,
        n: str,
        a: Optional[DataActionType] = None,
        s: Optional[DataSourceType] = None,
        d: Optional[DataSourceType] = None,
        scope: Optional[DatasetScope] = None,
        dependencies: Optional[List[str]] = None,
        config: Optional[Dict] = None,
        enabled: bool = True,
    ):
        """
        Initialize a PipelineTask.
        :param n: Name of the task.
        :param s: Source of data for the task.
        :param a: Action to perform.
        :param d: Destination for the task output.
        :param scope: Scope of the dataset being processed.
        :param dependencies: List of task names that this task depends on.
        :param config: Task-specific configuration.
        :param enabled: Whether the task is enabled.
        """
        self.id=uuid.uuid4()
        self.name = n
        self.action = a
        self.source = s
        self.destination = d
        self.data_scope = scope
        self.dependencies = dependencies or []
        self.config = config or {}
        self.enabled = enabled

    def __str__(self):
        parts = [self.name]
        if self.action:
            parts.append(self.action.value)
        if self.source:
            parts.append(f"from {self.source.value}")
        if self.destination:
            parts.append(f"to {self.destination.value}")
        if self.data_scope:
            parts.append(f"scope={self.data_scope.value}")
        return " :: ".join(parts)

class PipelineLoopGroup:
    """
    Represents a group of tasks that execute iteratively, with unique name enforcement.
    """

    def __init__(self, name: str, tasks: List[Union['PipelineTask', 'PipelineLoopGroup']]):
        """
        Initialize the PipelineLoopGroup.
        :param name: Name of the loop group.
        :param tasks: List of PipelineTask or nested PipelineLoopGroup.
        """
        self.name = name
        self.tasks: Dict[str, Union['PipelineTask', 'PipelineLoopGroup']] = {}
        for task in tasks:
            if task.name in self.tasks:
                raise ValueError(f"Task or group with name '{task.name}' already exists in group '{self.name}'.")
            self.tasks[task.name] = task

    def get_task(self, name: str):
        """
        Retrieve a task or nested group by name.
        :param name: Name of the task or group to retrieve.
        :return: Task or group with the given name.
        :raises KeyError: If no task or group exists with the given name.
        """
        if name not in self.tasks:
            raise KeyError(f"Task or group with name '{name}' not found in {self.name}.")
        return self.tasks[name]

    def __str__(self):
        """
        Represent the PipelineLoopGroup as a string for pipeline flow.
        """
        inner_flow = "\n".join(str(task) for task in self.tasks.values())
        return f"[{self.name}]\n{inner_flow}"


class PipelineConfig:
    """
    Enhanced Pipeline configuration utility with unique name enforcement.
    """

    def __init__(self):
        self.tasks: Dict[str, Union['PipelineTask', 'PipelineLoopGroup']] = {}

    def add(self, task_or_group: Union['PipelineTask', 'PipelineLoopGroup']):
        """
        Add a task or PipelineLoopGroup to the pipeline.
        :param task_or_group: Single PipelineTask or PipelineLoopGroup.
        """
        if task_or_group.name in self.tasks:
            raise ValueError(f"Task or group with name '{task_or_group.name}' already exists in the pipeline.")
        self.tasks[task_or_group.name] = task_or_group

    def get_task(self, name: str):
        """
        Retrieve a task or group by name.
        :param name: Name of the task or group to retrieve.
        :return: Task or group with the given name.
        :raises KeyError: If no task or group exists with the given name.
        """
        if name not in self.tasks:
            raise KeyError(f"Task or group with name '{name}' not found.")
        return self.tasks[name]

    def get_pipeline_flow(self) -> str:
        """
        Generate the hierarchical pipeline flow description with enhanced formatting.
        :return: String representing the pipeline flow.
        """
        def _generate_flow(task_or_group, indent=0):
            if isinstance(task_or_group, PipelineTask):
                return " " * indent + f">> {str(task_or_group)}"
            elif isinstance(task_or_group, PipelineLoopGroup):
                header = f"{' ' * indent}** {task_or_group.name} **"
                inner_flow = "\n".join(_generate_flow(t, indent + 2) for t in task_or_group.tasks.values())
                return f"{header}\n{inner_flow}"

        return "\n".join(_generate_flow(task) for task in self.tasks.values()) + "\n"