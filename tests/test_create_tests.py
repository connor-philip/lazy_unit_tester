import unittest
import create_tests
import os

CURRENTDIRPATH = os.path.dirname(os.path.realpath(__file__))


def yield_input_expected_output_match(function, inputList, expectedOutputList):
    for index, item in enumerate(inputList):
        returnedValue = function(item)
        if returnedValue == expectedOutputList[index]:
            yield (True, "")
        else:
            yield (False, "return of {}({}) did not match {}. Got instead:{}".format(function.__name__,
                                                                                     item,
                                                                                     expectedOutputList[index],
                                                                                     returnedValue))


class TestRegexSwitch(unittest.TestCase):

    def setUp(self):
        self.standardReturn = create_tests.regex_switch(False, False)
        self.indentedReturn = create_tests.regex_switch(False, True)
        self.commentedReturn = create_tests.regex_switch(True, False)
        self.catchAllReturn = create_tests.regex_switch(True, True)

    def test_string_is_returned(self):

        self.assertIsInstance(self.standardReturn, str)
        self.assertIsInstance(self.indentedReturn, str)
        self.assertIsInstance(self.commentedReturn, str)
        self.assertIsInstance(self.catchAllReturn, str)

    def testcorrect_regex_is_returned(self):
        standardRegex = r"^(?:def\s)(\w+)(?=\s?\((.+)?\):)"
        includeindentedRegex = r"^(?:[ \t]+)?(?:def\s)(\w+)(?=\s?\((.+)?\):)"
        includeCommentedRegex = r"^(?:#[ \t]?)?(?:def\s)(\w+)(?=\s?\((.+)?\):)"
        catchAllRegex = r"(?:def\s)(\w+)(?=\s?\((.+)?\):)"

        self.assertEqual(standardRegex, self.standardReturn)
        self.assertEqual(includeindentedRegex, self.indentedReturn)
        self.assertEqual(includeCommentedRegex, self.commentedReturn)
        self.assertEqual(catchAllRegex, self.catchAllReturn)


# Differet types of invalid function names are listed in functions_test_data.txt
class TestFindFunctionsInFile(unittest.TestCase):

    def setUp(self):
        self.functions_test_data_file = os.path.join(CURRENTDIRPATH, "test_create_tests_data", "functions_test_data.txt")
        self.standardRegex = create_tests.regex_switch(commented=False, indented=False)
        self.includeCommentedRegex = create_tests.regex_switch(commented=True, indented=False)
        self.includeindentedRegex = create_tests.regex_switch(commented=False, indented=True)
        self.catchAllRegex = create_tests.regex_switch(commented=True, indented=True)

    def test_list_of_functions_returned(self):
        returnedValue = create_tests.find_functions_in_file(self.functions_test_data_file, self.standardRegex)
        self.assertIsInstance(returnedValue, list)

    def test_standard_regex_matches_only_valid_functions(self):
        returnedValue = create_tests.find_functions_in_file(self.functions_test_data_file, self.standardRegex)
        expectedReturn = [
            "function_for_test_case1",
            "function_for_test_case2",
            "function_for_test_case3",
            "function_for_test_case4",
            "functionfortestcase",
            "functionfortestcase2",
            "FunctionForTestCase",
            "FunctionForTestCase2",
            "functionForTestCase",
            "functionForTestCase2",
            "spacebeforebrackets"]

        self.assertEqual(returnedValue, expectedReturn)

    def test_include_commented_regex_matches_only_valid_functions(self):
        returnedValue = create_tests.find_functions_in_file(self.functions_test_data_file, self.includeCommentedRegex)
        expectedReturn = [
            "function_for_test_case1",
            "function_for_test_case2",
            "function_for_test_case3",
            "function_for_test_case4",
            "functionfortestcase",
            "functionfortestcase2",
            "FunctionForTestCase",
            "FunctionForTestCase2",
            "functionForTestCase",
            "functionForTestCase2",
            "spacebeforebrackets",
            "commented_function1",
            "commented_function2"]

        self.assertEqual(returnedValue, expectedReturn)

    def test_include_indented_regex_matches_only_valid_functions(self):
        returnedValue = create_tests.find_functions_in_file(self.functions_test_data_file, self.includeindentedRegex)
        expectedReturn = [
            "function_for_test_case1",
            "function_for_test_case2",
            "function_for_test_case3",
            "function_for_test_case4",
            "functionfortestcase",
            "functionfortestcase2",
            "FunctionForTestCase",
            "FunctionForTestCase2",
            "functionForTestCase",
            "functionForTestCase2",
            "spacebeforebrackets",
            "space_indented_function",
            "tab_indented_function"]

        self.assertEqual(returnedValue, expectedReturn)

    def test_catch_all_regex_matches_only_valid_functions(self):
        returnedValue = create_tests.find_functions_in_file(self.functions_test_data_file, self.catchAllRegex)
        expectedReturn = [
            "function_for_test_case1",
            "function_for_test_case2",
            "function_for_test_case3",
            "function_for_test_case4",
            "functionfortestcase",
            "functionfortestcase2",
            "FunctionForTestCase",
            "FunctionForTestCase2",
            "functionForTestCase",
            "functionForTestCase2",
            "spacebeforebrackets",
            "space_indented_function",
            "tab_indented_function",
            "commented_function1",
            "commented_function2",
            "commented_space_indented_function",
            "commented_space_indented_function2",
            "commented_tab_indented_function"]

        self.assertEqual(returnedValue, expectedReturn)


