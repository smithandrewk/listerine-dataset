# layout.py
from dash import html, dcc

def create_layout(participant_options, recording_options):
    participant_options = [{'label': str(participant), 'value': participant} for participant in participant_options]
    recording_options = [{'label': str(recording), 'value': recording} for recording in recording_options]

    initial_participant = participant_options[0]['value'] if participant_options else None
    initial_recording = recording_options[0]['value'] if recording_options else None

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
                                    dcc.Dropdown(options=participant_options, value=initial_participant, id='participant-dropdown')
                                ]
                            ),
                            html.Div(
                                className="recording_dropdown_group",
                                children=[
                                    html.H3("Recording ID"),
                                    dcc.Dropdown(options=recording_options, value=initial_recording, id='recording-dropdown')
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
