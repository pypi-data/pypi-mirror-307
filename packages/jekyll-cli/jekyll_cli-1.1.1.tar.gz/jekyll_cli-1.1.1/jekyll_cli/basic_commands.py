# -*- coding: UTF-8 -*-
import os
import subprocess
from typing import Annotated

import typer
from typer import Typer, Option, Argument, Context

from .blog import Blog
from .config import Config
from .config_commands import app as config_app
from .enums import BlogType
from .item import Item
from .prompt import *
from .utils import complete_items, decode_stdout

app = Typer(
    no_args_is_help=True,
    help='Jekyll Blog CLI Tool.',
    rich_markup_mode='rich'
)

app.add_typer(config_app, rich_help_panel='Configuration')


@app.callback()
def check(context: Context):
    if context.invoked_subcommand != 'init' and context.invoked_subcommand != 'config':
        if Config.root is None:
            print('[red]No blog root. Use "blog init" to initialize the blog.')
            raise typer.Exit(code=1)


@app.command(rich_help_panel='Generation')
def serve(
    draft: Annotated[bool, Option(help='Start blog server with drafts.')] = Config.select('generate.draft'),
    port: Annotated[int, Option(help='Listen on the given port.')] = Config.select('generate.port')
):
    """Start blog server locally through jekyll."""
    os.chdir(Config.root)
    command = ['bundle', 'exec', 'jekyll', 'serve']
    # draft option
    if draft:
        command.append('--drafts')
    if port is not None:
        command.append(f'--port {port}')
    subprocess.run(command, shell=True)


@app.command(rich_help_panel='Generation')
def build(draft: Annotated[bool, Option(help='Build including drafts.')] = Config.select('generate.draft')):
    """Build jekyll site."""
    os.chdir(Config.root)
    command = ['bundle', 'exec', 'jekyll', 'build']
    if draft:
        command.append('--drafts')
    subprocess.run(command, shell=True)


@app.command(rich_help_panel='Operation')
def info(name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))]):
    """Show info about post or draft."""
    items = Blog.find(name)
    if len(items) == 0:
        print('[red]No such item.')
        return

    item = items[0] if len(items) == 1 else select(
        message=f'Found {len(items)} matches, select one to check:',
        choices={f'[{item.type.name}] {item.name}': item for item in items}
    )
    print_info(item.info(), title='[bold green]Info', show_header=False)


@app.command(name='list', rich_help_panel='Operation')
def list_items(
    name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))] = None,
    draft: Annotated[bool, Option('--draft', '-d', help='List only all drafts.')] = False,
    post: Annotated[bool, Option('--post', '-p', help='List only all posts.')] = False,
):
    """List all posts and drafts or find items by name."""
    match (draft, post):
        case (True, False):
            drafts = Blog.find(name, BlogType.Draft) if name is not None else Blog.drafts
            posts = None
        case (False, True):
            drafts = None
            posts = Blog.find(name, BlogType.Post) if name is not None else Blog.posts
        case _:
            if name is not None:
                items = Blog.find(name)
                drafts = [item for item in items if item.type == BlogType.Draft]
                posts = [item for item in items if item.type == BlogType.Post]
            else:
                drafts, posts = (Blog.drafts, Blog.posts)
    if posts:
        print_table(posts, title='[bold green]Posts', show_header=False)
    if drafts:
        print_table(drafts, title='[bold green]Drafts', show_header=False)
    if not posts and not drafts:
        print('[red]Nothing to show.')


@app.command(name='open', rich_help_panel='Operation')
def open_item(
    name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))],
    editor: Annotated[str, Option('--editor', '-e', help='Open item in given editor')] = None,
):
    """Open post or draft in editor."""
    items = Blog.find(name)
    if len(items) == 0:
        print(f'[red]No such item.')
        return

    item = items[0] if len(items) == 1 else select(
        message=f'Found {len(items)} matches, select one to open:',
        choices={f'[{item.type.name}] {item.name}': item for item in items}
    )
    if not editor:
        editor = Config.select('default.editor')
    print(f'Opening "{item.file_path}"...')
    item.open(editor=editor)


@app.command(rich_help_panel='Operation')
def draft(
    name: Annotated[str, Argument(help='Name of draft item.')],
    title: Annotated[str, Option('--title', '-t', help='Title of draft.')] = None,
    class_: Annotated[List[str], Option('--class', '-c', help='Categories of draft.')] = None,
    tag: Annotated[List[str], Option('--tag', '-g', help='Tags of draft.')] = None,
    editor: Annotated[str, Option('--editor', '-e', help='Open draft in given editor.')] = None
):
    """Create a draft."""
    item = Item(name, BlogType.Draft)
    if item in Blog:
        print(f'[red]Draft "{item.name}" already exists.')
        return
    item.create(title, class_, tag)
    print(f'"{item.file_path}" created successfully.')
    if editor:
        print('Opening draft...')
        item.open(editor=editor)


