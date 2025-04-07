#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 06/04/2024
    Author: Joshua David Golafshan
"""


class HTMLReportGenerator:
    def __init__(self, title="Report"):
        self.title = title
        self.components = []  # List to store all components like tables, charts, etc.

    @staticmethod
    def create_tag(tag_name: str, classname: str, id_name: str, style: str, contents):
        # Initialize the html_element with the required opening part
        html_element = f"<{tag_name}"

        # Add class attribute if it's not None or empty
        if classname:
            html_element += f' class="{classname}"'

        # Add id attribute if it's not None or empty
        if id_name:
            html_element += f' id="{id_name}"'

        # Add style attribute if it's not None or empty
        if style:
            html_element += f' style="{style}"'

        # Close the html_element and add the contents
        html_element += f">{contents}</{tag_name}>"

        return html_element

    @staticmethod
    def create_table(dataframe, table_id="table"):
        """
        Creates an HTML table from a dataframe.
        """
        table_html = f"""
        <h2>{table_id}</h2>
        <table class="table table-striped" id="{table_id}">
          <thead>
            <tr>
        """

        # Add the table headers dynamically from the dataframe columns
        for col in dataframe.columns:
            table_html += f"<th scope='col'>{col}</th>"

        table_html += "</tr></thead><tbody>"

        # Add the table rows dynamically from the dataframe rows
        for index, row in dataframe.iterrows():
            table_html += "<tr>"
            for col in dataframe.columns:
                table_html += f"<td>{row[col]}</td>"
            table_html += "</tr>"

        # Close the table structure
        table_html += """
          </tbody>
        </table>
        """

        return table_html

    def add_component(self, component_html):
        """
        Adds an HTML component (table, chart, etc.) to the report.
        """
        self.components.append(component_html)

    def generate_html_report(self):
        """
        Combines the header, components (tables, charts, etc.), and footer into a full HTML report.
        """
        # Start with the header
        full_html = f"""
        <!doctype html>
        <html lang="en">
        <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <title>{self.title}</title>
        <style>
            .container {{
                max-width: 1300px;
            }}
            .table td, .table th {{
                padding: .15rem;
            }}
        </style>
        </head>
        <body>
            <div class="container" style="{"{@media (min-width: 1200px) {.container {max-width: 1340px;}}"}">
                {"".join(self.components)}
            </div>
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        </body>
        </html>
        """

        return full_html
