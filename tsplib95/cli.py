# -*- coding: utf-8 -*-

"""Console script for tsplib95."""
import click
from tabulate import tabulate

from . import loaders
from . import exceptions


def load(filepaths):
    files = {}
    with click.progressbar(filepaths, label='Loading files',
                           show_pos=True) as bar:
        for filepath in bar:
            try:
                file = loaders.load_problem(filepath)
            except exceptions.ParsingError as e:
                error = f'\n{filepath}: {e}'
                click.secho(error, fg='red')
            else:
                files[filepath] = file

    return files


def print_information(files):
    header = ['Type', 'Size', 'Name']
    rows = sorted(get_tabular_data(files))
    click.echo_via_pager(tabulate(rows, header))


def get_tabular_data(files):
    for filepath, file in files.items():
        yield file.type, file.dimension or -1, filepath


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filepaths', nargs=-1,
                type=click.Path(dir_okay=False, readable=True))
def summarize(filepaths):
    """Console script for tsplib95."""
    if filepaths:
        files = load(filepaths)
        print_information(files)


if __name__ == '__main__':
    cli()
