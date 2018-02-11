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
    userFileNameImport = re.search(r"tests[\\|\/]test_(.+)\.py", filePath).group(1)
    insertIndex = 0

    with open(filePath, "a+") as unitTestFile:
        bodyStringList = unitTestFile.readlines()
        unitTestFile.close()

    strippedBodyString = []
    standardStringList = [
        "import unittest{0}".format("\n"),
        "import {0}{1}{1}{1}".format(userFileNameImport, "\n"),
        "if __name__ == \"__main__\":{0}".format("\n"),
        "{0}unittest.main(){1}".format("    ", "\n")]

    for line in bodyStringList:
        strippedBodyString.append(line.strip("\n"))

    for string in standardStringList:
        if string.strip("\n") not in strippedBodyString:
            bodyStringList.insert(insertIndex + standardStringList.index(string), string)

    insertIndex = bodyStringList.index(standardStringList[2])

    for className in classList:
        bodyStringList.insert(insertIndex, "class {0}(unittest.TestCase):{1}{1}".format(className, "\n"))
        bodyStringList.insert(insertIndex + 1, "{0}def setUp(self):{1}{0}{0}pass{1}{1}".format("    ", "\n"))
        bodyStringList.insert(insertIndex + 2, "{0}def tearDown(self):{1}{0}{0}pass{1}{1}{1}".format("    ", "\n"))
        insertIndex += 3

    with open(filePath, "w") as unitTestFile:
        unitTestFile.writelines(bodyStringList)
        unitTestFile.close()
