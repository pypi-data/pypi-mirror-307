/* Copyright 2024 Manuel Regidor - Sygel
License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html). */

odoo.define("remaining_days_widget_reformat_state", function (require) {
    "use strict";

    var basic_fields = require("web.basic_fields");

    basic_fields.RemainingDays.include({
        _render: function () {
            this._super.apply(this, arguments);
            if (this.nodeOptions.reformat && (
                !this.nodeOptions.reformat_states || this.nodeOptions.reformat_states.includes(this.recordData.state)
            )) {
                this.$el.removeClass();
            }
        },
    });
})
