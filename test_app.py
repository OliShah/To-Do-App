import unittest
from unittest.mock import patch, mock_open
import json 
from app import read_tasks

class TestReadTasks(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='[{"Task":"Task 1" }]')
    @patch("os.path.exists")
    def test_read_tasks_file_exists(self, mock_exists, mock_file):
        mock_exists.return_value=True 

        result = read_tasks()

        expected = [{"Task":"Task 1"}]
        self.assertEqual(result, expected)

    @patch("os.path.exists")
    def test_read_tasks_file_not_exists(self, mock_exists):
        mock_exists.return_value = False

        result = read_tasks()

        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='invalid_json')
    @patch("os.path.exists")
    def test_read_tasks_invalid_json(self, mock_exists, mock_file):
        mock_exists.return_value = True

        with self.assertRaises(json.JSONDecodeError):
            read_tasks()

if __name__ == "__main__":
    unittest.main()
