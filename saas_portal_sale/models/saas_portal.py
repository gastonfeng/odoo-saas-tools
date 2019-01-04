from odoo import models, fields, api



class SaasPortalPlan(models.Model):
    _inherit = 'saas_portal.plan'

    free_subdomains = fields.Boolean(
        help='allow to choose subdomains for trials otherwise allow only after payment',
        default=True)
    non_trial_instances = fields.Selection(
        [('from_trial', 'From trial'), ('create_new', 'Create new')],
        string='Non-trial instances',
        help='Whether to use trial database or create new one when user make payment',
        required=True, default='create_new')
    product_tmpl_id = fields.Many2one('product.template', 'Product')

    product_variant_ids = fields.One2many('product.product',
                                          'saas_plan_id',
                                          'Product variants')

    ##  \addtogroup    newdatabase    创建数据库
    ##  @{
    ## SaasPortalPlan#_new_database_vals:继承函数，创建分析账户，返回分析账户id
    ##  @}
    @api.multi
    ##  @todo    创建合同明细
    ## @ingroup newdatabase
    def _new_database_vals(self, vals):
        '''继承函数，创建分析账户，返回分析账户id
        '''
        vals = super(SaasPortalPlan, self)._new_database_vals(vals)

        contract = self.env['account.analytic.account'].sudo().create({
            'name': vals['name'],
            'partner_id': vals['partner_id'],
            'recurring_invoices': True,
        })

        vals['contract_id'] = contract.id
        return vals



class SaasPortalClient(models.Model):
    _inherit = 'saas_portal.client'

    contract_id = fields.Many2one(
        'account.analytic.account',
        string='Contract',
        readonly=True,
    )