class TestConvertFunctionNameToUnittestClassName(unittest.TestCase):

    def setUp(self):
        self.functionList = [
            "function_for_test_case1",
            "function_for_test_case2",
            "function_for_test_case3",
            "function_for_test_case4",
            "functionfortestcase",
            "functionfortestcase2",
            "FunctionForTestCase",
            "FunctionForTestCase2",
            "functionForTestCase",
            "functionForTestCase2",
            "spacebeforebrackets"]

        self.expectedReturn = [
            'TestFunctionForTestCase1',
            'TestFunctionForTestCase2',
            'TestFunctionForTestCase3',
            'TestFunctionForTestCase4',
            'TestFunctionfortestcase',
            'TestFunctionfortestcase2',
            'TestFunctionForTestCase',
            'TestFunctionForTestCase2',
            'TestFunctionForTestCase',
            'TestFunctionForTestCase2',
            'TestSpacebeforebrackets']

    def test_function_names_formatted_to_class_name_correctly(self):
        returnedValue = create_tests.convert_function_name_to_unittest_class_name(self.functionList)

        self.assertEqual(returnedValue, self.expectedReturn)


class TestCreateUnittestFilepath(unittest.TestCase):

    def test_function_returns_unittest_filepath_from_valid_input(self):
        inputList = [
            "/c/pythonfile.py",
            "/c/python_file.py",
            "/c/PythonFile.py",
            "/c/pythonfile.py",
            "/c/python file.py",
            "/d/python_file.py",
            "/z/pythonflie.py",
            "/d/directory/python_file.py"]
        expectedOutputList = [
            {'unittestFileName': 'test_pythonfile.py', 'unittestFilePath': '/c/tests'},
            {'unittestFileName': 'test_python_file.py', 'unittestFilePath': '/c/tests'},
            {'unittestFileName': 'test_PythonFile.py', 'unittestFilePath': '/c/tests'},
            {'unittestFileName': 'test_pythonfile.py', 'unittestFilePath': '/c/tests'},
            {'unittestFileName': 'test_python file.py', 'unittestFilePath': '/c/tests'},
            {'unittestFileName': 'test_python_file.py', 'unittestFilePath': '/d/tests'},
            {'unittestFileName': 'test_pythonflie.py', 'unittestFilePath': '/z/tests'},
            {'unittestFileName': 'test_python_file.py', 'unittestFilePath': '/d/directory/tests'}
        ]

        for returnedValue in yield_input_expected_output_match(create_tests.create_unittest_filepath,
                                                               inputList,
                                                               expectedOutputList):
            self.assertTrue(returnedValue[0], msg=returnedValue[1])

    def test_function_returns_false_from_invalid_input(self):
        returnedValue = create_tests.create_unittest_filepath("pythonfile")

        self.assertFalse(returnedValue)

    def test_function_only_accepts_py_files(self):
        returnedValue = create_tests.create_unittest_filepath("/c/pythonfile.pie")

        self.assertFalse(returnedValue)

    def test_function_needs_full_file_path(self):
        returnedValue = create_tests.create_unittest_filepath("pythonfile.py")

        self.assertFalse(returnedValue)


