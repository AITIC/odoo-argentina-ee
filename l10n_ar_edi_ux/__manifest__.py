{
    'name': 'Argentinian Electronic Invoicing UX',
    'version': "17.0.1.11.0",
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'l10n_ar_ux',
        'l10n_ar_edi',
        'account_accountant',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/arca_service_status_data.xml',
        'views/res_partner_view.xml',
        'views/account_move_view.xml',
        'views/account_journal_view.xml',
        'views/l10n_ar_boarding_permission_view.xml',
        'wizards/res_partner_update_from_padron_wizard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'l10n_ar_edi_ux/static/src/js/arca_status_systray.js',
            'l10n_ar_edi_ux/static/src/xml/arca_status_systray.xml',
            'l10n_ar_edi_ux/static/src/scss/arca_status_systray.scss',
        ],
        'web.qunit_suite_tests': [
            'l10n_ar_edi_ux/static/src/js/arca_status_systray.js',
            'l10n_ar_edi_ux/static/src/xml/arca_status_systray.xml',
            'l10n_ar_edi_ux/static/tests/arca_status_systray_tests.js',
        ],
    },
    'demo': [
        'demo/res_partner_demo.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'post_load': 'monkey_patches',
}
