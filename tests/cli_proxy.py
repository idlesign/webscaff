# Helper to debug CLI runs through.
from sys import argv

from webscaff.cli import program

program.run(argv=argv)
