# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "zuain",
    "summary": "Personalizaciones pedidas por Zuain",
    "version": "13.0.1.0.0",
    "category": "Misc",
    "website": "https://github.com/juanpgarza/zuain-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "product_pricelist", # adhoc
        ],
    "data": [
            'views/product_product_views.xml',
            'views/product_template_views.xml',
        ],
    "installable": True,
}
