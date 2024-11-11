# -*- coding: utf-8 -*-
import os
import string
import random
import time
import subprocess
import sdk_test

CURPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class TestACMELogs(sdk_test.TestSdk):
    def test_002_acme_logs(self):
        init_script = os.path.join(CURPATH, 'tests', 'data', 'init-acme-logs.sh')

        app_id = self.app_id
        domains = [ self.apex ]

        cert_id = self.client.set_le_cert(domains=domains, acme_csr_type='rsa')
        self.assertIsInstance(cert_id, int)

        command = "/usr/bin/bash {} {}".format(init_script, cert_id)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
        self.assertEqual(result.returncode, 0)

        data, count = self.client.get_acme_logs(cert_id)
        self.assertEqual(len(data), 100)
        self.assertEqual(count, 100)
