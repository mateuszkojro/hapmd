import time
from dash import Dash, html, dcc
from dash.dependencies import Output, Input

app = Dash(__name__)

app.layout = html.Div(
    className="device_info",
    children=[
        dcc.Location(id="url", refresh=False),
        html.H1(
            children="Hampd",
            className="header_text",
        ),
        html.H5(
            children="Horizontal antenna pattern measurement device",
            className="header_text",
        ),
        html.Div(
            className="device_grid",
            children=[
                html.Div(
                    className="device_info",
                    children=[
                        html.H2("HAMEG HMS3010", className="header_text"),
                        html.Table(
                            [
                                html.Tr(
                                    [
                                        html.Td(html.H3("Connection")),
                                        html.Td(html.P(id="hameg_connection")),
                                        html.Td(html.H3("Sweep Min Frequency")),
                                        html.Td(html.P(id="hameg_sweep_min_frequency")),
                                    ],
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("State")),
                                        html.Td(html.P(id="hameg_state")),
                                        html.Td(html.H3("Sweep max Frequency")),
                                        html.Td(html.P(id="hameg_sweep_max_frequency")),
                                    ],
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("IDN")),
                                        html.Td(html.P(id="hameg_idn")),
                                        html.Td(html.H3("Frequency step")),
                                        html.Td(html.P(id="hameg_frequency_step")),
                                    ],
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("Sweep Time")),
                                        html.Td(html.P(id="hameg_sweep_time")),
                                        html.Td(html.H3("Measurement Time")),
                                        html.Td(html.P(id="hameg_measurement_time")),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    className="device_info",
                    children=[
                        html.H2(
                            "Rotor device",
                            className="header_text",
                        ),
                        html.Table(
                            [
                                html.Tr(
                                    [
                                        html.Td(html.H3("Connection")),
                                        html.Td(html.P(id="rotor_connection")),
                                        html.Td(html.H3("Min angle")),
                                        html.Td(html.P(id="rotor_min_angle")),
                                    ]
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("State")),
                                        html.Td(html.P(id="rotor_state")),
                                        html.Td(html.H3("Max angle")),
                                        html.Td(html.P(id="rotor_max_angle")),
                                    ]
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("Angle")),
                                        html.Td(html.P(id="rotor_angle")),
                                        html.Td(html.H3("Angle Step")),
                                        html.Td(html.P(id="rotor_angle_step")),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("hameg_connection", "children"),
    Output("hameg_state", "children"),
    Output("hameg_idn", "children"),
    Output("hameg_sweep_time", "children"),
    Output("hameg_measurement_time", "children"),
    Output("hameg_sweep_min_frequency", "children"),
    Output("hameg_sweep_max_frequency", "children"),
    Output("hameg_frequency_step", "children"),
    Output("rotor_connection", "children"),
    Output("rotor_state", "children"),
    Output("rotor_angle", "children"),
    Output("rotor_min_angle", "children"),
    Output("rotor_max_angle", "children"),
    Output("rotor_angle_step", "children"),
    Input("url", "pathname"),
)
def callback_a(x):
    hameg_connection = "Ok"
    hameg_state = "Ready"
    hameg_idn = f"idn stuff {12334.545345}"
    hameg_sweep_time = 0.2
    hameg_sweep_min_frequency = 1*10**6
    hameg_sweep_max_frequency = 8*10**6
    hameg_frequency_step = 100
    rotor_connection = "Ok"
    rotor_state = "Redy"
    rotor_angle = 12.4
    rotor_min_angle = 90
    rotor_max_angle = 270
    rotor_angle_step = 0.2

    hameg_measurement_time = (
        hameg_sweep_time * (hameg_sweep_max_frequency - hameg_sweep_min_frequency)
    ) / hameg_frequency_step

    #TODO better representation of measurement time, convert seconds to hours and minutes 
    #TODO nicer table, with breaking lines and light frame
    #TODO find out more parameters that need to be displayed 
     
    return (
        hameg_connection,
        hameg_state,
        hameg_idn,
        f"{hameg_sweep_time}s",
        f"{hameg_measurement_time / (60*60)}h",
        f"{hameg_sweep_min_frequency}Hz",
        f"{hameg_sweep_max_frequency}Hz",
        f"{hameg_frequency_step}Hz",
        rotor_connection,
        rotor_state,
        rotor_angle,
        rotor_min_angle,
        rotor_max_angle,
        rotor_angle_step,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
