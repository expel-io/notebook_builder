import inspect
import os
import sys
from datetime import datetime

import mock
import pandas as pd
import pytest

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from hunt_tools.hunt import Hunt
import hunt_tools


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


class TestHunt():

    @pytest.fixture
    def hunt(self):
        return Hunt('/file/path')

    def test_normalize_hunt_df(self, hunt):
        '''
        Test that our get_df method returns our hunt_data
        '''
        columns = ['record_id', 'proc_first_seen', 'proc_last_seen', 'conn_first_seen', 'conn_last_seen', 'host',
                   'user', 'process_name', 'process_args', 'parent_name', 'domain', 'dest_ip', 'dest_port', 'netconns']
        test_obj = hunt.normalize_hunt_df(columns, pd.DataFrame(test_data))
        # print(test_obj.to_dict('records'))

        assert test_obj.to_dict('records') == [{'index': 0, 'process_first_seen': '2019-08-17T00:36:07', 'process_last_seen': '2019-09-30T00:36:07', 'connection_first_seen': '2019-08-17T00:37:29', 'connection_last_seen': '2019-09-30T00:37:39', 'process_name': 'w3wp.exe', 'process_args': 'c:\\windows\\systemDD\\inetsrv\\wDwp.exe -ap "clerkdocs"', 'parent_name': 'svchost.exe', 'user': 'IIS APPPOOL\\EvilClerk', 'host': 'clerk01', 'domain': 'api.dropboxapi.com', 'sensor_id': 425, 'dest_ip': '162.125.3.7', 'dest_port': 443, 'netconns': 45, 'event_id': 'cda92f81-db5f-4018-a6a4-e80e7a29b72d', 'record_id': '1000', 'proc_first_seen': '', 'proc_last_seen': '', 'conn_first_seen': '',
                                                'conn_last_seen': ''}, {'index': 1, 'process_first_seen': '2019-08-17T00:33:04', 'process_last_seen': '2019-09-30T00:33:04', 'connection_first_seen': '2019-08-17T00:34:27', 'connection_last_seen': '2019-09-30T00:34:30', 'process_name': 'cmd.exe', 'process_args': 'c:\\windows\\systemDD\\cmd.exe -ap "clerkdocs"', 'parent_name': 'powershell.exe', 'user': 'EVIL\\EvilUSER', 'host': 'user01', 'domain': 'api.test2.com', 'sensor_id': 427, 'dest_ip': '162.125.4.8', 'dest_port': 80, 'netconns': 47, 'event_id': '9f78d2d8-7171-4d2f-9fd2-c0413aa83184', 'record_id': '1001', 'proc_first_seen': '', 'proc_last_seen': '', 'conn_first_seen': '', 'conn_last_seen': ''}]
