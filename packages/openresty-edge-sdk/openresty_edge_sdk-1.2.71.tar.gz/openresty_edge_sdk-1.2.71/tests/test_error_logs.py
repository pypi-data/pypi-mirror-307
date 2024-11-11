# -*- coding: utf-8 -*-
import os
import string
import random
import time
import subprocess
import sdk_test

CURPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class TestErrorLogs(sdk_test.TestSdk):
    app_id = None

    def test_001_init(self):
        init_script = os.path.join(CURPATH, 'tests', 'data', 'init-error-logs.sh')

        app_id = self.app_id
        TestErrorLogs.app_id = app_id

        command = "/usr/bin/bash {} {}".format(init_script, app_id)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
        self.assertEqual(result.returncode, 0)

    def test_002_node_error_logs(self):
        data, count = self.client.get_node_error_logs()
        self.assertEqual(len(data), count)
        self.assertTrue(count >= 0)

        start_time = 1728345983
        data, count = self.client.get_node_error_logs(start_time=start_time)
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

        end_time = 1728346598
        data, count = self.client.get_node_error_logs(start_time=start_time, end_time=end_time)
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 11)

        data, count = self.client.get_node_error_logs(start_time=start_time, req_id="000028800bac65d7fed03afd")
        self.assertEqual(len(data), 2)
        self.assertTrue(count == 2)

        data, count = self.client.get_node_error_logs(start_time=start_time, level="error")
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

        data, count = self.client.get_node_error_logs(start_time=start_time, level="warn")
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

        data, count = self.client.get_node_error_logs(start_time=start_time, level="crit")
        self.assertEqual(len(data), 0)
        self.assertTrue(count == 0)


    def test_003_admin_error_logs(self):
        data, count = self.client.get_admin_error_logs()
        self.assertEqual(len(data), count)
        self.assertTrue(count >= 0)

        start_time = 1528345600
        data, count = self.client.get_admin_error_logs(start_time=start_time)
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

        end_time = 1728345629
        data, count = self.client.get_admin_error_logs(start_time=start_time, end_time=end_time)
        self.assertEqual(len(data), 5)
        self.assertTrue(count == 5)

        data, count = self.client.get_admin_error_logs(start_time=start_time, req_id="000028800bac65d7fed03afd")
        self.assertEqual(len(data), 0)
        self.assertTrue(count == 0)

        data, count = self.client.get_admin_error_logs(start_time=start_time, level="error")
        self.assertEqual(len(data), 0)
        self.assertTrue(count == 0)

        data, count = self.client.get_admin_error_logs(start_time=start_time, level="warn")
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

    def test_004_log_server_error_logs(self):
        data, count = self.client.get_log_server_error_logs()
        self.assertEqual(len(data), count)
        self.assertTrue(count >= 0)

        start_time = 1528345600
        data, count = self.client.get_log_server_error_logs(start_time=start_time)
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

        end_time = 1728349200
        data, count = self.client.get_log_server_error_logs(start_time=start_time, end_time=end_time)
        self.assertEqual(len(data), 6)
        self.assertTrue(count == 6)

        data, count = self.client.get_log_server_error_logs(start_time=start_time, req_id="000028800bac65d7fed03afd")
        self.assertEqual(len(data), 0)
        self.assertTrue(count == 0)

        data, count = self.client.get_log_server_error_logs(start_time=start_time, level="error")
        self.assertEqual(len(data), 0)
        self.assertTrue(count == 0)

        data, count = self.client.get_log_server_error_logs(start_time=start_time, level="warn")
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

    def test_005_http_app_error_logs(self):
        self.app_id = TestErrorLogs.app_id
        self.client.use_app(self.app_id)

        data, count = self.client.get_http_app_error_logs()
        self.assertEqual(len(data), count)
        self.assertTrue(count >= 0)

        start_time = 1528345600
        data, count = self.client.get_http_app_error_logs(start_time=start_time)
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

        end_time = 1728346207
        data, count = self.client.get_http_app_error_logs(start_time=start_time, end_time=end_time)
        self.assertEqual(len(data), 5)
        self.assertTrue(count == 5)

        data, count = self.client.get_http_app_error_logs(start_time=start_time, req_id="0000270000b465d7f2f037f5")
        self.assertEqual(len(data), 1)
        self.assertTrue(count == 1)

        data, count = self.client.get_http_app_error_logs(start_time=start_time, level="crit")
        self.assertEqual(len(data), 0)
        self.assertTrue(count == 0)

        data, count = self.client.get_http_app_error_logs(start_time=start_time, level="error")
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)

        data, count = self.client.get_http_app_error_logs(start_time=start_time, level="warn")
        self.assertEqual(len(data), 10)
        self.assertTrue(count == 20)