class TestWriteNewFunctionsToFile(unittest.TestCase):

    def setUp(self):
        self.fileName = "test_functions_test_data.py"
        self.unitTestFilePath = os.path.join(CURRENTDIRPATH, "test_functions_test_data.py")
        self.unitTestFileFreshBaseline = os.path.join(CURRENTDIRPATH, "test_create_tests_data", "test_functions_test_data_fresh_baseline.txt")
        self.unitTestFileExistingBaseline = os.path.join(CURRENTDIRPATH, "test_create_tests_data", "test_functions_test_data_existing_baseline.txt")
        self.standardRegex = create_tests.regex_switch(commented=False, indented=False)
        functionList = create_tests.find_functions_in_file(os.path.join(CURRENTDIRPATH, "test_create_tests_data", "functions_test_data.txt"),
                                                           self.standardRegex)
        self.classList = create_tests.convert_function_name_to_unittest_class_name(functionList)

    def tearDown(self):
        os.remove(self.unitTestFilePath)

    def test_file_is_created(self):
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.fileName, self.classList)
        doesfileExist = os.path.isfile(self.unitTestFilePath)

        self.assertTrue(doesfileExist)

    def test_file_matches_baseline_for_fresh_file(self):
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.fileName, self.classList)

        with open(self.unitTestFilePath, "r") as createdFile:
            createdFileContents = createdFile.read()
            createdFile.close()

        with open(self.unitTestFileFreshBaseline, "r") as baseLine:
            baseLineFileContents = baseLine.read()
            baseLine.close()

        self.assertEqual(createdFileContents,
                         baseLineFileContents,
                         msg="created file did not match baseline, created file;\n{}".format(createdFileContents))

    def test_file_matches_baseline_for_existing_file(self):
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.fileName, self.classList)
        self.classList.append("ThisIsNew")
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.fileName, self.classList)

        with open(self.unitTestFilePath, "r") as createdFile:
            createdFileContents = createdFile.read()
            createdFile.close()

        with open(self.unitTestFileExistingBaseline, "r") as baseLine:
            baseLineFileContents = baseLine.read()
            baseLine.close()

        self.assertEqual(createdFileContents,
                         baseLineFileContents,
                         msg="created file did not match baseline, created file;\n{}".format(createdFileContents))


class TestFilterExistingClassesFromTestFile(unittest.TestCase):

    def setUp(self):
        self.fileName = "test_functions_test_data.py"
        self.unitTestFilePath = os.path.join(CURRENTDIRPATH, "test_functions_test_data.py")
        self.standardRegex = create_tests.regex_switch(commented=False, indented=False)
        functionList = create_tests.find_functions_in_file(os.path.join(CURRENTDIRPATH, "test_create_tests_data", "functions_test_data.txt"),
                                                           self.standardRegex)
        self.classList = create_tests.convert_function_name_to_unittest_class_name(functionList)
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.fileName, self.classList)

    def tearDown(self):
        os.remove(self.unitTestFilePath)

    def test_list_of_functions_returned(self):
        returnedValue = create_tests.filter_existing_classes_from_test_file(self.unitTestFilePath,
                                                                            self.classList)

        self.assertIsInstance(returnedValue, list)

    def test_existing_functions_are_excluded(self):
        returnedValue = create_tests.filter_existing_classes_from_test_file(self.unitTestFilePath,
                                                                            self.classList)

        self.assertEqual(returnedValue, [])

    def test_new_functions_are_included(self):
        self.classList.append("ThisIsNew")
        returnedValue = create_tests.filter_existing_classes_from_test_file(self.unitTestFilePath,
                                                                            self.classList)

        self.assertEqual(returnedValue, ["ThisIsNew"])


if __name__ == "__main__":
    unittest.main()
