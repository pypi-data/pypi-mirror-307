#!/usr/bin/env python3

import click
import os
from datetime import datetime

@click.command()
@click.version_option(package_name="obsidian_note_cli")
@click.option('--title', help='Title of the note')
@click.option('--vault', default=lambda: os.getenv('OBSIDIAN_VAULT', '~/Documents/Obsidian Vault'), help='Obsidian vault name')
@click.option('--path', default=lambda: os.getenv('OBSIDIAN_PATH', ''), help='Path inside the vault')
@click.option('--tags', help='Space-separated tags for the note')
@click.option('--status', default=None, help='Status of the note (optional)')
@click.option('--source', default=None, help='Source of the content, if meaningful')
@click.option('--created_at', default=datetime.now().strftime('%Y-%m-%d'), help='Creation date (defaults to today)')
@click.argument('content', type=click.File('r'), required=False)
def save_note(title, vault, path, tags, status, source, created_at, content):
    """
    Save a note with specified front matter in Obsidian format.
    """

    if not title:
        title = click.prompt('Note title', default='Note title')
        
    if not tags:
        tags = click.prompt('Note tags, comma separated', default=None)

    # Convert tags into list format
    tags_list = [tag.strip() for tag in tags.split(' ')] if tags else []

    # Generate front matter for the note
    front_matter = {
        'tags': tags_list,
        'created_at': created_at,
    }
    if status:
        front_matter['status'] = status
    if source:
        front_matter['source'] = source
           
    # Read content from stdin if available, or use content file provided as an argument
    note_content = content.read() if content else ""
    if not note_content:
        click.echo("Enter note content (type END on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        note_content = "\n".join(lines)
    
    # Format front matter in markdown
    front_matter_md = '---\n'
    for key, value in front_matter.items():
        if isinstance(value, list):
            front_matter_md += f'{key}: {value}\n'
        else:
            front_matter_md += f'{key}: "{value}"\n'
    front_matter_md += '---\n\n'
    
    # Concatenate front matter and content
    full_content = front_matter_md + note_content

    # Define file path
    file_path = os.path.join(os.path.expanduser(vault), path, f"{title}.md")

    # Write the note to the specified file
    with open(file_path, 'w') as f:
        f.write(full_content)
    
    click.echo(f"Note saved to {file_path}")

if __name__ == '__main__':
    save_note()
