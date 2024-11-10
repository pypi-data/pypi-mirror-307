#!/usr/bin/env python3

import os
import json
import git
import shutil
from pathlib import Path
from InquirerPy import inquirer
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.spinner import Spinner

console = Console()
repo = git.Repo('.')

def save_git_history():
    try:
        log = repo.git.log('--pretty=format:%H|%ad|%s|%an').splitlines()
        history = [
            {
                'hash': entry.split('|')[0],
                'date': entry.split('|')[1],
                'message': entry.split('|')[2],
                'author': entry.split('|')[3]
            }
            for entry in log
        ]

        history_path = Path.cwd() / 'git_history.json'
        with open(history_path, 'w') as f:
            json.dump(history, f, indent=2)

        print(f"[gray]Git history saved to {history_path}[/gray]")
    except Exception as error:
        print(f"[red]Failed to fetch Git history: {error}[/red]")

def check_gitignore():
    gitignore_path = Path.cwd() / '.gitignore'
    common_ignored_files = [
        'node_modules/', 'dist/', '.env', '*.log', 'coverage/', '.DS_Store', 'git_history.json'
    ]

    if not gitignore_path.exists():
        create_gitignore = inquirer.confirm(
            message="No .gitignore file found. Would you like to create one?", default=True
        ).execute()
        if create_gitignore:
            with open(gitignore_path, 'w') as f:
                f.write('\n'.join(common_ignored_files))
            print("[green]Created .gitignore with selected entries.[/green]")
    else:
        with open(gitignore_path, 'r') as f:
            existing_entries = f.read().splitlines()
        
        new_entries = [item for item in common_ignored_files if item not in existing_entries]
        
        if new_entries:
            selected_files = inquirer.checkbox(
                message="Select files to add to .gitignore:",
                choices=new_entries,
            ).execute()

            with open(gitignore_path, 'a') as f:
                f.write('\n' + '\n'.join(selected_files))
            print("[green]Updated .gitignore.[/green]")

def get_git_status():
    status = repo.git.status('--short').splitlines()
    untracked_files = [line[3:] for line in status if line.startswith('??')]
    modified_files = [line[3:] for line in status if not line.startswith('??')]
    return untracked_files, modified_files

def prompt_for_adding_files(files):
    if not files:
        print("[cyan]Project is up to date.[/cyan]")
        return False

   
    add_method = inquirer.confirm(
        message="Add files automatically (y) or manually (n)?", default=True
    ).execute()

    if add_method:
        repo.git.add(files)
        print(f"[white]Adding files:[/white] {', '.join(files)}")
    else:
        selected_files = inquirer.checkbox(
            message="Select files to add:", choices=files
        ).execute()
        repo.git.add(selected_files)
        print(f"[white]Adding files:[/white] {', '.join(selected_files)}")
    
    return True

def commit_changes():
    commit_messages = [
        'Update files', 'Refactor code', 'Fix bugs', 'Enhance performance', 'Add new feature'
    ]

    commit_message = inquirer.select(
        message="Select a commit message:", choices=commit_messages
    ).execute()

    repo.git.commit('-m', commit_message)
    return commit_message

def push_to_branch(commit_message):
    remotes = repo.remotes
    if not remotes:
        print("[red]No remote repository found.[/red]")
        return

    branch = Prompt.ask("Enter the branch name to push to", default="main")
    
    if branch not in [h.name for h in repo.refs]:
        print(f"[red]Branch '{branch}' does not exist on remote.[/red]")
        return

    with console.status(f"Pushing code to branch '{branch}'..."):
        try:
            repo.git.push('origin', branch)
            latest_commit = repo.git.log('-1', '--pretty=%H').strip()[:7]
            print(
                f"\n{{ [white]Branch[/white]: '[green]{branch}[/green]', [white]SHA[/white]: '[green]{latest_commit}[/green]', [white]Commit[/white]: '[green]{commit_message}[/green]' }}"
            )
        except git.exc.GitCommandError as error:
            console.log(f"[red]Failed to push code to GitHub: {error}[/red]")

def main():
    try:
        check_gitignore()
        untracked_files, modified_files = get_git_status()
        files_to_display = [f for f in modified_files + untracked_files if Path(f).exists()]

        if files_to_display:
            prompt_for_adding_files(files_to_display)

        commit_message = commit_changes()
        push_to_branch(commit_message)
    except Exception as err:
        print(f"[red]An error occurred: {err}[/red]")

if __name__ == "__main__":
    main()
