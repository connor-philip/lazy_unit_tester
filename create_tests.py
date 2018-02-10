import re
import os


def find_functions_in_file(filePath):
    functionList = []

    with open(filePath, "r") as openFileObj:
        for line in openFileObj:
            functionMatch = re.search(r"(?<=^def\s)\w+(?=\s?\((.+)?\):)", line)
            if functionMatch is not None:
                functionList.append(functionMatch.group(0))

        openFileObj.close()

    return functionList


def convert_function_name_to_unittest_class_name(functionList):
    classList = []

    def findMatchGroup(matchobj):
        return matchobj.group(2).upper()

    for function in functionList:
        className = re.sub(r"(^|_)(\w)", findMatchGroup, function)
        className = "Test{}".format(className)
        classList.append(className)

    return classList


def construct_unittest_filepath_from_users_filepath(filePath):
    def findMatchGroup(matchobj):
        return "{0}tests{0}test_{1}".format(matchobj.group(1), matchobj.group(2))

    unittestFilepath = re.sub(r"(\/|\\)([^\/|\\]+\.py$)", findMatchGroup, filePath)

    if filePath == unittestFilepath:
        return False

    return unittestFilepath


def filter_existing_classes_from_test_file(filePath, classList):
    newClassList = []

    for className in classList:
        with open(filePath) as openFileObj:
            if className not in openFileObj.read():
                newClassList.append(className)
        openFileObj.close()

    return newClassList


def write_new_functions_to_file(filePath, classList):
    with open(filePath, "a") as unitTestFile:
        for className in classList:
            classNameString = "class {}(unittest.TestCase):\n\n".format(className)
            setUpString = "    def setUp(self):\n        pass\n\n"
            tearDownString = "    def tearDown(self):\n        pass\n\n"
            unitTestFile.write(classNameString)
            unitTestFile.write(setUpString)
            unitTestFile.write(tearDownString)
