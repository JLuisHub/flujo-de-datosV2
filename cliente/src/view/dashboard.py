##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: dashboard.py
# Capitulo: Flujo de Datos
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 1.0.0 Noviembre 2022
# Descripción:
#
#   Este archivo define los elementos visuales de la pantalla
#   del tablero
#
#-------------------------------------------------------------------------
from src.controller.dashboard_controller import DashboardController
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import date
import dash

app = dash.Dash(__name__)

class Dashboard:

    def __init__(self):
        pass

    def document(self):
        return dbc.Container(
            fluid = True,
            children = [
                html.Br(),
                self._header_title("Sales Report"),
                html.Div(html.Hr()),
                self._header_subtitle("Sales summary financial report"),
                html.Br(),
                self._highlights_cards(),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._bar_chart_providers_by_location(),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._bar_chart_sales_per_location(),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._bar_chart_orders_per_location(),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._panel_best_sellers(),
                                    width=6
                                ),
                                dbc.Col(
                                    self._panel_worst_sales(),
                                    width=6
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._panel_most_selled_products(),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    self._panel_most_selled_products2(),
                                    width=12
                                ),
                            ]
                        )
                    ]
                ),
                html.Br(),
            ]
        )

    def _header_title(self, title):
        return dbc.Row(
            [
                dbc.Col(html.H2(title, className="display-4"))
            ]
        )

    def _header_subtitle(self, subtitle):
        return html.Div(
            [
                html.P(
                    subtitle,
                    className="lead",
                ),
            ],
            id="blurb",
        )

    def _card_value(self, label, value):
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H2(value, className="card-title"),
                    ]
                ),
                dbc.CardFooter(label),
            ]
        )

    def _highlights_cards(self):
        products = DashboardController.load_products()
        orders = DashboardController.load_orders()
        providers = DashboardController.load_providers()
        locations = DashboardController.load_locations()
        sales = DashboardController.load_sales()
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            self._card_value("Products", products["products"])
                        ),
                        dbc.Col(
                            self._card_value("Orders", orders["orders"])
                        ),
                        dbc.Col(
                            self._card_value("Providers", providers["providers"])
                        ),
                        dbc.Col(
                            self._card_value("Locations", locations["locations"])
                        ),
                        dbc.Col(
                            self._card_value("Sales", "$ {:,.2f}".format(float(sales['sales'])))
                        ),
                    ]
                ),
            ]
        )

    def _bar_chart_providers_by_location(self):
        data = DashboardController.load_providers_per_location()
        bar_char_fig = px.bar(data, x="location", y="providers")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Providers per location", className="card-title"),
                        dcc.Graph(
                            id='providers-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _bar_chart_sales_per_location(self):
        data = DashboardController.load_sales_per_location()
        bar_char_fig = px.bar(data, x="location", y="sales")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Sales per location", className="card-title"),
                        dcc.Graph(
                            id='sales-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _bar_chart_orders_per_location(self):
        data = DashboardController.load_orders_per_location()
        bar_char_fig = px.bar(data, x="location", y="orders")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Orders per location", className="card-title"),
                        dcc.Graph(
                            id='orders-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _panel_best_sellers(self):
        best_sellers = DashboardController.load_best_sellers()
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Best sellers", className="card-title"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- [{sale['invoice']}] $ {sale['total']:,.2f}", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for sale in best_sellers
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    def _panel_worst_sales(self):
        worst_sales = DashboardController.load_worst_sales()
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Worst sales", className="card-title"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- [{sale['invoice']}] $ {sale['total']:,.2f}", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for sale in worst_sales
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    def _panel_most_selled_products(self):
        most_selled = DashboardController.load_most_selled_products()
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Most selled", className="card-title"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- {product['product']} [{product['times']} time(s) sold]", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for product in most_selled
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    
    def _panel_most_selled_products2(self):
        most_selled = DashboardController.load_most_selled_products2()
        return html.Div(
            [
                dcc.DatePickerRange(
                id='datepicker-range',
                min_date_allowed=date(2023, 1, 1),
                max_date_allowed=date(2023, 4, 12),
                initial_visible_month=date(2023, 1, 1),
                end_date=date(2023, 4, 12)
                ),
                html.Button('Buscar', id='button'),
                html.Div(id='output-container-date-picker-range'),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("BEST SELLER BY DATE RANGE", className="card-title2"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- d {product['date']} // d {product['product']} // t {product['times']}", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for product in most_selled
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    
    