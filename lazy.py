from create_tests import CreateTests
import argparse
import os

parser = argparse.ArgumentParser(prog="command")
parser.add_argument("-f", "--file", type=str, required=True, help="File which you want to unittests for")
args = parser.parse_args()


CreateTests(os.path.abspath(args.file)).write_tests()
