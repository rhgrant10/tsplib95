# -*- coding: utf-8 -*-

"""Console script for tsplib95."""
import click

from . import parser


def get_problems(filepaths):
    m = max(len(path) for path in filepaths)

    problems = {}
    for filepath in filepaths:
        s = m - len(filepath)
        click.echo(f'\rLoading {filepath}{"…":<{s}}', nl=False)
        problem = parser.parse(filepath)
        problems[filepath] = problem

    # looks gnarly but really it's just erasing the last output line
    click.echo(f'\r{" ":<{m + 9}}')

    return problems


def print_information(problems):
    print('Type    Size    Name')
    for type_, size, name in sorted(get_tabular_data(problems)):
        print(f'{type_:<4} {size:>7}\t{name}')


def get_tabular_data(problems):
    for filepath, problem in problems.items():
        yield problem['TYPE'], problem['DIMENSION'], filepath


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filepaths', nargs=-1,
                type=click.Path(dir_okay=False, readable=True))
def summarize(filepaths):
    """Console script for tsplib95."""
    if filepaths:
        problems = get_problems(filepaths)
        print_information(problems)


if __name__ == '__main__':
    cli()
