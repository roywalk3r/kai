#!/usr/bin/env python3
"""
Workflow automation system for multi-step command sequences.
"""

import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class StepCondition(Enum):
    """Conditions for step execution."""
    ALWAYS = "always"
    ON_SUCCESS = "on_success"
    ON_FAILURE = "on_failure"


class WorkflowStep:
    """Single step in a workflow."""
    
    def __init__(
        self,
        name: str,
        command: str,
        condition: StepCondition = StepCondition.ALWAYS,
        timeout: int = 300,
        retry: int = 0,
        continue_on_error: bool = False
    ):
        self.name = name
        self.command = command
        self.condition = condition
        self.timeout = timeout
        self.retry = retry
        self.continue_on_error = continue_on_error
        self.result = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "command": self.command,
            "condition": self.condition.value,
            "timeout": self.timeout,
            "retry": self.retry,
            "continue_on_error": self.continue_on_error
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'WorkflowStep':
        """Create from dictionary."""
        condition_str = data.get("condition", "always")
        condition = StepCondition(condition_str) if condition_str in [c.value for c in StepCondition] else StepCondition.ALWAYS
        
        return cls(
            name=data["name"],
            command=data["command"],
            condition=condition,
            timeout=data.get("timeout", 300),
            retry=data.get("retry", 0),
            continue_on_error=data.get("continue_on_error", False)
        )


class Workflow:
    """Automated workflow definition."""
    
    def __init__(
        self,
        name: str,
        description: str,
        steps: List[WorkflowStep],
        variables: Optional[Dict[str, str]] = None,
        category: str = "custom"
    ):
        self.name = name
        self.description = description
        self.steps = steps
        self.variables = variables or {}
        self.category = category
        self.created_at = datetime.now().isoformat()
        self.last_run = None
        self.run_count = 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "variables": self.variables,
            "category": self.category,
            "created_at": self.created_at,
            "last_run": self.last_run,
            "run_count": self.run_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Workflow':
        """Create from dictionary."""
        steps = [WorkflowStep.from_dict(step_data) for step_data in data.get("steps", [])]
        
        workflow = cls(
            name=data["name"],
            description=data["description"],
            steps=steps,
            variables=data.get("variables"),
            category=data.get("category", "custom")
        )
        workflow.created_at = data.get("created_at", datetime.now().isoformat())
        workflow.last_run = data.get("last_run")
        workflow.run_count = data.get("run_count", 0)
        return workflow
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> 'Workflow':
        """Load workflow from YAML file."""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        steps = []
        for step_data in data.get("steps", []):
            steps.append(WorkflowStep(
                name=step_data["name"],
                command=step_data["command"],
                condition=StepCondition(step_data.get("condition", "always")),
                timeout=step_data.get("timeout", 300),
                retry=step_data.get("retry", 0),
                continue_on_error=step_data.get("continue_on_error", False)
            ))
        
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            steps=steps,
            variables=data.get("variables"),
            category=data.get("category", "custom")
        )


