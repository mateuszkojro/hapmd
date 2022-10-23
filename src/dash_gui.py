from dash import Dash, html

app = Dash(__name__)


colors = {"background": "#262626", "text": "#7FDBFF"}
device_info_style = {
    "backgroundColor": colors["background"],
    "width": "50%",
    "float": "left",
    "padding": "20px",
    "border": "2px",
    'margin': 0
}

app.layout = html.Div(
    style={"backgroundColor": colors["background"],'margin': 0},
    children=[
        html.H1(
            children="Hampd",
            style={
                "textAlign": "center",
                "color": colors["text"],
            },
        ),
        html.H5(
            children="Horizontal antenna pattern measurement device",
            style={
                "textAlign": "center",
                "color": colors["text"],
            },
        ),
        
        html.Div(
            style={"backgroundColor": colors["background"]},
            children=[
                html.Div(
                    style=device_info_style,
                    children=[
                        html.H4(
                            children="HAMEG HMS3010",
                            style={
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                        html.H4(
                            children="Connection: ok",
                            style={
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                        
                        html.H4(
                            children="State: ready",
                            style={
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                    ],
                ),
                html.Div(
                    style=device_info_style,
                    children=[
                        html.H3(
                            children="Rotor device",
                            style={
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                        html.H4(
                            children="Connection: ok",
                            style={
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                        html.H4(
                            children="State: ready",
                            style={
                                "textAlign": "left",
                                "color": colors["text"],
                            },
                        ),
                    ],
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
