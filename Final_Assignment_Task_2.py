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
                dcc.Dropdown(
                    options=[
                        {"label": "Yearly Statistics", "value": "Yearly"},
                        {"label": "Recession Period Statistics", "value": "Recession"},
                    ],
                    value="Yearly",
                    id="input-report",
                ),
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


def recession_graphs():
    vehicle_type_names = {
        "Supperminicar": "Super Mini Car",
        "Mediumfamilycar": "Medium Family Car",
        "Smallfamiliycar": "Small Family Car",
        "Sports": "Sports Car",
        "Executivecar": "Executive Car",
    }
    label_names = {
        "Automobile_Sales": "Automobile Sales",
        "Vehicle_Type": "Vehicle Type",
        "Advertising_Expenditure": "Advertising Expenditure",
        "unemployment_rate": "Unemployment Rate",
    }
    fig_line = px.line(
        df_rec[["Year", "Automobile_Sales"]].groupby("Year").mean().reset_index(),
        x="Year",
        y="Automobile_Sales",
        title="Average Automobile Sales by Year",
        color_discrete_sequence=["#C45A9A"],
        labels=label_names,
    )
    fig_line.show()
    bar_df = (
        df_rec[["Vehicle_Type", "Automobile_Sales"]]
        .groupby("Vehicle_Type")
        .mean()
        .reset_index()
    )
    bar_df["Vehicle_Type"] = bar_df["Vehicle_Type"].map(vehicle_type_names)
    fig_bar_1 = px.bar(
        bar_df,
        x="Vehicle_Type",
        y="Automobile_Sales",
        title="Average Automobile Sales by Vehicle Type",
        color_discrete_sequence=["#C45A9A"],
        labels=label_names,
    )
    fig_bar_1.show()
    pie_df = (
        df_rec[["Vehicle_Type", "Advertising_Expenditure"]]
        .groupby("Vehicle_Type")
        .sum()
        .reset_index()
    )
    pie_df["Vehicle_Type"] = pie_df["Vehicle_Type"].map(vehicle_type_names)
    fig_pie = px.pie(
        pie_df,
        values="Advertising_Expenditure",
        names="Vehicle_Type",
        title="Sum of Advertising Expenditure by Vehicle Type",
        labels=label_names,
    )
    fig_pie.show()
    bar2_df = (
        df_rec[["unemployment_rate", "Vehicle_Type", "Automobile_Sales"]]
        .groupby(["Vehicle_Type", "unemployment_rate"])
        .sum()
        .reset_index()
    )
    fig_bar_2 = px.bar(
        bar2_df,
        x="unemployment_rate",
        y="Automobile_Sales",
        color="Vehicle_Type",
        labels=label_names,
        title="Automobile Sales by Vehicle Type Per Unemployment Rate",
    )
    fig_bar_2.for_each_trace(
        lambda t: t.update(
            name=vehicle_type_names[t.name],
            legendgroup=vehicle_type_names[t.name],
            hovertemplate=t.hovertemplate.replace(t.name, vehicle_type_names[t.name]),
        )
    )
    fig_bar_2.show()


if __name__ == "__main__":
    app.run_server()

df_rec[["Year", "Automobile_Sales"]].groupby("Year").mean()
df_rec[["Vehicle_Type", "Automobile_Sales"]].groupby("Vehicle_Type").mean()

vehicle_type_names = {
    "Supperminicar": "Super Mini Car",
    "Mediumfamilycar": "Medium Family Car",
    "Smallfamiliycar": "Small Family Car",
    "Sports": "Sports Car",
    "Executivecar": "Executive Car",
}

pie_df = (
    df_rec[["Vehicle_Type", "Advertising_Expenditure"]]
    .groupby("Vehicle_Type")
    .sum()
    .reset_index()
)
pie_df["Vehicle_Type"] = pie_df["Vehicle_Type"].map(vehicle_type_names)

bar2_df = (
    df_rec[["unemployment_rate", "Vehicle_Type", "Automobile_Sales"]]
    .groupby(["Vehicle_Type", "unemployment_rate"])
    .sum()
    .reset_index()
)
px.bar(bar2_df, x="unemployment_rate", y="Automobile_Sales", color="Vehicle_Type")
df_rec.dtypes
df["Vehicle_Type"].unique()