class WorkflowExecutor:
    """Execute workflows."""
    
    def __init__(self, executor_func):
        """
        Initialize workflow executor.
        
        Args:
            executor_func: Function to execute individual commands
        """
        self.executor_func = executor_func
        self.execution_log = []
    
    def execute_workflow(
        self,
        workflow: Workflow,
        variables: Optional[Dict[str, str]] = None,
        dry_run: bool = False
    ) -> Dict:
        """
        Execute a workflow.
        
        Args:
            workflow: Workflow to execute
            variables: Override variables
            dry_run: If True, don't actually execute
        
        Returns:
            Execution results
        """
        # Merge variables
        all_variables = {**workflow.variables, **(variables or {})}
        
        results = {
            "workflow": workflow.name,
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "success": True
        }
        
        previous_success = True
        
        for step in workflow.steps:
            # Check condition
            should_execute = self._check_condition(step.condition, previous_success)
            
            if not should_execute:
                results["steps"].append({
                    "name": step.name,
                    "skipped": True,
                    "reason": f"Condition {step.condition.value} not met"
                })
                continue
            
            # Replace variables in command
            command = self._replace_variables(step.command, all_variables)
            
            # Execute step (with retry)
            step_result = self._execute_step(step, command, dry_run)
            results["steps"].append(step_result)
            
            # Update previous success
            previous_success = step_result.get("success", False)
            
            # Check if we should continue
            if not previous_success and not step.continue_on_error:
                results["success"] = False
                break
        
        results["end_time"] = datetime.now().isoformat()
        
        # Update workflow stats
        workflow.last_run = results["start_time"]
        workflow.run_count += 1
        
        return results
    
    def _check_condition(self, condition: StepCondition, previous_success: bool) -> bool:
        """Check if step condition is met."""
        if condition == StepCondition.ALWAYS:
            return True
        elif condition == StepCondition.ON_SUCCESS:
            return previous_success
        elif condition == StepCondition.ON_FAILURE:
            return not previous_success
        return True
    
    def _replace_variables(self, command: str, variables: Dict[str, str]) -> str:
        """Replace variables in command."""
        for var_name, var_value in variables.items():
            command = command.replace(f"${{{var_name}}}", var_value)
            command = command.replace(f"${var_name}", var_value)
        return command
    
    def _execute_step(self, step: WorkflowStep, command: str, dry_run: bool) -> Dict:
        """Execute a single step with retry logic."""
        result = {
            "name": step.name,
            "command": command,
            "attempts": []
        }
        
        attempts = step.retry + 1
        
        for attempt in range(attempts):
            if dry_run:
                attempt_result = {
                    "attempt": attempt + 1,
                    "success": True,
                    "output": "[DRY RUN] Would execute: " + command
                }
            else:
                try:
                    success, output = self.executor_func(command, timeout=step.timeout)
                    attempt_result = {
                        "attempt": attempt + 1,
                        "success": success,
                        "output": output
                    }
                except Exception as e:
                    attempt_result = {
                        "attempt": attempt + 1,
                        "success": False,
                        "error": str(e)
                    }
            
            result["attempts"].append(attempt_result)
            
            if attempt_result["success"]:
                result["success"] = True
                result["output"] = attempt_result["output"]
                break
        else:
            result["success"] = False
            result["error"] = "All retry attempts failed"
        
        return result


