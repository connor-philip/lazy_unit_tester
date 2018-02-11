import unittest
import create_tests
import os

CURRENTDIRPATH = os.path.dirname(os.path.realpath(__file__))


def yield_input_expected_output_match(function, inputList, expectedOutputList):
    for index, item in enumerate(inputList):
        if function(item) == expectedOutputList[index]:
            yield (True, "")
        else:
            yield (False, "return of {}({}) did not match {}".format(function.__name__, item, expectedOutputList[index]))


class TestFindFunctionsInFile(unittest.TestCase):  # Differet types of invalid function names are listed in functions_test_data.txt

    def setUp(self):
        self.functions_test_data_file = "{}/functions_test_data.txt".format(CURRENTDIRPATH)
        self.returnedValue = create_tests.find_functions_in_file(self.functions_test_data_file)

    def test_list_of_functions_returned(self):
        self.assertIsInstance(self.returnedValue, list)

    def test_regex_matches_only_valid_functions(self):
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

        self.assertEqual(self.returnedValue, expectedReturn)


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


class TestConstructUnittestFilepathFromUsersFilepath(unittest.TestCase):

    def test_function_adds_correct_slashes_for_filepath(self):
        inputList = [
            "C:\pythonfile.py",
            "/z/pythonflie.py"]
        expectedOutputList = [
            "C:\\tests\\test_pythonfile.py",
            "/z/tests/test_pythonflie.py"]

        for returnedValue in yield_input_expected_output_match(create_tests.construct_unittest_filepath_from_users_filepath, inputList, expectedOutputList):
            self.assertTrue(returnedValue[0], msg=returnedValue[1])

    def test_function_returns_unittest_filepath_from_valid_input(self):
        inputList = [
            "C:\pythonfile.py",
            "C:\python_file.py",
            "C:\PythonFile.py",
            "C:\pythonfile.py",
            "C:\python file.py",
            "D:\python_file.py",
            "/z/pythonflie.py"]
        expectedOutputList = [
            "C:\\tests\\test_pythonfile.py",
            "C:\\tests\\test_python_file.py",
            "C:\\tests\\test_PythonFile.py",
            "C:\\tests\\test_pythonfile.py",
            "C:\\tests\\test_python file.py",
            "D:\\tests\\test_python_file.py",
            "/z/tests/test_pythonflie.py"]

        for returnedValue in yield_input_expected_output_match(create_tests.construct_unittest_filepath_from_users_filepath, inputList, expectedOutputList):
            self.assertTrue(returnedValue[0], msg=returnedValue[1])

    def test_function_returns_false_from_invalid_input(self):
        returnedValue = create_tests.construct_unittest_filepath_from_users_filepath("pythonfile")

        self.assertFalse(returnedValue)

    def test_function_only_accepts_py_files(self):
        returnedValue = create_tests.construct_unittest_filepath_from_users_filepath("C:\pythonfile.pie")

        self.assertFalse(returnedValue)

    def test_function_needs_full_file_path(self):
        returnedValue = create_tests.construct_unittest_filepath_from_users_filepath("pythonfile.py")

        self.assertFalse(returnedValue)


class TestWriteNewFunctionsToFile(unittest.TestCase):

    def setUp(self):
        self.unitTestFilePath = "/home/vagrant/CPTS/tests/test_functions_test_data.py"
        self.unitTestFileFreshBaseline = "/home/vagrant/CPTS/tests/test_functions_test_data_fresh_baseline.txt"
        self.unitTestFileExistingBaseline = "/home/vagrant/CPTS/tests/test_functions_test_data_existing_baseline.txt"
        functionList = create_tests.find_functions_in_file("/home/vagrant/CPTS/tests/functions_test_data.txt")
        self.classList = create_tests.convert_function_name_to_unittest_class_name(functionList)

    def tearDown(self):
        os.remove(self.unitTestFilePath)

    def test_file_is_created(self):
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.classList)
        doesfileExist = os.path.isfile(self.unitTestFilePath)

        self.assertTrue(doesfileExist)

    def test_file_matches_baseline_for_fresh_file(self):
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.classList)

        with open(self.unitTestFilePath, "r") as createdFile:
            createdFileContents = createdFile.read()
            createdFile.close()

        with open(self.unitTestFileFreshBaseline, "r") as baseLine:
            baseLineFileContents = baseLine.read()
            baseLine.close()

        self.assertEqual(createdFileContents, baseLineFileContents, msg="created file did not match baseline, created file;\n{}".format(createdFileContents))

    def test_file_matches_baseline_for_existing_file(self):
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.classList)
        self.classList.append("ThisIsNew")
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.classList)

        with open(self.unitTestFilePath, "r") as createdFile:
            createdFileContents = createdFile.read()
            createdFile.close()

        with open(self.unitTestFileExistingBaseline, "r") as baseLine:
            baseLineFileContents = baseLine.read()
            baseLine.close()

        self.assertEqual(createdFileContents, baseLineFileContents, msg="created file did not match baseline, created file;\n{}".format(createdFileContents))


class TestFilterExistingClassesFromTestFile(unittest.TestCase):

    def setUp(self):
        self.unitTestFilePath = "/home/vagrant/CPTS/tests/test_functions_test_data.py"
        functionList = create_tests.find_functions_in_file("/home/vagrant/CPTS/tests/functions_test_data.txt")
        self.classList = create_tests.convert_function_name_to_unittest_class_name(functionList)
        create_tests.write_new_functions_to_file(self.unitTestFilePath, self.classList)

    def tearDown(self):
        os.remove(self.unitTestFilePath)

    def test_list_of_functions_returned(self):
        returnedValue = create_tests.filter_existing_classes_from_test_file(self.unitTestFilePath, self.classList)

        self.assertIsInstance(returnedValue, list)

    def test_existing_functions_are_excluded(self):
        returnedValue = create_tests.filter_existing_classes_from_test_file(self.unitTestFilePath, self.classList)

        self.assertEquals(returnedValue, [])

    def test_new_functions_are_included(self):
        self.classList.append("ThisIsNew")
        returnedValue = create_tests.filter_existing_classes_from_test_file(self.unitTestFilePath, self.classList)

        self.assertEquals(returnedValue, ["ThisIsNew"])


if __name__ == "__main__":
    unittest.main()
