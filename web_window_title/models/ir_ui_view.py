# -*- coding: utf-8 -*-

import logging

from openerp import api, fields, models, _

_logger = logging.getLogger(__name__)

class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.cr_uid_ids_context
    def render(self, *args, **kwargs):
        if len(args) >= 4:
            template_id = args[2]
            if template_id in ['web.login', 'web.webclient_bootstrap']:
                qcontext = args[3]
                qcontext["title"] = self.pool['ir.config_parameter'].get_param(args[0], args[1], "web.base.title", "")
        return super(View, self).render(*args, **kwargs)