class WorkflowManager:
    """Manage workflows."""
    
    def __init__(self):
        self.workflows_dir = Path.home() / ".prometheus" / "workflows"
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        self.workflows_file = self.workflows_dir / "workflows.json"
        self.workflows = self._load_workflows()
        
        # Create built-in workflows if empty
        if not self.workflows:
            self._create_builtin_workflows()
    
    def _load_workflows(self) -> Dict[str, Workflow]:
        """Load workflows from file."""
        if self.workflows_file.exists():
            try:
                with open(self.workflows_file, 'r') as f:
                    data = json.load(f)
                return {
                    name: Workflow.from_dict(wf_data)
                    for name, wf_data in data.items()
                }
            except:
                return {}
        return {}
    
    def _save_workflows(self):
        """Save workflows to file."""
        data = {
            name: workflow.to_dict()
            for name, workflow in self.workflows.items()
        }
        
        with open(self.workflows_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _create_builtin_workflows(self):
        """Create built-in workflows."""
        builtins = [
            Workflow(
                name="deploy",
                description="Standard deployment workflow",
                steps=[
                    WorkflowStep("Pull code", "git pull"),
                    WorkflowStep("Install dependencies", "pip install -r requirements.txt"),
                    WorkflowStep("Run tests", "pytest", continue_on_error=True),
                    WorkflowStep("Deploy", "./deploy.sh")
                ],
                category="deployment"
            ),
            Workflow(
                name="backup-project",
                description="Backup project files",
                steps=[
                    WorkflowStep("Create backup directory", "mkdir -p ~/backups"),
                    WorkflowStep("Archive project", "tar -czf ~/backups/project_$(date +%Y%m%d).tar.gz ."),
                    WorkflowStep("List backups", "ls -lh ~/backups/")
                ],
                category="maintenance"
            ),
            Workflow(
                name="system-update",
                description="Update system packages",
                steps=[
                    WorkflowStep("Update package list", "sudo apt update"),
                    WorkflowStep("Upgrade packages", "sudo apt upgrade -y"),
                    WorkflowStep("Clean cache", "sudo apt autoremove -y")
                ],
                category="system"
            ),
            Workflow(
                name="docker-rebuild",
                description="Rebuild and restart Docker containers",
                steps=[
                    WorkflowStep("Stop containers", "docker-compose down"),
                    WorkflowStep("Pull images", "docker-compose pull"),
                    WorkflowStep("Rebuild", "docker-compose build --no-cache"),
                    WorkflowStep("Start", "docker-compose up -d")
                ],
                category="docker"
            ),
        ]
        
        for workflow in builtins:
            self.workflows[workflow.name] = workflow
        
        self._save_workflows()
    
    def create_workflow(self, workflow: Workflow) -> bool:
        """Create a new workflow."""
        if workflow.name in self.workflows:
            return False
        
        self.workflows[workflow.name] = workflow
        self._save_workflows()
        return True
    
    def get_workflow(self, name: str) -> Optional[Workflow]:
        """Get workflow by name."""
        return self.workflows.get(name)
    
    def delete_workflow(self, name: str) -> bool:
        """Delete a workflow."""
        if name in self.workflows:
            del self.workflows[name]
            self._save_workflows()
            return True
        return False
    
    def list_workflows(self, category: Optional[str] = None) -> List[Workflow]:
        """List workflows."""
        workflows = list(self.workflows.values())
        
        if category:
            workflows = [wf for wf in workflows if wf.category == category]
        
        return sorted(workflows, key=lambda w: w.name)
    
    def import_workflow_file(self, yaml_path: Path) -> bool:
        """Import workflow from YAML file."""
        try:
            workflow = Workflow.from_yaml(yaml_path)
            return self.create_workflow(workflow)
        except:
            return False


# Global workflow manager
_workflow_manager = None


def get_workflow_manager() -> WorkflowManager:
    """Get global workflow manager instance."""
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = WorkflowManager()
    return _workflow_manager


def show_workflows():
    """Display available workflows."""
    from rich.console import Console
    from rich.table import Table
    
    manager = get_workflow_manager()
    workflows = manager.list_workflows()
    
    if not workflows:
        console = Console()
        console.print("[yellow]No workflows defined[/yellow]")
        return
    
    table = Table(title="Workflows", border_style="cyan")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="bright_white")
    table.add_column("Steps", justify="center")
    table.add_column("Category", style="dim")
    table.add_column("Runs", justify="center", style="dim")
    
    for workflow in workflows:
        table.add_row(
            workflow.name,
            workflow.description,
            str(len(workflow.steps)),
            workflow.category,
            str(workflow.run_count)
        )
    
    console = Console()
    console.print(table)
    console.print(f"\n[dim]Total: {len(workflows)} workflows[/dim]")
    console.print("[dim]Run workflow: workflow run <name>[/dim]")


def show_workflow_details(name: str):
    """Show workflow details."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    
    manager = get_workflow_manager()
    workflow = manager.get_workflow(name)
    
    if not workflow:
        console = Console()
        console.print(f"[red]Workflow '{name}' not found[/red]")
        return
    
    console = Console()
    
    # Workflow info
    console.print(Panel(
        f"[bold bright_cyan]Name:[/bold bright_cyan] {workflow.name}\n"
        f"[bold bright_cyan]Description:[/bold bright_cyan] {workflow.description}\n"
        f"[bold bright_cyan]Category:[/bold bright_cyan] {workflow.category}\n"
        f"[bold bright_cyan]Steps:[/bold bright_cyan] {len(workflow.steps)}\n"
        f"[bold bright_cyan]Run Count:[/bold bright_cyan] {workflow.run_count}",
        title="[bold]Workflow Details[/bold]",
        border_style="cyan"
    ))
    
    # Variables
    if workflow.variables:
        console.print("\n[bold]Variables:[/bold]")
        for var, value in workflow.variables.items():
            console.print(f"  • ${{{var}}} = {value}")
    
    # Steps
    console.print("\n[bold]Steps:[/bold]")
    table = Table(border_style="cyan")
    table.add_column("#", style="dim", width=3)
    table.add_column("Name", style="cyan")
    table.add_column("Command", style="bright_white")
    table.add_column("Condition", style="dim")
    
    for i, step in enumerate(workflow.steps, 1):
        table.add_row(
            str(i),
            step.name,
            step.command[:50] + "..." if len(step.command) > 50 else step.command,
            step.condition.value
        )
    
    console.print(table)
