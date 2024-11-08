import os
from unittest.mock import patch, call

from django.core.management import call_command
from django.test import TestCase, override_settings


class TestLoadDataCommand(TestCase):

    def setUp(self):
        super().setUp()

        self.copy_patcher = patch(
            'smart_fixtures.management.commands.loaddata.shutil.copy'
        )
        self.mock_copy = self.copy_patcher.start()

        self.listdir_patcher = patch(
            'smart_fixtures.management.commands.loaddata.os.listdir'
        )
        self.mock_listdir = self.listdir_patcher.start()

        self.makedirs_patcher = patch(
            'smart_fixtures.management.commands.loaddata.os.makedirs'
        )
        self.mock_makedirs = self.makedirs_patcher.start()

        self.isfile_patcher = patch(
            'smart_fixtures.management.commands.loaddata.os.path.isfile',
        )
        self.mock_isfile = self.isfile_patcher.start()

        self.base_handle_patcher = patch(
            'django.core.management.commands.loaddata.Command.handle'
        )
        self.mock_base_handle = self.base_handle_patcher.start()

        self.write_patcher = patch(
            'django.core.management.base.OutputWrapper.write'
        )
        self.mock_write = self.write_patcher.start()

        self.mocked_copied_files_message = 'Copied files message'
        self.create_copied_files_message_patcher = patch(
            'smart_fixtures.management.commands.loaddata'
            '.create_copied_files_message',
            return_value=self.mocked_copied_files_message
        )
        self.mock_create_copied_files_message = (
            self.create_copied_files_message_patcher.start()
        )

    @override_settings(FIXTURES={
        'labels': ['portfolio', 'link', 'skill'],
        'media': [
            {'src': 'path/to/src1', 'dest': 'path/to/dest1'},
            {'src': 'path/to/src2', 'dest': 'path/to/dest2'}
        ]
    })
    def test_handle(self):
        self.mock_listdir.side_effect = [
            ['image1.jpg', 'image2.png'],  # Files for src1
            ['image3.jpg', 'image4.png']  # Files for src2
        ]
        # Simulate that the first file in src2 does not exist:
        self.mock_isfile.side_effect = [True, True, False, True]

        call_command('loaddata', '--all')

        self.mock_base_handle.assert_called_once()
        call_args, _ = self.mock_base_handle.call_args
        self.assertEqual(call_args, ('portfolio', 'link', 'skill'))

        expected_makedirs_calls = [
            call(dir_path, exist_ok=True)
            for dir_path in ['path/to/dest1', 'path/to/dest2']
        ]
        self.mock_makedirs.assert_has_calls(
            expected_makedirs_calls,
            any_order=True
        )

        self.mock_copy.assert_has_calls([
            call(
                os.path.join('path/to/src1', 'image1.jpg'),
                os.path.join('path/to/dest1', 'image1.jpg')
            ),
            call(
                os.path.join('path/to/src1', 'image2.png'),
                os.path.join('path/to/dest1', 'image2.png')
            ),
            call(
                os.path.join('path/to/src2', 'image4.png'),
                os.path.join('path/to/dest2', 'image4.png')
            )
        ])
        self.mock_write.assert_called_once_with(
            self.mocked_copied_files_message
        )

    @override_settings(FIXTURES={
        'labels': ['portfolio', 'link', 'skill'],
        'media': [
            {'src': 'path/to/src1', 'dest': 'path/to/dest1'}
        ]
    })
    def test_handle_with_no_files(self):
        self.mock_listdir.return_value = []

        call_command('loaddata', '--all')

        self.mock_base_handle.assert_called_once()
        call_args, _ = self.mock_base_handle.call_args
        self.assertEqual(call_args, ('portfolio', 'link', 'skill'))

        self.mock_makedirs.assert_called_once_with(
            'path/to/dest1',
            exist_ok=True
        )
        self.mock_copy.assert_not_called()
        self.mock_write.assert_called_once_with(
            self.mocked_copied_files_message
        )

    @override_settings(FIXTURES={
        'labels': ['portfolio', 'link', 'skill'],
    })
    def test_handle_without_specified_media(self):
        call_command('loaddata', '--all')
        self.mock_base_handle.assert_called_once()
        call_args, _ = self.mock_base_handle.call_args
        self.assertEqual(call_args, ('portfolio', 'link', 'skill'))
        self.mock_makedirs.assert_not_called()
        self.mock_copy.assert_not_called()
        self.mock_write.assert_called_once_with(
            self.mocked_copied_files_message
        )

    @override_settings(FIXTURES=None)
    def test_handle_with_invalid_fixtures_setting_variable(self):
        expected_message = (
            'In order to use "loaddata" command with "--all" flag, '
            'you must set FIXTURES settings variable and it must a '
            'valid dictionary with "labels" list or tuple'
        )

        with override_settings(FIXTURES=None):
            call_command('loaddata', '--all')
        self.mock_base_handle.assert_called_once()
        self.mock_makedirs.assert_not_called()
        self.mock_copy.assert_not_called()
        self.mock_write.assert_called_once_with(expected_message)

        self.mock_write.reset_mock()
        self.mock_base_handle.reset_mock()

        with override_settings(FIXTURES='INVALID'):
            call_command('loaddata', '--all')
        self.mock_base_handle.assert_called_once()
        self.mock_makedirs.assert_not_called()
        self.mock_copy.assert_not_called()
        self.mock_write.assert_called_once_with(expected_message)

        self.mock_write.reset_mock()
        self.mock_base_handle.reset_mock()

        with override_settings(FIXTURES={'still': 'invalid'}):
            call_command('loaddata', '--all')
        self.mock_base_handle.assert_called_once()
        self.mock_makedirs.assert_not_called()
        self.mock_copy.assert_not_called()
        self.mock_write.assert_called_once_with(expected_message)

    def tearDown(self):
        super().tearDown()
        self.copy_patcher.stop()
        self.listdir_patcher.stop()
        self.makedirs_patcher.stop()
        self.isfile_patcher.stop()
        self.base_handle_patcher.stop()
        self.write_patcher.stop()
        self.create_copied_files_message_patcher.stop()
