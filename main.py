import copy
import os, glob
import click
from generator.synthetic_data import SyntheticData


@click.group()
def custom_group():
    pass

@custom_group.command()
@click.option("-l", "--label", help="name of output directory (default '03-size-10k')", default="03-size-10k")
@click.option("-c", "--count", help="amount of generated items (default 10000)", default=10000)
@click.option("-b", "--bulk", help="amount of bulk for processing (default 1000)", default=1000)
@click.option("-cmp", "--compress", help="is compress (default True)", default=True)
def generate(label, count, bulk, compress):
    """Generate own dataset with requested data size (and processing in bulks).
    Command line example: 'python main.py generate -l 03-size-10k -c 10000 -b 1000' or 'python main.py generate --help' """

    generator = SyntheticData()
    generator.generate(label, count, bulk, compress)

@click.group()
def std_group():
    pass

@std_group.command()
def standard():
    """Generate standard datasets (it means these datasets '01-size-100' and '02-size-1k' will be generated).
    Command line example: 'python main.py standard' """
    generator = SyntheticData()
    generator.generate(label="01-size-100", count=100, bulk_max=100, compress=True)
    generator.generate(label="02-size-1K", count=1000, bulk_max=1000, compress=True)

cli = click.CommandCollection(sources=[std_group, custom_group])

if __name__ == '__main__':

    # Sample of command lines:
        # python main.py standard
        # python main.py generate -l 03-size-10k -c 10000 -b 1000
    
    cli()



