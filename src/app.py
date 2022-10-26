from sre_parse import State
import time
from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State

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
                                        html.Td(
                                            dcc.Input(
                                                id="hameg_sweep_min_frequency",
                                                type="number",
                                                value=1 * 10**6,
                                            )
                                        ),
                                    ],
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("State")),
                                        html.Td(html.P(id="hameg_state")),
                                        html.Td(html.H3("Sweep Max Frequency")),
                                        html.Td(
                                            dcc.Input(
                                                id="hameg_sweep_max_frequency",
                                                type="number",
                                                value=8 * 10**6,
                                            )
                                        ),
                                    ],
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("IDN")),
                                        html.Td(html.P(id="hameg_idn")),
                                        html.Td(html.H3("Frequency step")),
                                        html.Td(
                                            dcc.Input(
                                                id="hameg_frequency_step",
                                                type="number",
                                                value=100,
                                            )
                                        ),
                                    ],
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("Measurement Time")),
                                        html.Td(html.P(id="hameg_measurement_time")),
                                        html.Td(html.H3("Sweep Time")),
                                        html.Td(
                                            dcc.Input(
                                                id="hameg_sweep_time",
                                                type="number",
                                                value=0.2,
                                            )
                                        ),
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
                                        html.Td(
                                            dcc.Input(
                                                id="rotor_min_angle",
                                                type="number",
                                                value=90,
                                            )
                                        ),
                                    ]
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("State")),
                                        html.Td(html.P(id="rotor_state")),
                                        html.Td(html.H3("Max angle")),
                                        html.Td(
                                            dcc.Input(
                                                id="rotor_max_angle",
                                                type="number",
                                                value=270,
                                            )
                                        ),
                                    ]
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("Current Angle")),
                                        html.Td(html.P(id="rotor_angle")),
                                        html.Td(html.H3("Angle Step")),
                                        html.Td(
                                            dcc.Input(
                                                id="rotor_angle_step",
                                                type="number",
                                                value=5,
                                            )
                                        ),
                                    ]
                                ),
                                html.Tr(
                                    [
                                        html.Td(html.H3("Step Measurement cycles")),
                                        html.Td(html.P(id="step_measurement_cycles")),
                                        
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
        html.Button("START MEASUREMENT", id="start_stop_measurement", n_clicks=0),
    ],
)


@app.callback(
    Output("start_stop_measurement", "children"),
    Input("start_stop_measurement", "n_clicks"),
    State("hameg_measurement_time","children"),
    State("step_measurement_cycles","children")
)
def start_stop_measurement_button(n_clicks, hameg_measurement_time,step_measurement_cycles):
    if n_clicks % 2 == 0:
        return "START MEASUREMENT bla bla bla bla"
    else:
        return "STOP"


@app.callback(
    Output("hameg_connection", "children"),
    Output("hameg_state", "children"),
    Output("hameg_idn", "children"),
    Output("hameg_measurement_time", "children"),
    Output("rotor_connection", "children"),
    Output("rotor_state", "children"),
    Output("rotor_angle", "children"),
    Output("step_measurement_cycles", "children"),
    Input("url", "pathname"),
    Input("hameg_sweep_time", "value"),
    Input("hameg_sweep_min_frequency", "value"),
    Input("hameg_sweep_max_frequency", "value"),
    Input("hameg_frequency_step", "value"),
    Input("rotor_max_angle", "value"),
    Input("rotor_min_angle", "value"),
    Input("rotor_angle_step", "value"),
)
def callback_a(
    url,
    hameg_sweep_time,
    hameg_sweep_min_frequency,
    hameg_sweep_max_frequency,
    hameg_frequency_step,
    rotor_max_angle,
    rotor_min_angle,
    rotor_angle_step,
):
    hameg_connection = "Ok"
    hameg_state = "Ready"
    hameg_idn = f"idn stuff {12334.545345}"
    # hameg_sweep_time = 0.2
    # hameg_sweep_min_frequency = 1*10**6
    # hameg_sweep_max_frequency = 8*10**6
    # hameg_frequency_step = 100
    rotor_connection = "Ok"
    rotor_state = "Redy"
    rotor_angle = 12.4
    # rotor_min_angle = 90
    # rotor_max_angle = 270
    # rotor_angle_step = 0.2

    step_measurement_cycles = (rotor_max_angle - rotor_min_angle) / rotor_angle_step

    hameg_measurement_time = (
        hameg_sweep_time * (hameg_sweep_max_frequency - hameg_sweep_min_frequency)
    ) / hameg_frequency_step

    # TODO better representation of measurement time, convert seconds to hours and minutes
    # TODO nicer table, with breaking lines and light frame
    # TODO find out more parameters that need to be displayed

    return (
        hameg_connection,
        hameg_state,
        hameg_idn,
        # f"{hameg_sweep_time}s",
        f"{hameg_measurement_time / (60*60)}h",
        # f"{hameg_sweep_min_frequency}Hz",
        # f"{hameg_sweep_max_frequency}Hz",
        # f"{hameg_frequency_step}Hz",
        rotor_connection,
        rotor_state,
        rotor_angle,
        # rotor_min_angle,
        # rotor_max_angle,
        # rotor_angle_step,
        step_measurement_cycles
    )


if __name__ == "__main__":
    app.run_server(debug=True)
