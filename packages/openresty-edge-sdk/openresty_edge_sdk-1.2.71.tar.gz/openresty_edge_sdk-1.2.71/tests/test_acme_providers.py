# -*- coding: utf-8 -*-
# import io
import sdk_test
import time
import random

class TestAcmeProviders(sdk_test.TestSdk):
    def test_acme_providers(self):
        # create
        now = random.randint(1, int(time.time()))
        endpoint = "https://acme.zerossl.com/v2/DV90"
        email = "oredge-sdk@openresty.com"
        eab_hmac_key = "abcdefghijklmnopqrstuvwxyz"
        eab_kid = "_DPxNuSfLTqcD3331Q49wT30OaelCTWsEOJuMPf_dL4"
        provider_id = self.client.new_acme_provider(name=f"amce_providers_{now}",
                                                 endpoint=endpoint,
                                                 eab_hmac_key=eab_hmac_key,
                                                 eab_kid=eab_kid, email=email)
        self.assertIsInstance(provider_id, int)

        # get
        acme_provider = self.client.get_acme_provider(provider_id)
        self.assertEqual(acme_provider.get('name'), f"amce_providers_{now}")
        self.assertEqual(acme_provider.get('endpoint'), endpoint)
        self.assertEqual(acme_provider.get('email'), email)
        self.assertEqual(acme_provider.get('eab_hmac_key'), eab_hmac_key)
        self.assertEqual(acme_provider.get('eab_kid'), eab_kid)

        # modify
        new_time = random.randint(1, int(time.time()))
        new_endpoint = "https://acme.zerossl.com/v2/DV90new"
        new_email = "oredge-sdk-new@openresty.com"
        new_eab_hmac_key = "abcdefghijklmnopqrstuvwxyz-new"
        new_eab_kid = "_DPxNuSfLTqcD3331Q49wT30OaelCTWsEOJuMPf_dL4_new"
        ok = self.client.put_acme_provider(id=provider_id,
                                           name=f"amce_providers_{new_time}",
                                           endpoint=new_endpoint,
                                           eab_hmac_key=new_eab_hmac_key,
                                           eab_kid=new_eab_kid, email=new_email)
        self.assertTrue(ok)

        acme_provider = self.client.get_acme_provider(provider_id)
        self.assertEqual(acme_provider.get('name'), f"amce_providers_{new_time}")
        self.assertEqual(acme_provider.get('endpoint'), new_endpoint)
        self.assertEqual(acme_provider.get('email'), new_email)
        self.assertEqual(acme_provider.get('eab_hmac_key'), new_eab_hmac_key)
        self.assertEqual(acme_provider.get('eab_kid'), new_eab_kid)

        acme_providers = self.client.get_all_acme_providers()
        self.assertEqual(len(acme_providers), 1)

        # delete
        ok = self.client.del_acme_provider(id=provider_id)
        self.assertTrue(ok)

        acme_providers = self.client.get_all_acme_providers()
        self.assertEqual(len(acme_providers), 0)


    def test_use_acme_provider(self):
        # create
        now = random.randint(1, int(time.time()))
        endpoint = "https://acme.zerossl.com/v2/DV90"
        email = "oredge-sdk@openresty.com"
        eab_hmac_key = "abcdefghijklmnopqrstuvwxyz"
        eab_kid = "_DPxNuSfLTqcD3331Q49wT30OaelCTWsEOJuMPf_dL4"
        provider_id = self.client.new_acme_provider(name=f"amce_providers_{now}",
                                                 endpoint=endpoint,
                                                 eab_hmac_key=eab_hmac_key,
                                                 eab_kid=eab_kid, email=email)
        self.assertIsInstance(provider_id, int)

        # get
        acme_provider = self.client.get_acme_provider(provider_id)
        self.assertEqual(acme_provider.get('name'), f"amce_providers_{now}")
        self.assertEqual(acme_provider.get('endpoint'), endpoint)
        self.assertEqual(acme_provider.get('email'), email)
        self.assertEqual(acme_provider.get('eab_hmac_key'), eab_hmac_key)
        self.assertEqual(acme_provider.get('eab_kid'), eab_kid)

        old_app_id = self.app_id
        domains = ['prefix' + self.apex]
        app_id = self.client.new_app(domains=domains, label=self.apex)
        self.client.use_app(app_id)

        cert_id = self.client.set_le_cert(domains=domains, acme_provider=provider_id, acme_csr_type='rsa')
        self.assertIsInstance(cert_id, int)

        self.client.use_app(old_app_id)

        ok = self.client.del_app(app_id)
        self.assertTrue(ok)

        ok = self.client.del_acme_provider(id=provider_id)
        self.assertTrue(ok)
