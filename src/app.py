from dash import Dash, html

app = Dash(__name__)
# app.css.append_css({'external_url': '/assets/style.css'})


colors = {"background": "#262626", "text": "#7FDBFF", "panel":"#363636"}


app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    className='device_info',
    children=[
        html.H1(
            children="Hampd",
            className = "header_text",
        ),
        html.H5(
            children="Horizontal antenna pattern measurement device",
            className = "header_text",
        ),
        html.Div(
            style={"backgroundColor": colors["background"], "display":"table",},
            children=[
                html.Div(
                    className = "device_info",
                    children=[
                        html.H4(
                            children="HAMEG HMS3010",
                            className = "text",
                        ),
                        html.H4(
                            children="Connection: ok",
                            className = "text"
                        ),
                        html.H4(
                            children="State: ready",
                            className = "text",
                        ),
                    ],
                ),
                html.Div(
                    className="device_info",
                    children=[
                        html.H3(
                            children="Rotor device",
                            className = "text",
                        ),
                        html.H4(
                            children="Connection: ok",
                            className = "text",
                        ),
                        html.H4(
                            children="State: ready",
                            className = "text",
                        ),
                    ],
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
