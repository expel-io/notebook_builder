import inspect
import os
import sys
from datetime import datetime
from unittest.mock import MagicMock

import mock
import pandas as pd
import pytest

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from hunt_tools.downselects import Downselects


class TestDownselects():

    test_data = [
        {
            "index": 0,
            "Process First Seen": "2019-08-17T00:36:07",
            "Process Last Seen": "2019-09-30T00:36:07",
            "Connection First Seen": "2019-08-17T00:37:29",
            "Connection Last Seen": "2019-09-30T00:37:39",
            "Process Name": "w3wp.exe",
            "Process Arguments": "c:\\windows\\systemDD\\inetsrv\\wDwp.exe -ap \"clerkdocs\"",
            "Parent Name": "svchost.exe",
            "User": "IIS APPPOOL\\EvilClerk",
            "Hostname": "clerk01",
            "Domain": "api.dropboxapi.com",
            "Sensor Id": 425,
            "Destination Ip": "162.125.3.7",
            "Destination Port": 443,
            "Connection Count": 45,
            "Event Id": "cda92f81-db5f-4018-a6a4-e80e7a29b72d"
        },
        {
            "index": 1,
            "Process First Seen": "2019-08-17T00:33:04",
            "Process Last Seen": "2019-09-30T00:33:04",
            "Connection First Seen": "2019-08-17T00:34:27",
            "Connection Last Seen": "2019-09-30T00:34:30",
            "Process Name": "cmd.exe",
            "Process Arguments": "c:\\windows\\systemDD\\cmd.exe -ap \"clerkdocs\"",
            "Parent Name": "powershell.exe",
            "User": "EVIL\\EvilUSER",
            "Hostname": "user01",
            "Domain": "api.test2.com",
            "Sensor Id": 427,
            "Destination Ip": "162.125.4.8",
            "Destination Port": 80,
            "Connection Count": 47,
            "Event Id": "9f78d2d8-7171-4d2f-9fd2-c0413aa83184"
        }
    ]

    @pytest.fixture
    def downselects(self):
        return Downselects(self.test_data)

    def test_get_df(self, downselects):
        '''
        Test that our get_df method returns our hunt_data
        '''
        assert downselects.get_df() == [
            {'index': 0, 'Process First Seen': '2019-08-17T00:36:07', 'Process Last Seen': '2019-09-30T00:36:07', 'Connection First Seen': '2019-08-17T00:37:29', 'Connection Last Seen': '2019-09-30T00:37:39', 'Process Name': 'w3wp.exe', 'Process Arguments': 'c:\\windows\\systemDD\\inetsrv\\wDwp.exe -ap "clerkdocs"',
                'Parent Name': 'svchost.exe', 'User': 'IIS APPPOOL\\EvilClerk', 'Hostname': 'clerk01', 'Domain': 'api.dropboxapi.com', 'Sensor Id': 425, 'Destination Ip': '162.125.3.7', 'Destination Port': 443, 'Connection Count': 45, 'Event Id': 'cda92f81-db5f-4018-a6a4-e80e7a29b72d'},
            {'index': 1, 'Process First Seen': '2019-08-17T00:33:04', 'Process Last Seen': '2019-09-30T00:33:04', 'Connection First Seen': '2019-08-17T00:34:27', 'Connection Last Seen': '2019-09-30T00:34:30', 'Process Name': 'cmd.exe', 'Process Arguments': 'c:\\windows\\systemDD\\cmd.exe -ap "clerkdocs"',
                'Parent Name': 'powershell.exe', 'User': 'EVIL\\EvilUSER', 'Hostname': 'user01', 'Domain': 'api.test2.com', 'Sensor Id': 427, 'Destination Ip': '162.125.4.8', 'Destination Port': 80, 'Connection Count': 47, 'Event Id': '9f78d2d8-7171-4d2f-9fd2-c0413aa83184'}
        ]

    def test_general_frequency_trend(self, monkeypatch, downselects):
        '''
        Test that our general_frequency_trend method returns the correct data
        '''
        monkeypatch.setenv('TESTING', '')

        test_obj = downselects.general_frequency_trend(['Domain'], 'Hostname', pd.DataFrame(self.test_data))
        # print(test_obj)

        assert test_obj.to_markdown() == '''| Domain             |   count |
|:-------------------|--------:|
| api.dropboxapi.com |       1 |
| api.test2.com      |       1 |'''

    def test_column_frequency_count(self, monkeypatch, downselects):
        '''
        Test that our general_frequency_trend method returns the correct data
        '''
        monkeypatch.setenv('TESTING', '')

        test_obj = downselects.column_frequency_count('Domain', pd.DataFrame(self.test_data))
        # print(test_obj.to_markdown())

        assert test_obj.to_markdown() == '''|    | Domain             |   count |
|---:|:-------------------|--------:|
|  0 | api.dropboxapi.com |       1 |
|  1 | api.test2.com      |       1 |'''

    def test_column_group(self, monkeypatch, downselects):
        '''
        Test that our column_group method returns the correct data
        '''
        monkeypatch.setenv('TESTING', '')

        test_obj = downselects.column_group(['User', 'Domain'], 'Domain', pd.DataFrame(self.test_data))
        # print(test_obj.to_markdown())

        assert test_obj.to_markdown() == '''|    | User                  | Domain             |
|---:|:----------------------|:-------------------|
|  0 | EVIL\EvilUSER         | api.test2.com      |
|  1 | IIS APPPOOL\EvilClerk | api.dropboxapi.com |'''

    def test_java_exploit(self, monkeypatch, downselects):
        '''
        Test that our java_exploit method returns the correct data
        '''
        monkeypatch.setenv('TESTING', '')

        java_test_data = [
            {
                "index": 0,
                "Process First Seen": "2019-08-17T00:36:07",
                "Process Last Seen": "2019-09-30T00:36:07",
                "Connection First Seen": "2019-08-17T00:37:29",
                "Connection Last Seen": "2019-09-30T00:37:39",
                "Process Name": "w3wp.exe",
                "Process Arguments": "c:\\windows\\systemDD\\inetsrv\\wDwp.exe -ap \"clerkdocs\"",
                "parent_name": "java.exe",
                "User": "IIS APPPOOL\\EvilClerk",
                "Hostname": "clerk01",
                "Domain": "api.dropboxapi.com",
                "Sensor Id": 425,
                "Destination Ip": "162.125.3.7",
                "Destination Port": 443,
                "Connection Count": 45,
                "Event Id": "cda92f81-db5f-4018-a6a4-e80e7a29b72d"
            },
            {
                "index": 1,
                "Process First Seen": "2019-08-17T00:33:04",
                "Process Last Seen": "2019-09-30T00:33:04",
                "Connection First Seen": "2019-08-17T00:34:27",
                "Connection Last Seen": "2019-09-30T00:34:30",
                "Process Name": "cmd.exe",
                "Process Arguments": "c:\\windows\\systemDD\\cmd.exe -ap \"clerkdocs\"",
                "parent_name": "javaw.exe",
                "User": "EVIL\\EvilUSER",
                "Hostname": "user01",
                "Domain": "api.test2.com",
                "Sensor Id": 427,
                "Destination Ip": "162.125.4.8",
                "Destination Port": 80,
                "Connection Count": 47,
                "Event Id": "9f78d2d8-7171-4d2f-9fd2-c0413aa83184"
            }
        ]

        test_obj = downselects.java_exploit(['User', 'Domain', 'parent_name'], pd.DataFrame(java_test_data))
        # print(test_obj.to_markdown())

        assert test_obj.to_markdown() == '''|    | User                  | Domain             | parent_name   |
|---:|:----------------------|:-------------------|:--------------|
|  0 | IIS APPPOOL\EvilClerk | api.dropboxapi.com | java.exe      |
|  1 | EVIL\EvilUSER         | api.test2.com      | javaw.exe     |'''

    def test_office_exploit(self, monkeypatch, downselects):
        '''
        Test that our office_exploit method returns the correct data
        '''
        monkeypatch.setenv('TESTING', '')

        office_test_data = [
            {
                "index": 0,
                "Process First Seen": "2019-08-17T00:36:07",
                "Process Last Seen": "2019-09-30T00:36:07",
                "Connection First Seen": "2019-08-17T00:37:29",
                "Connection Last Seen": "2019-09-30T00:37:39",
                "Process Name": "w3wp.exe",
                "Process Arguments": "c:\\windows\\systemDD\\inetsrv\\wDwp.exe -ap \"clerkdocs\"",
                "parent_name": "winword.exe",
                "User": "IIS APPPOOL\\EvilClerk",
                "Hostname": "clerk01",
                "Domain": "api.dropboxapi.com",
                "Sensor Id": 425,
                "Destination Ip": "162.125.3.7",
                "Destination Port": 443,
                "Connection Count": 45,
                "Event Id": "cda92f81-db5f-4018-a6a4-e80e7a29b72d"
            },
            {
                "index": 1,
                "Process First Seen": "2019-08-17T00:33:04",
                "Process Last Seen": "2019-09-30T00:33:04",
                "Connection First Seen": "2019-08-17T00:34:27",
                "Connection Last Seen": "2019-09-30T00:34:30",
                "Process Name": "cmd.exe",
                "Process Arguments": "c:\\windows\\systemDD\\cmd.exe -ap \"clerkdocs\"",
                "parent_name": "excel.exe",
                "User": "EVIL\\EvilUSER",
                "Hostname": "user01",
                "Domain": "api.test2.com",
                "Sensor Id": 427,
                "Destination Ip": "162.125.4.8",
                "Destination Port": 80,
                "Connection Count": 47,
                "Event Id": "9f78d2d8-7171-4d2f-9fd2-c0413aa83184"
            }
        ]

        test_obj = downselects.office_exploit(['User', 'Domain', 'parent_name'], pd.DataFrame(office_test_data))
        # print(test_obj.to_markdown())

        assert test_obj.to_markdown() == '''|    | User                  | Domain             | parent_name   |
|---:|:----------------------|:-------------------|:--------------|
|  0 | IIS APPPOOL\EvilClerk | api.dropboxapi.com | winword.exe   |
|  1 | EVIL\EvilUSER         | api.test2.com      | excel.exe     |'''

    def test_adobe_exploit(self, monkeypatch, downselects):
        '''
        Test that our adobe_exploit method returns the correct data
        '''
        monkeypatch.setenv('TESTING', '')

        adobe_test_data = [
            {
                "index": 0,
                "Process First Seen": "2019-08-17T00:36:07",
                "Process Last Seen": "2019-09-30T00:36:07",
                "Connection First Seen": "2019-08-17T00:37:29",
                "Connection Last Seen": "2019-09-30T00:37:39",
                "Process Name": "w3wp.exe",
                "Process Arguments": "c:\\windows\\systemDD\\inetsrv\\wDwp.exe -ap \"clerkdocs\"",
                "parent_name": "acrobat.exe",
                "User": "IIS APPPOOL\\EvilClerk",
                "Hostname": "clerk01",
                "Domain": "api.dropboxapi.com",
                "Sensor Id": 425,
                "Destination Ip": "162.125.3.7",
                "Destination Port": 443,
                "Connection Count": 45,
                "Event Id": "cda92f81-db5f-4018-a6a4-e80e7a29b72d"
            },
            {
                "index": 1,
                "Process First Seen": "2019-08-17T00:33:04",
                "Process Last Seen": "2019-09-30T00:33:04",
                "Connection First Seen": "2019-08-17T00:34:27",
                "Connection Last Seen": "2019-09-30T00:34:30",
                "Process Name": "cmd.exe",
                "Process Arguments": "c:\\windows\\systemDD\\cmd.exe -ap \"clerkdocs\"",
                "parent_name": "acrord32.exe",
                "User": "EVIL\\EvilUSER",
                "Hostname": "user01",
                "Domain": "api.test2.com",
                "Sensor Id": 427,
                "Destination Ip": "162.125.4.8",
                "Destination Port": 80,
                "Connection Count": 47,
                "Event Id": "9f78d2d8-7171-4d2f-9fd2-c0413aa83184"
            }
        ]

        test_obj = downselects.adobe_exploit(['User', 'Domain', 'parent_name'], pd.DataFrame(adobe_test_data))
        # print(test_obj.to_markdown())

        assert test_obj.to_markdown() == '''|    | User                  | Domain             | parent_name   |
|---:|:----------------------|:-------------------|:--------------|
|  0 | IIS APPPOOL\EvilClerk | api.dropboxapi.com | acrobat.exe   |
|  1 | EVIL\EvilUSER         | api.test2.com      | acrord32.exe  |'''

    def test_web_shell_exploit(self, monkeypatch, downselects):
        '''
        Test that our web_shell_exploit method returns the correct data
        '''
        monkeypatch.setenv('TESTING', '')

        web_test_data = [
            {
                "index": 0,
                "Process First Seen": "2019-08-17T00:36:07",
                "Process Last Seen": "2019-09-30T00:36:07",
                "Connection First Seen": "2019-08-17T00:37:29",
                "Connection Last Seen": "2019-09-30T00:37:39",
                "Process Name": "w3wp.exe",
                "Process Arguments": "c:\\windows\\systemDD\\inetsrv\\wDwp.exe -ap \"clerkdocs\"",
                "parent_name": "w3wp.exe",
                "User": "IIS APPPOOL\\EvilClerk",
                "Hostname": "clerk01",
                "Domain": "api.dropboxapi.com",
                "Sensor Id": 425,
                "Destination Ip": "162.125.3.7",
                "Destination Port": 443,
                "Connection Count": 45,
                "Event Id": "cda92f81-db5f-4018-a6a4-e80e7a29b72d"
            },
            {
                "index": 1,
                "Process First Seen": "2019-08-17T00:33:04",
                "Process Last Seen": "2019-09-30T00:33:04",
                "Connection First Seen": "2019-08-17T00:34:27",
                "Connection Last Seen": "2019-09-30T00:34:30",
                "Process Name": "cmd.exe",
                "Process Arguments": "c:\\windows\\systemDD\\cmd.exe -ap \"clerkdocs\"",
                "parent_name": "tomcat.exe",
                "User": "EVIL\\EvilUSER",
                "Hostname": "user01",
                "Domain": "api.test2.com",
                "Sensor Id": 427,
                "Destination Ip": "162.125.4.8",
                "Destination Port": 80,
                "Connection Count": 47,
                "Event Id": "9f78d2d8-7171-4d2f-9fd2-c0413aa83184"
            }
        ]

        test_obj = downselects.web_shell_exploit(['User', 'Domain', 'parent_name'], pd.DataFrame(web_test_data))
        # print(test_obj.to_markdown())

        assert test_obj.to_markdown() == '''|    | User                  | Domain             | parent_name   |
|---:|:----------------------|:-------------------|:--------------|
|  0 | IIS APPPOOL\EvilClerk | api.dropboxapi.com | w3wp.exe      |
|  1 | EVIL\EvilUSER         | api.test2.com      | tomcat.exe    |'''