@app.command(rich_help_panel='Operation')
def post(
    name: Annotated[str, Argument(help='Name of post item.')],
    title: Annotated[str, Option('--title', '-t', help='Title of post.')] = None,
    class_: Annotated[List[str], Option('--class', '-c', help='Categories of post.')] = None,
    tag: Annotated[List[str], Option('--tag', '-g', help='Tags of post.')] = None,
    editor: Annotated[str, Option('--editor', '-e', help='Open post in given editor.')] = None
):
    """Create a post."""
    item = Item(name, BlogType.Post)
    if item in Blog:
        print(f'[red]Post "{item.name}" already exists.')
        return
    item.create(title, class_, tag)
    print(f'"{item.file_path}" created successfully.')
    if editor:
        print('Opening post...')
        item.open(editor=editor)


@app.command(rich_help_panel='Operation')
def remove(name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))]):
    """Remove a post or draft."""
    items = Blog.find(name)
    if len(items) == 0:
        print(f'[red]No such item.')
        return

    selected_items = items if len(items) == 1 else check(
        message=f'Found {len(items)} matches, select items to remove (Ctrl+A to select all, Ctrl+R to toggle selection):',
        choices={f'[{item.type.name}] {item.name}': item for item in items}
    )
    for i, item in enumerate(selected_items):
        print(f'{i + 1}. {item}')
    if confirm(f'Found {len(items)} matches, remove above items?'):
        for item in items:
            item.remove()
        print('[green]Remove successfully.')


@app.command(rich_help_panel='Operation')
def publish(name: Annotated[str, Argument(help='Name of draft.', autocompletion=complete_items(Blog.drafts))]):
    """Publish a draft."""
    items = Blog.find(name, BlogType.Draft)

    if len(items) == 0:
        print_table(Blog.drafts, title='[bold green]Drafts', show_header=False)
        print('[red]No such item in _drafts.')
        return

    if len(items) != 1:
        items = check(
            message=f'Found {len(items)} matches, select items to publish (Ctrl+A to select all, Ctrl+R to toggle selection):',
            choices={f'[{item.type.name}] {item.name}': item for item in items}
        )
    for item in items:
        item.publish()
        print(f'Draft "{item.name}" published as "{item.file_path}"')


@app.command(rich_help_panel='Operation')
def unpublish(name: Annotated[str, Argument(help='Name of post.', autocompletion=complete_items(Blog.posts))]):
    """Unpublish a post."""
    items = Blog.find(name, BlogType.Post)

    if len(items) == 0:
        print_table(Blog.posts, title='[bold green]Posts', show_header=False)
        print('[red]No such item in _posts.')
        return

    if len(items) != 1:
        items = check(
            message=f'Found {len(items)} matches, select items to unpublish (Ctrl+A to select all, Ctrl+R to toggle selection):',
            choices={f'[{item.type.name}] {item.name}': item for item in items}
        )
    for item in items:
        item.unpublish()
        print(f'Post "{item.name}" unpublished as "{item.file_path}"')


@app.command(rich_help_panel='Configuration')
def init():
    """Initialize the application interactively."""
    print('[bold green]Welcome to the Jekyll CLI application!:wave::wave::wave:')
    print("Let's set up your basic configuration.:wink:")
    root = input_directory_path('Please enter the root path of your blog:')
    mode = select(
        message='Please choose the management mode (single or item):',
        choices={
            'single (A single markdown file denotes a blog item.)': 'single',
            'item (A directory containing a markdown file and an assets directory denotes a blog item.)': 'item'
        }
    )
    deploy = confirm('Generate deploy configuration file "jekyll-deploy.yml"?', default=True)

    rule()
    print('You have entered the following configurations:')
    print_info({
        'Blog root path': root,
        'Management mode': mode,
        'Generate deploy configuration': deploy
    }, show_header=False)

    if confirm('Confirm your configurations?', default=True):
        Config.init(root, mode, deploy)
        print('[bold green]Basic configuration set up successfully!')
        print('Generate config files:')
        print_info({
            'Blog configuration': str(Config.config_path),
            'Deploy configuration': str(Config.deploy_path),
        }, show_header=False)
        print('Type "--help" for more information.')
    else:
        print('[red]Aborted.')


@app.command(rich_help_panel='Operation')
def rename(
    name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))],
    new_name: Annotated[str, Argument(help='New name.')]
):
    """Rename a post or draft."""
    items = Blog.find(name)
    if len(items) == 0:
        print('[red]No such item.')
        return

    item = items[0] if len(items) == 1 else select(
        message=f'Found {len(items)} matches, select one to rename:',
        choices={f'[{item.type.name}] {item.name}': item for item in items}
    )

    old_path = item.path
    item.rename(new_name)
    print(f'Renamed "{old_path}" to "{item.path}" successfully.')


@app.command(rich_help_panel='Generation')
def deploy():
    """Deploy the site with the '<root>/jekyll-deploy.yml.'"""
    steps = Config.select('deploy.steps')
    if steps is None:
        print('[red]No deploy configuration found.')
        return

    os.chdir(Config.root)
    for step in steps:
        command = step.get('command')
        if not command:
            continue
        name = step.get('name', command)
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode == 0:
            print(f'[green]Run "{name}" successfully.')
            if result.stdout:
                print(decode_stdout(result.stdout))
        else:
            print(f'[red]Run "{name}" failed, the details are shown below:')
            print(f'[red]{decode_stdout(result.stdout)}')
            print(f'[red]{decode_stdout(result.stderr)}')
            break
