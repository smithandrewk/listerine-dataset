# layout.py
from dash import html, dcc

def create_layout(participant_options, recording_options):
    return html.Div(
        className='main_app',
        children=[
            html.H1("Accelerometer Data with Labeled Intervals"),
            html.Div(
                className="main_panel",
                children=[
                    html.Div(
                        className="sidebar_panel",
                        children=[
                            html.Div(
                                className="participant_dropdown_group",
                                children=[
                                    html.H3("Participant ID"),
                                    dcc.Dropdown(options=participant_options, id='participant-dropdown')
                                ]
                            ),
                            html.Div(
                                className="recording_dropdown_group",
                                children=[
                                    html.H3("Recording ID"),
                                    dcc.Dropdown(options=recording_options, id='recording-dropdown')
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className="graph_panel",
                        children=[
                            dcc.Graph(id='acceleration-graph')
                        ]
                    )
                ]
            )
        ]
    )
