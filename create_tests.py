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
        className = "Test%s" % (className)
        classList.append(className)

    return classList


def construct_unittest_filepath_from_users_filepath(filePath):
    def findMatchGroup(matchobj):
        return "%stests%stest_%s" % (matchobj.group(1), matchobj.group(1), matchobj.group(2))

    unittestFilepath = re.sub(r"(\/|\\)([^\/|\\]+\.py$)", findMatchGroup, filePath)

    if filePath == unittestFilepath:
        return False

    return unittestFilepath


def compare_functions_in_existing_test_file(filePath):
    pass


def write_new_functions_to_file():
    pass
