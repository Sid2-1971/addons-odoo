# -*- coding: utf-8 -*-

{
    'name': 'Site Under Maintenance',
    'category': 'Technical Settings',
    'author': "techspawn solution",
    'website': "www.techspawn.com",
    'summary': 'Put your site under maintenance',
    'description': """
Site Under Maintenance Module
=============================================
* This module gives feature,only administrator lock the system for maintenance reasons.
* When your site or server is under to maintenance then it will not allow normal users to login in.
* In system only Admin can login. 
* Normal user can login after finishing maintenance.
* Admin can send notification email to the normal users or customers when site is under maintenance.
""",
    'external_dependencies': {
        'python': ['simplejson']
    },
    'website': "http://www.techspawn.com",
    'version': '0.1',
    'depends': [
        'web','mail',
    ],
    'images': ['static/description/main.jpg'],
    'data': [
        "data/ir_config_parameter_data.xml",
        "data/mail.xml",
        "views/webclient_templates.xml",
        "views/change_menu_color.xml",
    ],
    'qweb': [
        'static/src/xml/dashboard.xml',
        'static/src/xml/reminder_topbar.xml',
    ],
}
