# Copyright 2026 AITIC S.A.S <https://aitic.com.ar>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from types import SimpleNamespace
from unittest.mock import patch

from requests.exceptions import Timeout

from odoo import fields
from odoo.exceptions import AccessError, UserError
from odoo.tests import TransactionCase, new_test_user, tagged


CLIENT_PATH = "odoo.addons.l10n_ar_edi_ux.models.arca_service_status.Client"


@tagged("post_install", "-at_install")
class TestArcaServiceStatus(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.write({
            "country_id": cls.env.ref("base.ar").id,
            "l10n_ar_afip_ws_environment": "testing",
        })
        cls.Status = cls.env["l10n_ar.afip.service.status"]
        cls.testing = cls.env.ref("l10n_ar_edi_ux.arca_service_status_testing")
        cls.production = cls.env.ref("l10n_ar_edi_ux.arca_service_status_production")
        (cls.testing | cls.production).write({
            "wsfe_status": "unknown", "wsaa_status": "unknown",
            "check_date": False, "wsfe_error": False, "wsaa_error": False,
        })
        fixture_env = cls.env(context={**cls.env.context, "no_reset_password": True})
        cls.user = new_test_user(
            fixture_env, login="arca_status_internal", groups="base.group_user",
            company_id=cls.company.id, company_ids=[(6, 0, cls.company.ids)],
        )
        cls.portal = new_test_user(fixture_env, login="arca_status_portal", groups="base.group_portal")

    def _mock_client(self, client):
        client.return_value.service.FEDummy.return_value = SimpleNamespace(
            AppServer="OK", DbServer="OK", AuthServer="OK",
        )

    def test_cached_read_does_not_contact_arca_or_invent_availability(self):
        with patch(CLIENT_PATH) as client:
            info = self.Status.with_user(self.user).get_status_info()
        client.assert_not_called()
        self.assertTrue(info["enabled"])
        self.assertEqual(info["environment"], "testing")
        self.assertEqual(info["wsfe"]["status"], "unknown")
        self.assertFalse(info["last_check"])

    def test_manual_refresh_checks_both_services_and_updates_cache(self):
        with patch(CLIENT_PATH) as client:
            self._mock_client(client)
            info = self.Status.with_user(self.user).refresh_status()
        self.assertEqual(client.call_count, 2)
        client.return_value.service.FEDummy.assert_called_once_with()
        urls = [call.args[0] for call in client.call_args_list]
        self.assertIn("wswhomo.afip.gov.ar", urls[0])
        self.assertIn("wsaahomo.afip.gov.ar", urls[1])
        for call in client.call_args_list:
            transport = call.kwargs["transport"]
            self.assertEqual(transport.load_timeout, 10)
            self.assertEqual(transport.operation_timeout, 10)
            self.assertTrue(transport.session.verify)
        self.assertEqual(info["wsfe"]["status"], "available")
        self.assertEqual(info["wsaa"]["status"], "available")
        self.assertEqual(info["last_check"], fields.Datetime.to_string(self.testing.check_date))
        self.assertFalse(self.production.check_date)

    def test_wsfe_failure_is_not_hidden_by_wsaa_success(self):
        with patch(CLIENT_PATH) as client:
            self._mock_client(client)
            client.return_value.service.FEDummy.return_value.DbServer = "FAIL"
            info = self.Status.with_user(self.user).refresh_status()
        self.assertEqual(info["wsfe"]["status"], "unavailable")
        self.assertIn("FAIL", info["wsfe"]["error"])
        self.assertEqual(info["wsaa"]["status"], "available")

    def test_timeouts_replace_previous_success(self):
        self.testing.write({"wsfe_status": "available", "wsaa_status": "available"})
        with patch(CLIENT_PATH, side_effect=Timeout("fixture timeout")):
            with self.assertLogs("odoo.addons.l10n_ar_edi_ux", level="WARNING"):
                info = self.Status.with_user(self.user).refresh_status()
        self.assertEqual(info["wsfe"]["status"], "unavailable")
        self.assertEqual(info["wsaa"]["status"], "unavailable")
        self.assertTrue(info["last_check"])

    def test_regular_user_cannot_write_or_select_arbitrary_company(self):
        with self.assertRaises(AccessError):
            self.testing.with_user(self.user).write({"wsfe_status": "available"})
        other = self.env["res.company"].create({
            "name": "ARCA inaccessible company", "country_id": self.env.ref("base.ar").id,
        })
        with self.assertRaises(AccessError):
            self.Status.with_user(self.user).with_context(
                allowed_company_ids=other.ids,
            ).refresh_status()

    def test_portal_cannot_read_or_trigger_network_requests(self):
        with patch(CLIENT_PATH) as client:
            for method in ("get_status_info", "refresh_status"):
                with self.assertRaises(AccessError):
                    getattr(self.Status.with_user(self.portal), method)()
        client.assert_not_called()

    def test_missing_environment_does_not_contact_arca(self):
        self.company.l10n_ar_afip_ws_environment = False
        with patch(CLIENT_PATH) as client:
            info = self.Status.get_status_info()
            self.assertFalse(info["environment"])
            with self.assertRaises(UserError):
                self.Status.refresh_status()
        client.assert_not_called()

    def test_company_switch_uses_its_own_environment(self):
        other = self.env["res.company"].create({
            "name": "ARCA production company", "country_id": self.env.ref("base.ar").id,
            "l10n_ar_afip_ws_environment": "production",
        })
        self.user.company_ids |= other
        self.testing.write({"wsfe_status": "available"})
        with patch(CLIENT_PATH) as client:
            self._mock_client(client)
            info = self.Status.with_user(self.user).with_company(other).refresh_status()
        self.assertEqual(info["environment"], "production")
        self.assertIn("servicios1.afip.gov.ar", client.call_args_list[0].args[0])
        self.assertTrue(self.production.check_date)
        self.assertFalse(self.testing.check_date)
