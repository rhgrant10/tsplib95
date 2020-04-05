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


def get_tabular_data(files):
    header = ['Type', 'Size', 'Name']
    rows = []
    for filepath, file in files.items():
        row = file.type, file.dimension or -1, filepath
        rows.append(row)
    return header, rows


def print_information(files):
    header, rows = get_tabular_data(files)
    click.echo_via_pager(tabulate(sorted(rows), header))


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
