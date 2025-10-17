#!/usr/bin/env python3
"""
Remote command execution via SSH.
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json


class RemoteHost:
    """Represents a remote host configuration."""
    
    def __init__(
        self,
        name: str,
        hostname: str,
        user: str,
        port: int = 22,
        key_file: Optional[str] = None
    ):
        self.name = name
        self.hostname = hostname
        self.user = user
        self.port = port
        self.key_file = key_file
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "hostname": self.hostname,
            "user": self.user,
            "port": self.port,
            "key_file": self.key_file
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RemoteHost':
        """Create from dictionary."""
        return cls(
            name=data["name"],
            hostname=data["hostname"],
            user=data["user"],
            port=data.get("port", 22),
            key_file=data.get("key_file")
        )


class RemoteExecutor:
    """Execute commands on remote hosts."""
    
    def __init__(self):
        self.hosts_file = Path.home() / ".prometheus" / "remote_hosts.json"
        self.hosts = self._load_hosts()
    
    def _load_hosts(self) -> Dict[str, RemoteHost]:
        """Load remote hosts configuration."""
        if self.hosts_file.exists():
            try:
                with open(self.hosts_file, 'r') as f:
                    data = json.load(f)
                return {
                    name: RemoteHost.from_dict(host_data)
                    for name, host_data in data.items()
                }
            except:
                return {}
        return {}
    
    def _save_hosts(self):
        """Save hosts configuration."""
        self.hosts_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            name: host.to_dict()
            for name, host in self.hosts.items()
        }
        
        with open(self.hosts_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_host(
        self,
        name: str,
        hostname: str,
        user: str,
        port: int = 22,
        key_file: Optional[str] = None
    ) -> bool:
        """Add a remote host."""
        if name in self.hosts:
            return False
        
        self.hosts[name] = RemoteHost(name, hostname, user, port, key_file)
        self._save_hosts()
        return True
    
    def remove_host(self, name: str) -> bool:
        """Remove a remote host."""
        if name in self.hosts:
            del self.hosts[name]
            self._save_hosts()
            return True
        return False
    
    def list_hosts(self) -> List[RemoteHost]:
        """List all configured hosts."""
        return list(self.hosts.values())
    
    def get_host(self, name: str) -> Optional[RemoteHost]:
        """Get host by name."""
        return self.hosts.get(name)
    
    def execute_on_host(
        self,
        host_name: str,
        command: str,
        timeout: int = 30
    ) -> Tuple[bool, str]:
        """
        Execute command on remote host.
        
        Args:
            host_name: Name of configured host
            command: Command to execute
            timeout: Timeout in seconds
        
        Returns:
            Tuple of (success, output)
        """
        host = self.get_host(host_name)
        if not host:
            return False, f"Host '{host_name}' not found"
        
        # Build SSH command
        ssh_cmd = ["ssh"]
        
        # Add port
        if host.port != 22:
            ssh_cmd.extend(["-p", str(host.port)])
        
        # Add key file
        if host.key_file:
            ssh_cmd.extend(["-i", host.key_file])
        
        # Add host and command
        ssh_cmd.append(f"{host.user}@{host.hostname}")
        ssh_cmd.append(command)
        
        try:
            result = subprocess.run(
                ssh_cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {timeout}s"
        except Exception as e:
            return False, f"SSH error: {str(e)}"
    
    def execute_on_multiple(
        self,
        host_names: List[str],
        command: str,
        parallel: bool = True
    ) -> Dict[str, Tuple[bool, str]]:
        """
        Execute command on multiple hosts.
        
        Args:
            host_names: List of host names
            command: Command to execute
            parallel: Whether to execute in parallel
        
        Returns:
            Dict mapping host name to (success, output)
        """
        results = {}
        
        if parallel:
            # Simple parallel execution using subprocess
            import concurrent.futures
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(self.execute_on_host, name, command): name
                    for name in host_names
                }
                
                for future in concurrent.futures.as_completed(futures):
                    host_name = futures[future]
                    try:
                        results[host_name] = future.result()
                    except Exception as e:
                        results[host_name] = (False, str(e))
        else:
            # Sequential execution
            for host_name in host_names:
                results[host_name] = self.execute_on_host(host_name, command)
        
        return results
    
    def test_connection(self, host_name: str) -> Tuple[bool, str]:
        """Test connection to host."""
        return self.execute_on_host(host_name, "echo 'Connection OK'", timeout=10)
    
    def copy_file_to_host(
        self,
        host_name: str,
        local_path: str,
        remote_path: str
    ) -> Tuple[bool, str]:
        """
        Copy file to remote host using SCP.
        
        Args:
            host_name: Name of configured host
            local_path: Local file path
            remote_path: Remote file path
        
        Returns:
            Tuple of (success, output)
        """
        host = self.get_host(host_name)
        if not host:
            return False, f"Host '{host_name}' not found"
        
        # Build SCP command
        scp_cmd = ["scp"]
        
        if host.port != 22:
            scp_cmd.extend(["-P", str(host.port)])
        
        if host.key_file:
            scp_cmd.extend(["-i", host.key_file])
        
        scp_cmd.append(local_path)
        scp_cmd.append(f"{host.user}@{host.hostname}:{remote_path}")
        
        try:
            result = subprocess.run(
                scp_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"SCP error: {str(e)}"


# Global executor instance
_remote_executor = None


def get_remote_executor() -> RemoteExecutor:
    """Get global remote executor instance."""
    global _remote_executor
    if _remote_executor is None:
        _remote_executor = RemoteExecutor()
    return _remote_executor


def show_remote_hosts():
    """Display configured remote hosts."""
    from rich.console import Console
    from rich.table import Table
    
    executor = get_remote_executor()
    hosts = executor.list_hosts()
    
    if not hosts:
        console = Console()
        console.print("[yellow]No remote hosts configured[/yellow]")
        console.print("[dim]Add a host: remote add <name> <user@hostname>[/dim]")
        return
    
    table = Table(title="Remote Hosts", border_style="cyan")
    table.add_column("Name", style="cyan")
    table.add_column("User", style="bright_white")
    table.add_column("Hostname", style="bright_white")
    table.add_column("Port", justify="center")
    table.add_column("Key", style="dim")
    
    for host in hosts:
        key_info = "✓" if host.key_file else "-"
        table.add_row(
            host.name,
            host.user,
            host.hostname,
            str(host.port),
            key_info
        )
    
    console = Console()
    console.print(table)
    console.print(f"\n[dim]Total: {len(hosts)} hosts[/dim]")
    console.print("[dim]Execute on host: remote exec <host> <command>[/dim]")


def execute_remote_command(host_name: str, command: str):
    """Execute command on remote host and display result."""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    executor = get_remote_executor()
    
    console.print(f"[cyan]Executing on {host_name}...[/cyan]")
    
    success, output = executor.execute_on_host(host_name, command)
    
    if success:
        console.print(Panel(
            f"[bold green]✓ Success[/bold green]\n\n{output}",
            title=f"[bold]Result from {host_name}[/bold]",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]✗ Failed[/bold red]\n\n{output}",
            title=f"[bold]Result from {host_name}[/bold]",
            border_style="red"
        ))


def execute_on_multiple_hosts(host_names: List[str], command: str):
    """Execute command on multiple hosts and display results."""
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    executor = get_remote_executor()
    
    console.print(f"[cyan]Executing on {len(host_names)} hosts...[/cyan]")
    
    results = executor.execute_on_multiple(host_names, command, parallel=True)
    
    table = Table(title="Execution Results", border_style="cyan")
    table.add_column("Host", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Output", style="bright_white")
    
    for host_name, (success, output) in results.items():
        status = "[green]✓[/green]" if success else "[red]✗[/red]"
        output_preview = output[:100] + "..." if len(output) > 100 else output
        table.add_row(host_name, status, output_preview)
    
    console.print(table)
    
    # Summary
    success_count = sum(1 for success, _ in results.values() if success)
    console.print(f"\n[dim]Succeeded: {success_count}/{len(host_names)}[/dim]")
