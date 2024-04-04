import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html, no_update

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"

df = pd.read_csv(URL)
print("Data downloaded and read into a dataframe!")

df_rec = df[df["Recession"] == 1]

df_rec.head()

external_scripts = [{"src": "https://cdn.tailwindcss.com"}]
app = Dash(__name__, external_scripts=external_scripts)
# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

app.layout = html.Main(
    children=[
        html.H1(
            "Automobile Sales Statistics Dashboard",
            className="mt-8 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl",
        ),
        html.Div(
            [
                html.Label(
                    "Select Report Type:",
                    className="text-base font-semibold text-gray-900",
                    htmlFor="input-report",
                ),
                html.P(
                    "Which report would you like to display, yearly or recession?",
                    className="text-sm text-gray-500",
                ),
                dcc.Dropdown(["Yearly", "Recession"], "Yearly", id="input-report"),
            ],
            className="mt-4",
        ),
        html.Div(
            [
                html.Label(
                    "Year:",
                    className="text-base font-semibold text-gray-900",
                    htmlFor="input-year",
                ),
                html.P(
                    "Which year would you like to display for the yearly report?",
                    className="text-sm text-gray-500",
                ),
                dcc.Dropdown(
                    df.Year.unique(), value=2005, id="input-year", disabled=True
                ),
            ],
            className="mt-4",
        ),
    ],
    className="flex flex-col items-center",
)


@callback(Output("input-year", "disabled"), Input("input-report", "value"))
def disable_year(report_value):
    if report_value == "Recession":
        return True
    else:
        return False


if __name__ == "__main__":
    app.run_server()
