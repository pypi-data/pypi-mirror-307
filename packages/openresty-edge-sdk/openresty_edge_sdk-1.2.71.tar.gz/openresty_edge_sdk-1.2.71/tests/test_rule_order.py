# -*- coding: utf-8 -*-
# import io
import os
import random
import sdk_test
from edge2client.constants import OFF, ON

CURPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class TestRuleOrder(sdk_test.TestSdk):
    def test_rule_order(self):
        condition = [{'var': 'uri', 'op': 'eq', 'val': '/favicon.ico'}]
        conseq = [
            {'print': {
                'msg': 'hello'
            }}
        ]

        # new rule 1
        rule_id = self.client.new_rule(condition=condition, conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        rule_id1 = rule_id

        rule = self.client.get_rule(rule_id)
        self.assertEqual(rule['order'], 0)

        # new rule 2
        rule_id = self.client.new_rule(condition=condition, conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        rule_id2 = rule_id

        rule = self.client.get_rule(rule_id)
        self.assertEqual(rule['order'], 0)

        # new rule 3
        rule_id = self.client.new_rule(condition=condition, conseq=conseq, order=1)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        rule_id3 = rule_id

        rule = self.client.get_rule(rule_id)
        self.assertEqual(rule['order'], 1)

        conseq = {
            'user-code': {'el': 'true => exit(403);'}
        }

        # update rule 1, order does not change
        ok = self.client.put_rule(rule_id=rule_id1, conseq=conseq)
        self.assertEqual(ok, True)

        rule = self.client.get_rule(rule_id1)
        self.assertEqual(rule['order'], 0)

        # update rule 3, order does not change
        ok = self.client.put_rule(rule_id=rule_id, conseq=conseq)
        self.assertEqual(ok, True)

        rule = self.client.get_rule(rule_id)
        self.assertEqual(rule['order'], 1)

        # update rule 1, order changed
        ok = self.client.put_rule(rule_id=rule_id1, conseq=conseq, order=2)
        self.assertEqual(ok, True)

        rule = self.client.get_rule(rule_id1)
        self.assertEqual(rule['order'], 2)
