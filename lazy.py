from create_tests import CreateTests
import argparse
import sys

parser = argparse.ArgumentParser(prog="command")
parser.add_argument("-f", "--file", type=str, required=True,
                    help="File which you want to unittests for")
parser.add_argument("-d", "--directory", default=False,
                    help="Location to write tests. Default is the target file's directory")
parser.add_argument("-i", "--indented", action="store_true",
                    help="Also looks for indented functions")
parser.add_argument("-c", "--commented", action="store_true",
                    help="Also looks for commented functions")

args = parser.parse_args()

instance = CreateTests(args.file, args.directory, args.commented, args.indented)
instance.write_tests()
sys.stdout.write("{}\n".format(instance.userMessage))
