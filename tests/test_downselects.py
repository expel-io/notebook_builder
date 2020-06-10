import inspect
import os
import sys
from datetime import datetime
from unittest.mock import MagicMock

import pandas as pd
import pytest

import hunt_tools
from hunt_tools.downselects import Downselects

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


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