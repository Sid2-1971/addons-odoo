# -*- coding: utf-8 -*-


import simplejson
from odoo.addons.web.controllers.main import ensure_db, Session, Home
from odoo.http import request
from odoo.tools import SUPERUSER_ID
from odoo import http, fields, _
from odoo.exceptions import AccessError
import werkzeug.utils,odoo,logging
from odoo.addons.web_settings_dashboard.controllers.main import WebSettingsDashboard as WSD






class SessionFun(object):

    def session_check(self, db, login, password):
        uid = db and login and password and request.session.authenticate(db, login, password)
        sid = request.httprequest.session.sid
        ir_par_obj = request.env['ir.config_parameter'].sudo()
        is_site_under_maintenance = bool(int(ir_par_obj.get_param('under_maintenance')))
        if uid != SUPERUSER_ID and is_site_under_maintenance:
            return False
        self.session_save(uid, sid)
        return True

    def session_save(self, uid, sid):
        now = fields.datetime.now()
        session_obj = request.env['ir.session'].sudo()
        cr = request.env.cr

        cr.autocommit(True)

        sessions = session_obj.search([
            ('session_id', '=', sid),
            ('user_id', '=', uid),
            ('is_logged_in', '=', True),
        ])

        if not sessions:
            values = {
                'user_id': uid,
                'is_logged_in': True,
                'session_id': sid,
                'login_date': now,
            }
            session_obj.create(values)
            cr.commit()



class SiteUnderMaintenance(http.Controller):

    @http.route(['/ajax/session/'], type='http', auth="public", website=True)
    def web_session_check(self, *args, **kwargs):
        json_result = []

        irp_session_obj = request.env['ir.session'].sudo()
        site_session_history = irp_session_obj.search([
            ('session_id', '=', request.session.sid),
            ('user_id', '=', request.session.uid),
        ])
        if site_session_history and not site_session_history.is_logged_in:
            request.session.logout()

        if request.session.uid is None:
            json_result.append({'result': 'true'})
        else:
            json_result.append({'result': 'false'})
        content = simplejson.dumps(json_result)
        return request.make_response(content, [('Content-Type', 'application/json;charset=utf-8')])

    @http.route('/site_under_maintenance/toggle', type='http', auth='user')
    def site_under_maintenance(self, *args, **kwargs):
        
        ensure_db()
        if request.env.uid != SUPERUSER_ID:
            raise AccessError(_("Access Denied"))
        
        redirect = request.params and 'redirect' in request.params and request.params['redirect'] or '/web'
        irp_par = request.env['ir.config_parameter'].sudo()
        session_obj = request.env['ir.session'].sudo()
        
        under_maintenance = 0 if bool(eval(irp_par.get_param('under_maintenance'))) else 1
        irp_par.set_param('under_maintenance', under_maintenance)
        if under_maintenance:
            sessions = session_obj.search([
                ('user_id', '!=', SUPERUSER_ID),
                ('is_logged_in', '=', True),
            ])
            if sessions:
                sessions.close_sessions()
    
        return werkzeug.utils.redirect(redirect, 303)





class WebSettingsDashboard(WSD):

    @http.route('/web_settings_dashboard/data', type='json', auth='user')
    def web_settings_dashboard_data(self, **kw):
        result = super(WebSettingsDashboard, self).web_settings_dashboard_data(**kw)
        irp_par = request.env['ir.config_parameter'].sudo()
        if 'share' in result:
            result["share"]["under_maintenance"] = bool(eval(irp_par.get_param('under_maintenance')))
            result["share"]["show_under_maintenance"] = True if request.uid == SUPERUSER_ID else False
        return result



class SiteHome(Home, SessionFun):

    @http.route('/web/login', type='http', auth="none", sitemap=False)
    def web_login(self, redirect=None, *args, **kw):
        ensure_db()
        request.params['login_success'] = False

        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
        
            old_uid = request.uid
            db = request.session.db
            login = request.params.get('login', None)
            password = request.params.get('password', None)
            
            result = self.session_check(db, login, password)
            if result:
                request.params['login_success'] = True
            else:
                request.uid = old_uid
                values['error'] = _('Sorry, site is under maintenance!!!!!!!! Please, try again later.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        if request.params['login_success']:
            return http.redirect_with_hash('/web')

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect(redirect, 303)




class SiteSession(Session, SessionFun):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        old_uid = request.uid
        result = self.session_check(db, login, password)
        if not result:
            password = None
            request.uid = old_uid
        return super(SiteSession, self).authenticate(db, login, password, base_location=base_location)







