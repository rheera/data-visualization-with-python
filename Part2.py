import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html, no_update

# Read the wildfire data into pandas dataframe
df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
)
# Extract year and month from the date column
df["Month"] = pd.to_datetime(
    df["Date"]
).dt.month_name()  # used for the names of the months
df["Year"] = pd.to_datetime(df["Date"]).dt.year


# Create app

# add tailwind to make styling easier later on
external_scripts = [{"src": "https://cdn.tailwindcss.com"}]
app = Dash(__name__, external_scripts=external_scripts)
# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True


# Layout Section of Dash

app.layout = html.Div(
    children=[
        html.H1(
            "Australia Wildfire Dashboard",
            className="mt-8 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl",
        ),
        html.Div(
            [
                html.Label(
                    "Regions: ", className="text-base font-semibold text-gray-900"
                ),
                html.P(
                    "Which region would you like to display?",
                    className="text-sm text-gray-500",
                ),
                html.Fieldset(
                    children=[
                        html.Legend("Selected Region", className="sr-only"),
                        html.Div(
                            children=[
                                dcc.RadioItems(
                                    [
                                        {
                                            "label": "New South Wales",
                                            "value": "NSW",
                                        },
                                        {
                                            "label": "Northern Territory",
                                            "value": "NT",
                                        },
                                        {
                                            "label": "Queensland",
                                            "value": "QL",
                                        },
                                        {
                                            "label": "South Australia",
                                            "value": "SA",
                                        },
                                        {
                                            "label": "Tasmania",
                                            "value": "TA",
                                        },
                                        {
                                            "label": "Victoira",
                                            "value": "VI",
                                        },
                                        {
                                            "label": "Western Australia",
                                            "value": "WA",
                                        },
                                    ],
                                    "NSW",
                                    id="input-region",
                                    className="flex items-center radio-btns flex-wrap",
                                    inline=True,
                                )
                            ],
                            className="space-y-4 sm:flex sm:items-center sm:space-x-10 sm:space-y-0",
                        ),
                    ],
                    className="mt-4",
                ),
            ],
            className="mt-4",
        ),
        html.Div(
            [
                html.Label(
                    "Year:",
                    className="text-base font-semibold text-gray-900",
                    htmlFor="year",
                ),
                html.P(
                    "Which year would you like to display?",
                    className="text-sm text-gray-500",
                ),
                dcc.Dropdown(df.Year.unique(), value=2005, id="input-year"),
            ],
            className="mt-4",
        ),
        html.Div(
            [dcc.Graph(id="pie-plot"), dcc.Graph(id="bar-plot")],
            className="mt-10 grid max-w-xl grid-cols-1 gap-8 text-base leading-7 text-gray-700 lg:max-w-none lg:grid-cols-2",
        ),
    ],
    className="flex flex-col items-center",
)


@callback(
    [
        Output(component_id="pie-plot", component_property="figure"),
        Output(component_id="bar-plot", component_property="figure"),
    ],
    [
        Input(component_id="input-region", component_property="value"),
        Input(component_id="input-year", component_property="value"),
    ],
)
def get_graph(entered_region, entered_year):
    up_df = df[(df["Year"] == int(entered_year)) & (df["Region"] == (entered_region))]

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    updf_pie = (
        up_df[["Estimated_fire_area", "Month"]].groupby("Month").mean().reset_index()
    )

    pie_fig = px.pie(
        updf_pie,
        values="Estimated_fire_area",
        names="Month",
        category_orders={
            "Month": month_order,
        },
        title=f"{entered_region}: Average Estimated Fire Area by Month in year {entered_year}",
    )

    updf_bar = up_df[["Count", "Month"]].groupby("Month").mean()
    updf_bar = updf_bar.reindex(month_order, axis=0).reset_index()
    bar_fig = px.bar(
        updf_bar,
        x="Month",
        y="Count",
        color_discrete_sequence=["#C45A9A"],
        title=f"{entered_region}: Average Count of Pixels for Presumed Vegetation Fires in year {entered_year}",
    )

    return [pie_fig, bar_fig]


if __name__ == "__main__":
    app.run_server()
