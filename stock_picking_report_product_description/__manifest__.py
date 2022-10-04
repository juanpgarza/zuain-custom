# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock picking report product description",    
    "summary": "Change the product description in the stock reports",
    "version": "15.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/juanpgarza/zuain-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        'views/report_stockpicking_operations.xml',
        ],
    "development_status": "Production/Stable",        
    "installable": True,
}
