import re
import os


def regex_switch(commented, indented):
    baseRegex = r"(?:def\s)(\w+)(?=\s?\((.+)?\):)"

    if commented and indented:
        searchRegex = baseRegex
    elif commented:
        searchRegex = r"^(?:#[ \t]?)?{}".format(baseRegex)
    elif indented:
        searchRegex = r"^(?:[ \t]+)?{}".format(baseRegex)
    else:
        searchRegex = r"^{}".format(baseRegex)

    return searchRegex


def find_functions_in_file(filePath, searchRegex):
    functionList = []

    with open(filePath, "r") as openFileObj:
        for line in openFileObj:
            functionMatch = re.search(searchRegex, line)
            if functionMatch is not None:
                functionList.append(functionMatch.group(1))

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


def create_unittest_filepath(filePath):
    pathComponentsRegex = r"(.+(?:\/|\\))([^\/|\\]+\.py$)"

    targetFileName = re.search(pathComponentsRegex, filePath)
    if targetFileName:
        returnDict = {
            "unittestFilePath": os.path.join(targetFileName.group(1), "tests"),
            "unittestFileName": "test_{0}".format(targetFileName.group(2))
        }
    else:
        return False

    return returnDict


def filter_existing_classes_from_test_file(filePath, classList):
    newClassList = []

    for className in classList:
        with open(filePath) as openFileObj:
            if className not in openFileObj.read():
                newClassList.append(className)
        openFileObj.close()

    return newClassList


def write_new_functions_to_file(filePath, fileName, classList):
    userFileNameImport = re.search(r"test_(.+)\.py", fileName).group(1)
    insertIndex = 0

    with open(filePath, "a+") as unitTestFile:
        unitTestFile.seek(0)
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

    for indexOffSet, string in enumerate(standardStringList):
        if string.strip("\n") not in strippedBodyString:
            bodyStringList.insert((insertIndex + indexOffSet), string)

    insertIndex = bodyStringList.index(standardStringList[2])

    for className in classList:
        bodyStringList.insert(insertIndex, "class {0}(unittest.TestCase):{1}{1}".format(className, "\n"))
        bodyStringList.insert(insertIndex + 1, "{0}def setUp(self):{1}{0}{0}pass{1}{1}".format("    ", "\n"))
        bodyStringList.insert(insertIndex + 2, "{0}def tearDown(self):{1}{0}{0}pass{1}{1}{1}".format("    ", "\n"))
        insertIndex += 3

    with open(filePath, "w") as unitTestFile:
        unitTestFile.writelines(bodyStringList)
        unitTestFile.close()


class CreateTests:

    def __init__(self, targetFilePath, testDirectory, serarchCommented, serarchIndented):
        self.targetFilePath = os.path.abspath(targetFilePath)
        self.searchRegex = regex_switch(serarchCommented, serarchIndented)
        filePathNameDict = create_unittest_filepath(self.targetFilePath)
        self.unittestFileName = filePathNameDict["unittestFileName"]
        self.unittestFilePath = self.file_path_switch(filePathNameDict, testDirectory)
        self.functionLists = find_functions_in_file(self.targetFilePath, self.searchRegex)
        self.classList = convert_function_name_to_unittest_class_name(self.functionLists)

    def file_path_switch(self, filePathNameDict, testDirectory):
        if testDirectory:
            return os.path.join(testDirectory, filePathNameDict["unittestFileName"])
        else:
            return os.path.join(filePathNameDict["unittestFilePath"], filePathNameDict["unittestFileName"])

    def write_tests(self):
        if os.path.isfile(self.unittestFilePath):
            self.classList = filter_existing_classes_from_test_file(self.unittestFilePath, self.classList)
        elif not os.path.exists(os.path.dirname(self.unittestFilePath)):
            os.makedirs(os.path.dirname(self.unittestFilePath))

        write_new_functions_to_file(self.unittestFilePath, self.unittestFileName, self.classList)
        self.userMessage = "Wrote {} new function(s) to {}".format(len(self.classList), self.unittestFilePath)
