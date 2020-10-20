import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import dash_table
import pandas as pd


# adding boostrap in
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = dbc.Container(
#     dbc.Alert("Hello Bootstrap!", color="success"), className="p-5"
# )


df = pd.read_csv("result.csv")
df.drop(["home_halfgoal_odds", "away_halfgoal_odds"], axis=1, inplace=True)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        # [
        #     html.Label("Dropdown"),
        #     dcc.Dropdown(
        #         options=[
        #             {"label": "New York City", "value": "NYC"},
        #             {"label": u"Montréal", "value": "MTL"},
        #             {"label": "San Francisco", "value": "SF"},
        #         ],
        #         value="MTL",
        #     ),
        # ],
        # style={"columnCount": 2},
        dcc.Dropdown(
            id="dropdown_selection",
            options=[
                {"label": i, "value": i} for i in sorted(df["fixture_title"].unique())
            ],
            # value=sorted(df["fixture_title"].unique()),
            multi=True,
        ),
        dash_table.DataTable(
            id="datatable-paging",
            columns=[{"name": i, "id": i} for i in sorted(df.columns)],
            page_current=0,
            page_size=5,
            page_action="custom",
        ),
    ]
)


# print(df.loc[df["fixture_title"] == "Manchester Utd vs Chelsea"])
# print(df.loc[df["fixture_title"] == "Manchester Utd vs Chelsea"].to_dict("records"))


@app.callback(
    Output("datatable-paging", "data"),
    [Input("dropdown_selection", "value"), Input("datatable-paging", "page_size")],
)
def update_table(value, page_size):

    print("---------")
    print(value)

    if value:
        output = df.loc[df["fixture_title"] == value[0]]
        final_output = output.to_dict("records")
        return final_output
        # return df.loc[df['fixture_title'] == value].to_dict('records')
    return None


if __name__ == "__main__":
    app.run_server(debug=True)
