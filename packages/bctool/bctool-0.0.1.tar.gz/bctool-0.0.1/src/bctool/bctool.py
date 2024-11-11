from os import write
import sys
import click
import functools

from beancount import loader
from beancount.parser import printer
from beancount.core import data

load_file = functools.partial(loader.load_file,log_errors=sys.stderr)


@click.group()
def beantool():
    pass

@beantool.command()
@click.argument("beanfiles", nargs=-1, type=click.Path(exists=True,file_okay=True,dir_okay=True,readable=True,allow_dash=True))
@click.option("--with-custom", is_flag=True, help="custom entry")
def merge(beanfiles, with_custom):

    entries = []
    for beanfile in beanfiles:
        result, _, _ = load_file(beanfile)
        entries+=result

    for entry in entries:
        if with_custom is False and isinstance(entry, data.Custom):
            continue

        printer.print_entry(entry)


if __name__=="__main__":
    beantool()
