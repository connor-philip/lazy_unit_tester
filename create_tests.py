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


def write_new_functions_to_file(filePath, classList, existingFile):
    userFileNameImport = re.search(r"tests[\\|\/]test_(.+)\.py", filePath).group(1)
    insertIndex = 0

    with open(filePath, "a+") as unitTestFile:
        bodyString = unitTestFile.readlines()

        if not existingFile:
            bodyString.insert(insertIndex, "import unittest{0}".format("\n"))
            bodyString.insert(insertIndex + 1, "import {0}{1}{1}{1}".format(userFileNameImport, "\n"))

        if existingFile:
            for line in bodyString:
                if "if __name__ == \"__main__\":" in line:
                    insertIndex = bodyString.index(line)
        else:
            insertIndex = 2

        for className in classList:
            bodyString.insert(insertIndex, "class {0}(unittest.TestCase):{1}{1}".format(className, "\n"))
            bodyString.insert(insertIndex + 1, "{0}def setUp(self):{1}{0}{0}pass{1}{1}".format("    ", "\n"))
            bodyString.insert(insertIndex + 2, "{0}def tearDown(self):{1}{0}{0}pass{1}{1}{1}".format("    ", "\n"))
            insertIndex += 3

        if not existingFile:
            bodyString.insert(insertIndex + 1, "if __name__ == \"__main__\":{0}".format("\n"))
            bodyString.insert(insertIndex + 2, "{0}unittest.main(){1}".format("    ", "\n"))

        unitTestFile.close()

    with open(filePath, "w") as unitTestFile:
        unitTestFile.writelines(bodyString)
        unitTestFile.close()
