import os
import plotly.express as px
import dash
from dash import html,dcc
from dash.dependencies import Input, Output, State
import json
from lib.utils import *
from layout import create_layout

app = dash.Dash(__name__)


currently_selected_participant_id = 0
currently_selected_recording_id = 0

participant_ids = sorted([int(dir) for dir in os.listdir(f'{DATA_DIR}/4_cropped')])

app.layout = create_layout(participant_ids,os.listdir(f'{DATA_DIR}/4_cropped/{currently_selected_participant_id}'))

@app.callback([
    Output('recording-dropdown','options'),
    Input('participant-dropdown','value')
    ])
def user_changed_participant_dropdown_selection(selection):
    recordings = os.listdir(f'{DATA_DIR}/4_cropped/{selection}')
    options = [{'label': recording, 'value': recording} for recording in sorted(recordings) if recording.endswith('.csv')]
    default_recording = recordings[0] if recordings else None
    return options, default_recording

# @app.callback([Input('recording-dropdown','value')])
# def user_changed_recording_dropdown_selection(selection):
#     global currently_selected_recording_id
#     currently_selected_recording_id = selection
#     redraw()

# def redraw():
#     print(currently_selected_participant_id,currently_selected_recording_id)
#     df = load_data(currently_selected_participant_id, currently_selected_recording_id)
#     print(df)


if __name__ == '__main__':
    app.run_server(debug=True)