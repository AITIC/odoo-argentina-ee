/** @odoo-module **/

import { ArcaStatusSystray } from "@l10n_ar_edi_ux/js/arca_status_systray";
import { localization } from "@web/core/l10n/localization";
import { patchTimeZone, patchWithCleanup } from "@web/../tests/helpers/utils";

QUnit.module("ARCA status");

QUnit.test("UTC timestamps use the user timezone, including date changes", (assert) => {
    patchTimeZone(-180);
    patchWithCleanup(localization, { dateTimeFormat: "dd/MM/yyyy HH:mm:ss" });
    const component = Object.create(ArcaStatusSystray.prototype);
    component.state = { lastCheck: "2026-11-05 01:30:00" };
    assert.strictEqual(component.lastCheckLabel, "04/11/2026 22:30:00");
});

QUnit.test("manual refresh calls the live endpoint and displays its new result", async (assert) => {
    const component = Object.create(ArcaStatusSystray.prototype);
    component.state = { loading: false };
    component.orm = {
        async call(model, method, args) {
            assert.strictEqual(model, "l10n_ar.afip.service.status");
            assert.strictEqual(method, "refresh_status");
            assert.deepEqual(args, []);
            return {
                enabled: true, environment: "testing", last_check: "2026-11-05 12:00:00",
                wsfe: { status: "available", error: false },
                wsaa: { status: "unavailable", error: "Timeout" },
            };
        },
    };
    component.notification = {
        add(message, options) { assert.strictEqual(options.type, "warning"); },
    };
    await component.onRefreshClick();
    assert.strictEqual(component.state.wsaa.status, "unavailable");
    assert.strictEqual(component.state.lastCheck, "2026-11-05 12:00:00");
    assert.strictEqual(component.state.loading, false);
});

QUnit.test("RPC failures never display a successful refresh or stale green status", async (assert) => {
    const component = Object.create(ArcaStatusSystray.prototype);
    component.state = {
        loading: false, wsfe: { status: "available" }, wsaa: { status: "available" },
    };
    component.orm = { async call() { throw new Error("fixture RPC failure"); } };
    component.notification = {
        add(message, options) { assert.strictEqual(options.type, "danger"); },
    };
    await component.onRefreshClick();
    assert.strictEqual(component.state.wsfe.status, "unknown");
    assert.strictEqual(component.state.wsaa.status, "unknown");
    assert.strictEqual(component.hasFailure, true);
    assert.strictEqual(component.state.loading, false);
});

QUnit.test("a second click while checking does not duplicate the request", async (assert) => {
    const component = Object.create(ArcaStatusSystray.prototype);
    component.state = { loading: true };
    component.orm = { call() { assert.step("unexpected RPC"); } };
    component.notification = { add() { assert.step("unexpected notification"); } };
    await component.onRefreshClick();
    assert.verifySteps([]);
});
