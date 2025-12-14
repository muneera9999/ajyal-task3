{
    'name': 'Educational Time Table Additional',
    'version': '17.0',
    'category': 'Extra Tools',
    'summary': 'Addition of Report in Timetable for Education erp',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': "http://www.educationalerp.com",
    'depends': ['base', 'education_core', 'education_time_table'],
    'data': [

        'security/ir.model.access.csv',
 
        'views/education_time_table_inherit.xml',
        'views/res_company_inherit.xml',

        'reports/timetable_report.xml',  

    ],
    
    'assets': {
    'web.report_assets_common': [
        'education_time_table_additional/static/description/logo.png'

    ],
},

    'application': False,
}
