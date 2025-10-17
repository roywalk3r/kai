#!/usr/bin/env python3
"""
Command chaining and piping system.
"""

import re
import subprocess
from typing import List, Dict, Tuple, Optional
from enum import Enum


class ChainOperator(Enum):
    """Command chain operators."""
    PIPE = "|"  # Pipe output to next command
    AND = "&&"  # Run next if previous succeeds
    OR = "||"  # Run next if previous fails
    SEMICOLON = ";"  # Run next regardless
    AMPERSAND = "&"  # Run in background


class CommandChain:
    """Parse and execute command chains."""
    
    def __init__(self):
        self.commands = []
        self.operators = []
    
    def parse(self, chain_str: str) -> bool:
        """
        Parse command chain string.
        
        Args:
            chain_str: Command chain string
        
        Returns:
            True if parsed successfully
        """
        # Split by operators while preserving the operators
        pattern = r'(\|\||&&|\||;|&)'
        parts = re.split(pattern, chain_str)
        
        self.commands = []
        self.operators = []
        
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            
            if part in ['||', '&&', '|', ';', '&']:
                if part == '||':
                    self.operators.append(ChainOperator.OR)
                elif part == '&&':
                    self.operators.append(ChainOperator.AND)
                elif part == '|':
                    self.operators.append(ChainOperator.PIPE)
                elif part == ';':
                    self.operators.append(ChainOperator.SEMICOLON)
                elif part == '&':
                    self.operators.append(ChainOperator.AMPERSAND)
            else:
                self.commands.append(part)
        
        return len(self.commands) > 0
    
    def execute(self, executor_func, ai_model=None) -> List[Dict]:
        """
        Execute command chain.
        
        Args:
            executor_func: Function to execute individual commands
            ai_model: Optional AI model for command generation
        
        Returns:
            List of execution results
        """
        results = []
        previous_output = ""
        previous_success = True
        
        for i, command in enumerate(self.commands):
            # Check if we should execute this command
            if i > 0:
                operator = self.operators[i - 1]
                
                if operator == ChainOperator.AND and not previous_success:
                    results.append({
                        "command": command,
                        "skipped": True,
                        "reason": "Previous command failed"
                    })
                    continue
                
                if operator == ChainOperator.OR and previous_success:
                    results.append({
                        "command": command,
                        "skipped": True,
                        "reason": "Previous command succeeded"
                    })
                    continue
                
                # For pipe, append previous output to command
                if operator == ChainOperator.PIPE and previous_output:
                    # Inject previous output into command context
                    command = f"{command} (using previous output)"
            
            # Execute command
            try:
                if ai_model:
                    # Generate actual command from natural language
                    response = ai_model.generate_command(command)
                    actual_command = response.get("command", command)
                else:
                    actual_command = command
                
                # Execute
                success, output = executor_func(actual_command)
                
                results.append({
                    "command": command,
                    "actual_command": actual_command,
                    "success": success,
                    "output": output,
                    "skipped": False
                })
                
                previous_success = success
                previous_output = output
                
            except Exception as e:
                results.append({
                    "command": command,
                    "success": False,
                    "error": str(e),
                    "skipped": False
                })
                previous_success = False
        
        return results
    
    def is_chain(self, query: str) -> bool:
        """Check if query contains chain operators."""
        return any(op in query for op in ['||', '&&', '|', ';'])


def parse_command_chain(chain_str: str) -> CommandChain:
    """Parse command chain from string."""
    chain = CommandChain()
    chain.parse(chain_str)
    return chain


def is_command_chain(query: str) -> bool:
    """Check if query is a command chain."""
    return CommandChain().is_chain(query)


def execute_chain(chain_str: str, executor_func, ai_model=None) -> List[Dict]:
    """Execute a command chain."""
    chain = parse_command_chain(chain_str)
    return chain.execute(executor_func, ai_model)


class PipelineBuilder:
    """Build command pipelines interactively."""
    
    def __init__(self):
        self.steps = []
    
    def add_step(self, command: str, operator: ChainOperator = ChainOperator.PIPE):
        """Add a step to the pipeline."""
        self.steps.append((command, operator))
    
    def build(self) -> str:
        """Build the command chain string."""
        if not self.steps:
            return ""
        
        parts = [self.steps[0][0]]
        
        for i in range(1, len(self.steps)):
            command, operator = self.steps[i]
            parts.append(operator.value)
            parts.append(command)
        
        return " ".join(parts)
    
    def clear(self):
        """Clear all steps."""
        self.steps.clear()


def format_chain_results(results: List[Dict]) -> str:
    """Format chain execution results for display."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    
    console = Console()
    output_lines = []
    
    for i, result in enumerate(results, 1):
        command = result.get("command", "")
        
        if result.get("skipped"):
            output_lines.append(f"[dim]{i}. {command} (skipped: {result.get('reason')})[/dim]")
        elif result.get("success"):
            output_lines.append(f"[green]✓ {i}. {command}[/green]")
            if result.get("output"):
                output_lines.append(f"[dim]{result['output'][:200]}[/dim]")
        else:
            output_lines.append(f"[red]✗ {i}. {command}[/red]")
            if result.get("error"):
                output_lines.append(f"[red]{result['error']}[/red]")
    
    return "\n".join(output_lines)
