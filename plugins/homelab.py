#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Build a dashboard to link to my self-hosted services.
"""

__version__ = '0.0.2'

import meerschaum as mrsm
from meerschaum.plugins import dash_plugin, web_page

SERVICES_PIPE: mrsm.Pipe = mrsm.Pipe('homelab', 'links')

@dash_plugin
def init_dash(dash_app):

    import dash_bootstrap_components as dbc
    import dash.html as html
    from meerschaum.api.dash.components import build_cards_grid

    @web_page('/homelab', login_required=False)
    def homelab_links():
        try:
            docs = sorted(
                SERVICES_PIPE.get_data().to_dict(orient='records'),
                key = lambda x: x.get('service'),
            )
        except Exception as e:
            docs = []
        cards = [
            dbc.Card([
                dbc.CardImg(
                    src = doc.get('image'),
                    top = True,
                    class_name = 'align-self-center',
                    style = {
                        'height': '70px',
                        'width': 'auto',
                        'margin-top': '15px',
                    },
                ),
                dbc.CardBody(
                    [html.H4(doc.get('service'))] + (
                        [
                            dbc.CardLink(
                                "Private",
                                href = private,
                                target = "_blank",
                            )
                        ]
                        if (private := doc.get('private'))
                        else []
                    ) + (
                        [
                            dbc.CardLink(
                                "Public",
                                href = public,
                                target = "_blank",
                            )
                        ]
                        if (public := doc.get('public'))
                        else []
                    )
                ),
            ])
            for doc in docs
        ]


        return dbc.Container([
            html.H1(
                "BMeares Homelab Services",
                style = {
                    'margin-top': '25px',
                    'margin-bottom': '25px',
                },
            ),
            build_cards_grid(cards, 4),
        ])
