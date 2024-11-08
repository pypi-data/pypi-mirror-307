from django.test import TestCase, override_settings

from smart_fixtures.utils import create_copied_files_message


@override_settings(BASE_DIR='/home/app')
class TestCreateCopiedFilesMessage(TestCase):

    def test_create_copied_files_message_empty(self):
        file_path_pairs = []
        result = create_copied_files_message(file_path_pairs)
        self.assertEqual(result, 'No media files were copied')

    def test_create_copied_files_message_single_pair(self):
        file_path_pairs = [
            ('/home/app/src/file1.txt', '/home/app/dest/file1.txt')
        ]
        result = create_copied_files_message(file_path_pairs)
        expected_message = (
            'Copied files:\n'
            '1. src/file1.txt -> dest/file1.txt\n'
        )
        self.assertEqual(result, expected_message)

    def test_create_copied_files_message_multiple_pairs(self):
        file_path_pairs = [
            ('/home/app/src/file1.txt', '/home/app/dest/file1.txt'),
            ('/home/app/src/file2.txt', '/home/app/dest/file2.txt')
        ]
        result = create_copied_files_message(file_path_pairs)
        expected_message = (
            'Copied files:\n'
            '1. src/file1.txt -> dest/file1.txt\n'
            '2. src/file2.txt -> dest/file2.txt\n'
        )
        self.assertEqual(result, expected_message)

    def test_create_copied_files_message_base_dir_missmatch(self):
        file_path_pairs = [
            ('/home/project/src/file1.txt', '/home/project/dest/file1.txt')
        ]
        result = create_copied_files_message(file_path_pairs)
        expected_message = (
            'Copied files:\n'
            '1. /home/project/src/file1.txt -> /home/project/dest/file1.txt\n'
        )
        self.assertEqual(result, expected_message)
