/** @odoo-module **/

import { Component, onMounted, onWillStart, onWillUnmount, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { deserializeDateTime, formatDateTime } from "@web/core/l10n/dates";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const STATUS_MODEL = "l10n_ar.afip.service.status";

export class ArcaStatusSystray extends Component {
    static template = "l10n_ar_edi_ux.ArcaStatusSystray";
    static components = { Dropdown };
    static props = {};

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state = useState({
            enabled: false,
            environment: false,
            wsfe: { status: "unknown", error: false },
            wsaa: { status: "unknown", error: false },
            lastCheck: false,
            loading: false,
            error: false,
        });
        onWillStart(() => this.loadStatus());
        onMounted(() => {
            this.interval = browser.setInterval(() => this.loadStatus(), 5 * 60 * 1000);
        });
        onWillUnmount(() => browser.clearInterval(this.interval));
    }

    get lastCheckLabel() {
        return this.state.lastCheck
            ? formatDateTime(deserializeDateTime(this.state.lastCheck))
            : _t("Not checked yet");
    }

    get environmentLabel() {
        return this.state.environment === "production" ? _t("Production") : _t("Testing");
    }

    get hasFailure() {
        return !!this.state.error || [this.state.wsfe, this.state.wsaa].some(
            (service) => service.status === "unavailable"
        );
    }

    get services() {
        const labels = {
            available: _t("Available"),
            unavailable: _t("Unavailable"),
            unknown: _t("Not checked"),
        };
        return ["wsfe", "wsaa"].map((key) => ({
            key,
            name: key.toUpperCase(),
            ...this.state[key],
            label: labels[this.state[key].status],
        }));
    }

    async loadStatus(refresh = false) {
        if (this.state.loading) {
            return false;
        }
        this.state.loading = true;
        try {
            const info = await this.orm.call(
                STATUS_MODEL, refresh ? "refresh_status" : "get_status_info", []
            );
            Object.assign(this.state, {
                enabled: info.enabled,
                environment: info.environment,
                wsfe: info.wsfe,
                wsaa: info.wsaa,
                lastCheck: info.last_check,
                error: false,
            });
            return true;
        } catch {
            this.state.error = _t("Unable to retrieve ARCA status. Please try again.");
            this.state.wsfe = { status: "unknown", error: false };
            this.state.wsaa = { status: "unknown", error: false };
            if (refresh) {
                this.notification.add(this.state.error, { type: "danger" });
            }
            return false;
        } finally {
            this.state.loading = false;
        }
    }

    async onRefreshClick() {
        if (await this.loadStatus(true)) {
            const available = [this.state.wsfe, this.state.wsaa].every(
                (service) => service.status === "available"
            );
            this.notification.add(
                available ? _t("ARCA services are available.") : _t("An ARCA service is unavailable."),
                { type: available ? "success" : "warning" }
            );
        }
    }
}

registry.category("systray").add("l10n_ar_edi_ux.ArcaStatusSystray", {
    Component: ArcaStatusSystray,
}, { sequence: 1 });
