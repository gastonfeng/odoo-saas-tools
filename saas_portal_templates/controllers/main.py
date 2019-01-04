from odoo.addons.saas_portal.controllers.main import SaasPortal as saas_portal_controller
from odoo.addons.web.controllers.main import login_and_redirect

from odoo import http
from odoo.http import request


class SaasPortalTemplates(saas_portal_controller):
    ## \addtogroup url url入口
    @http.route(['/saas_portal_templates/select-template'], type='http', auth='public', website=True)
    ##  @ingroup url
    def select_template(self, **post):
        '''进入模版选择页面 ，/saas_portal_templates/select-template ，外部接口'''
        domain = [('state', 'in', ['confirmed'])]
        fields = ['id', 'name', 'summary']
        templates = request.env['saas_portal.plan'].sudo().search_read(domain=domain, fields=fields)
        values = {'templates': templates}
        return request.render("saas_portal_templates.select_template", values)

    ##  @bug AttributeError: 'SaasPortal (extended by SaasPortalDemo, SaasPortal' object has no attribute 'create_new_database'
    @http.route(['/saas_portal_templates/new_database'], type='http', auth='public', website=True)
    ##  @ingroup url
    ##  @ingroup newdatabase
    def new_database(self, **post):
        '''数据库创建入口：/saas_portal_templates/new_database?plan_id=x ,在select_template页面调用'''
        if not request.session.uid:
            return login_and_redirect()
        plan_id = int(post.get('plan_id'))

        res = self.create_new_database(plan_id)
        return request.redirect(res.get('url'))
