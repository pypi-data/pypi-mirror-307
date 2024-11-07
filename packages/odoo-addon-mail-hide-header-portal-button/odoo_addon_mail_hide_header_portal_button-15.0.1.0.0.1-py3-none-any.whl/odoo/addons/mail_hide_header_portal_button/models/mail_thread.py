# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_classify_recipients(self, recipient_data, model_name, msg_vals=None):
        result = super()._notify_classify_recipients(
            recipient_data, model_name, msg_vals
        )
        for group in result:
            if group.get("notification_group_name") not in ["customer", "portal"]:
                group["has_button_access"] = False
        return result
