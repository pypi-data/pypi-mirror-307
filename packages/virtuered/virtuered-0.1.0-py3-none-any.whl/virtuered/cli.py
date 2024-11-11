#!/usr/bin/env python3
import argparse
import requests
import json
import time
import os
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich import print as rprint

class VirtueRedCLI:
    def __init__(self, server_url=None):
        # Priority order: 
        # 1. Command line argument
        # 2. Environment variable
        # 3. Config file
        # 4. Default value
        self.server_url = server_url or self._get_server_url()
        self.console = Console()

    def _get_server_url(self):
        """Get server URL from various sources"""
        # Check environment variable
        if 'VIRTUERED_SERVER' in os.environ:
            return os.environ['VIRTUERED_SERVER']

        # Check config file
        config_file = Path.home() / '.virtuered' / 'config.json'
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                    if 'server_url' in config:
                        return config['server_url']
            except Exception:
                pass  # Fall back to default if config file is invalid

        # Default value
        return "http://localhost:4401"

    def configure(self, server_url):
        """Save server configuration"""
        config_dir = Path.home() / '.virtuered'
        config_file = config_dir / 'config.json'
        
        # Create config directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Save configuration
        config = {'server_url': server_url}
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        self.console.print(f"[green]Server URL configured: {server_url}[/green]")
        self.console.print("[yellow]You can override this setting with:[/yellow]")
        self.console.print(f"  1. Command line: virtuered --server {server_url} list")
        self.console.print(f"  2. Environment: export VIRTUERED_SERVER={server_url}")

    def check_server(self):
        """Check if the server is running and accessible"""
        try:
            response = requests.get(f"{self.server_url}/runsinfo")
            response.raise_for_status()
            self.console.print(f"[green]Server is running and accessible at {self.server_url}[/green]")
            return True
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Server is not accessible: {str(e)}[/red]")
            self.console.print(f"[yellow]Make sure the server is running at {self.server_url}[/yellow]")
            return False

    def print_config(self):
        """Print current configuration"""
        self.console.print("\n[bold]Current Configuration:[/bold]")
        self.console.print(f"Server URL: {self.server_url}")
        self.console.print("\n[bold]Configuration Sources:[/bold]")
        
        # Check environment variable
        env_url = os.environ.get('VIRTUERED_SERVER')
        if env_url:
            self.console.print(f"Environment Variable: {env_url}")
        
        # Check config file
        config_file = Path.home() / '.virtuered' / 'config.json'
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                    self.console.print(f"Config File: {config.get('server_url')}")
            except Exception:
                pass

        self.console.print("\n[bold]Override Options:[/bold]")
        self.console.print("1. Command line: virtuered --server URL list")
        self.console.print("2. Environment: export VIRTUERED_SERVER=URL")
        self.console.print("3. Config file: ~/.virtuered/config.json")

    def monitor_progress(self, interval=5):
        """Monitor scan progress"""
        try:
            while True:
                response = requests.get(f"{self.server_url}/api/get_progress")
                response.raise_for_status()
                scans = response.json()
                
                if not scans:  # No active scans
                    self.console.print("[green]No active scans found[/green]")
                    break

                # Check if all scans are completed
                all_completed = all(
                    scan.get('scan_percentage', 0) >= 100 or 
                    scan.get('scanning_status') == 'Finished' 
                    for scan in scans
                )
                
                if all_completed:
                    self.console.print("\n[green]All scans completed![/green]")
                    break

                table = Table(show_header=True, header_style="bold")
                table.add_column("Scan Name")
                table.add_column("Model")
                table.add_column("Status")
                table.add_column("Progress")
                table.add_column("Time Remaining")

                for scan in scans:
                    # Create progress bar
                    progress = min(100, scan.get('scan_percentage', 0))
                    progress_bar = "█" * int(progress / 2) + "-" * (50 - int(progress / 2))
                    
                    status_color = {
                        'Scanning': 'green',
                        'Paused': 'yellow',
                        'Initializing': 'blue'
                    }.get(scan['scanning_status'], 'white')

                    table.add_row(
                        scan['scan_name'],
                        scan['model_name'],
                        f"[{status_color}]{scan['scanning_status']}[/{status_color}]",
                        f"[{status_color}]{progress_bar} {progress:.1f}%[/{status_color}]",
                        scan.get('remaining_time', 'N/A')
                    )

                self.console.clear()
                self.console.print(table)
                self.console.print("\n[yellow]Press Ctrl+C to exit monitoring[/yellow]")
                time.sleep(interval)

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Monitoring stopped by user[/yellow]")
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Error monitoring progress: {str(e)}[/red]")

    def get_runs(self):
        """Get list of all runs"""
        try:
            response = requests.get(f"{self.server_url}/runsinfo")
            response.raise_for_status()
            runs = response.json()
            
            if not runs:
                self.console.print("[yellow]No runs found[/yellow]")
                return []

            # Create and display the table
            table = Table(title="Scan Runs")
            table.add_column("Index", style="blue")
            table.add_column("Scan Name", style="cyan")
            table.add_column("Model", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("Time", style="yellow")
            # table.add_column("Run ID", style="white", no_wrap=False)

            for idx, run in enumerate(runs, 1):
                status_style = {
                    'Finished': 'green',
                    'Scanning': 'blue',
                    'Failed': 'red',
                    'Paused': 'yellow',
                    'Initializing': 'yellow'
                }.get(run['scanning_status'], 'white')
                
                table.add_row(
                    str(idx),
                    run['scan_name'],
                    run['model_name'],
                    f"[{status_style}]{run['scanning_status']}[/{status_style}]",
                    run['scan_time'],
                    # run['filename']
                )

            self.console.print(table)
            return runs

        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Failed to get runs: {str(e)}[/red]")
            return []

    def find_run_by_name_or_id(self, identifier):
        """Helper function to find a run by scan name or full run ID"""
        runs = self.get_runs()  # This will also display the table
        
        # Try to find by index first
        try:
            idx = int(identifier)
            if 1 <= idx <= len(runs):
                return runs[idx-1]['filename']
        except ValueError:
            pass

        # Try to find by scan name or full run ID
        matching_runs = [run for run in runs if 
                        run['scan_name'] == identifier or 
                        run['filename'] == identifier]
        
        if not matching_runs:
            self.console.print(f"[red]No run found with identifier: {identifier}[/red]")
            return None
        elif len(matching_runs) > 1:
            self.console.print(f"[yellow]Multiple runs found with name: {identifier}[/yellow]")
            self.console.print("Please use the index number from the list above.")
            return None
        else:
            return matching_runs[0]['filename']

    def pause_scan(self, identifier):
        """Pause a running scan"""
        run_id = self.find_run_by_name_or_id(identifier)
        if not run_id:
            return False
            
        try:
            payload = {
                "filename": run_id,
                "operation": "pause"
            }
            
            response = requests.post(f"{self.server_url}/api/scan_status", json=payload)
            response.raise_for_status()
            
            self.console.print(f"[green]Successfully paused scan: {run_id}[/green]")
            return True
            
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Failed to pause scan: {str(e)}[/red]")
            return False

    def resume_scan(self, identifier):
        """Resume a paused scan"""
        run_id = self.find_run_by_name_or_id(identifier)
        if not run_id:
            return False
            
        try:
            payload = {
                "filename": run_id,
                "operation": "resume"
            }
            
            response = requests.post(f"{self.server_url}/api/scan_status", json=payload)
            response.raise_for_status()
            
            self.console.print(f"[green]Successfully resumed scan: {run_id}[/green]")
            return True
            
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Failed to resume scan: {str(e)}[/red]")
            return False

    def get_run_summary(self, identifier):
        """Get summary for a specific run"""
        run_id = self.find_run_by_name_or_id(identifier)
        if not run_id:
            return
            
        try:
            response = requests.get(f"{self.server_url}/api/data/{run_id}")
            response.raise_for_status()
            data = response.json()
            
            # Print model name
            self.console.print(f"\n[bold cyan]Model:[/bold cyan] {data['model_name']}\n")
            
            # Print averages
            self.console.print("[bold]Dataset Averages:[/bold]")
            for dataset, score in data['averages'].items():
                self.console.print(f"{dataset}: {score:.2f}%")

            # Print subcategory averages
            self.console.print("\n[bold]Subcategory Averages:[/bold]")
            for dataset, subcats in data['averages_sub'].items():
                self.console.print(f"\n{dataset}:")
                for subcat, score in subcats.items():
                    self.console.print(f"  {subcat}: {score:.2f}%")

            # Print risk scores
            self.console.print("\n[bold]Risk Distribution:[/bold]")
            scores = data['scores']
            total = sum(scores.values())
            for risk, count in scores.items():
                percentage = (count / total * 100) if total > 0 else 0
                color = {
                    'High Risk': 'red',
                    'Low Risk': 'yellow',
                    'No Risk': 'green',
                    'No Response': 'blue'
                }.get(risk, 'white')
                self.console.print(f"[{color}]{risk}: {count} ({percentage:.1f}%)[/{color}]")

        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Failed to get run summary: {str(e)}[/red]")

    def generate_report(self, identifier):
        """Generate and download PDF report"""
        run_id = self.find_run_by_name_or_id(identifier)
        if not run_id:
            self.console.print(f"[red]No run found with identifier: {identifier}[/red]")
            return
            
        try:
            self.console.print("[green]Start generating report ... ")
            response = requests.get(f"{self.server_url}/api/generatepdf/{run_id}")
            response.raise_for_status()
            # Get the current working directory
            cwd = os.getcwd()
            filename = f"report_{run_id}.pdf"
            filepath = os.path.join(cwd, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            self.console.print(f"[green]Report saved at: {filepath}[/green]")
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Failed to generate report: {str(e)}[/red]")
            
    def delete_run(self, identifier):
        """Delete a run and its associated files"""
        run_id = self.find_run_by_name_or_id(identifier)
        if not run_id:
            return False
            
        try:
            # Ask for confirmation before deleting
            self.console.print(f"\n[yellow]Are you sure you want to delete run: {run_id}?[/yellow]")
            self.console.print("[yellow]This action cannot be undone.[/yellow]")
            confirmation = input("Type 'yes' to confirm: ")
            
            if confirmation.lower() != 'yes':
                self.console.print("[yellow]Deletion cancelled[/yellow]")
                return False
            
            payload = {
                "run_name": run_id
            }
            
            response = requests.delete(f"{self.server_url}/api/delete_run", json=payload)
            response.raise_for_status()
            
            self.console.print(f"[green]Successfully deleted run: {run_id}[/green]")
            return True
            
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Failed to delete run: {str(e)}[/red]")
            return False
        
def main():
    parser = argparse.ArgumentParser(description="VirtueAI Redteaming CLI")
    parser.add_argument('--server', default='http://localhost:4401', 
                       help='Server URL (default: http://localhost:4401)')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add configuration commands
    config_parser = subparsers.add_parser('config', help='Configure server settings')
    config_parser.add_argument('server_url', nargs='?', help='Server URL to configure')
    
    # Add show config command
    subparsers.add_parser('show-config', help='Show current configuration')
    
    # Add server status command
    subparsers.add_parser('status', help='Check server status')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Initialize a new scan')
    scan_parser.add_argument('--name', required=True, help='Scan name')
    scan_parser.add_argument('--model', required=True, help='Model name')
    scan_parser.add_argument('--datasets', required=True, help='Datasets (JSON string)')
    scan_parser.add_argument('--extra-args', help='Extra arguments (JSON string)')
    scan_parser.add_argument('--monitor', action='store_true', help='Monitor progress after starting')
    
    # List runs command
    subparsers.add_parser('list', help='List all runs')
    
    # Get summary command
    summary_parser = subparsers.add_parser('summary', help='Get run summary')
    summary_parser.add_argument('identifier', 
                              help='Run identifier (can be index number, scan name, or full run ID)')
    
    # Generate report command
    report_parser = subparsers.add_parser('report', help='Generate PDF report')
    report_parser.add_argument('identifier', 
                             help='Run identifier (can be index number, scan name, or full run ID)')
    
    # Monitor command
    subparsers.add_parser('monitor', help='Monitor ongoing scans')
    
    # Pause command
    pause_parser = subparsers.add_parser('pause', help='Pause a running scan')
    pause_parser.add_argument('identifier', 
                            help='Run identifier (can be index number, scan name, or full run ID)')
    
    # Resume command
    resume_parser = subparsers.add_parser('resume', help='Resume a paused scan')
    resume_parser.add_argument('identifier', 
                             help='Run identifier (can be index number, scan name, or full run ID)')
    # delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a run and its associated files')
    delete_parser.add_argument('identifier', 
                             help='Run identifier (can be index number, scan name, or full run ID)')
    delete_parser.add_argument('--force', '-f', action='store_true',
                             help='Force deletion without confirmation')
    
    args = parser.parse_args()
    cli = VirtueRedCLI(args.server)

    if args.command == 'config':
        if args.server_url:
            cli.configure(args.server_url)
        else:
            cli.print_config()
    
    elif args.command == 'show-config':
        cli.print_config()
    
    elif args.command == 'status':
        cli.check_server()
        
    elif args.command == 'scan':
        if cli.check_server():  # Check server before starting scan
            datasets = json.loads(args.datasets)
            extra_args = json.loads(args.extra_args) if args.extra_args else None
            if cli.init_scan(args.name, args.model, datasets, extra_args):
                if args.monitor:
                    cli.monitor_progress()
    
    elif args.command == 'list':
        if cli.check_server():
            cli.get_runs()
    
    elif args.command == 'summary':
        if cli.check_server():
            cli.get_run_summary(args.identifier)
    
    elif args.command == 'report':
        if cli.check_server():
            cli.generate_report(args.identifier)
    
    elif args.command == 'monitor':
        if cli.check_server():
            cli.monitor_progress()
        
    elif args.command == 'pause':
        if cli.check_server():
            cli.pause_scan(args.identifier)
        
    elif args.command == 'resume':
        if cli.check_server():
            cli.resume_scan(args.identifier)
        
    elif args.command == 'delete':
        if cli.check_server():
            cli.delete_run(args.identifier)
    else:
        parser.print_help()
        
if __name__ == '__main__':
    main()