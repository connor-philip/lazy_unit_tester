import unittest
import create_tests
import os

CURRENTDIRPATH = os.path.dirname(os.path.realpath(__file__))


class TestFindFunctionsInFile(unittest.TestCase):  # Differet types of invalid function names are listed in functions_test_data.txt

    def setUp(self):
        self.functions_test_data_file = "%s/functions_test_data.txt" % (CURRENTDIRPATH)
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
            "spacebeforebrackets"
        ]

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
            "spacebeforebrackets"
        ]

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
            'TestSpacebeforebrackets'
        ]

    def test_function_names_formatted_to_class_name_correctly(self):
        returnedValue = create_tests.convert_function_name_to_unittest_class_name(self.functionList)

        self.assertEqual(returnedValue, self.expectedReturn)


class TestCheckForExistingTestFile(unittest.TestCase):

    def setUp(self):
        open("/home/vagrant/CPTS/tests/create_tests.txt", "a").close()

    def tearDown(self):
        os.remove("/home/vagrant/CPTS/tests/create_tests.txt")

    def test_function_returns_true_if_file_already_exists(self):
        returnedValue = create_tests.check_for_existing_unittest_file("/home/vagrant/CPTS/create_tests.py")

        self.assertEqual(returnedValue, True)

    def test_function_returns_false_if_file_does_not_exists(self):
        returnedValue = create_tests.check_for_existing_unittest_file("/home/vagrant/CPTS/unknown.py")

        self.assertEqual(returnedValue, False)

    def test_function_only_looks_for_py_files(self):
        returnedValue = create_tests.check_for_existing_unittest_file("/home/vagrant/CPTS/create_tests.txt")

        self.assertEqual(returnedValue, False)


class TestCompareFunctionsInExistingTestFile(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_list_of_functions_returned(self):
        pass

    def test_existing_functions_are_excluded(self):
        pass

    def test_new_functions_are_included(self):
        pass


class TestWriteNewFunctionsToFile(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_file_is_created(self):
        pass

    def test_imports_are_added(self):
        pass

    def test_function_test_classes_are_added(self):
        pass

    def test_setup_and_teardown_are_added(self):
        pass


if __name__ == "__main__":
    unittest.main()
