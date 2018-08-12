# -*- coding: utf-8 -*-

"""Console script for tsplib95."""
import click

from . import utils


def load(filepaths):
    m = max(len(path) for path in filepaths)

    files = {}
    for filepath in filepaths:
        s = m - len(filepath)
        click.echo(f'\rLoading {filepath}{"…":<{s}}', nl=False)
        file = utils.load_unknown(filepath)
        files[filepath] = file

    # looks gnarly but really it's just erasing the last output line
    click.echo(f'\r{" ":<{m + 9}}')

    return files


def print_information(files):
    print('Type    Size    Name')
    for type_, size, name in sorted(get_tabular_data(files)):
        print(f'{type_:<4} {size:>7}\t{name}')


def get_tabular_data(files):
    for filepath, file in files.items():
        yield file.type, file.dimension, filepath


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
