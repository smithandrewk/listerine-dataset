import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from layout import create_layout
from lib.utils import load_data,DATA_DIR
import json
import plotly.express as px

app = dash.Dash(__name__)

# TODO: load all data at beginning, or at least lazy load all recording for selected participant and also all 0 recordings for each aprticipant
participant_ids = sorted([int(dir) for dir in os.listdir(f'{DATA_DIR}/4_cropped')])
print(participant_ids)
recordings = sorted([int(file.replace('.csv','')) for file in os.listdir(f'{DATA_DIR}/4_cropped/0') if file.endswith('.csv')])

app.layout = create_layout(participant_ids, recordings)

@app.callback(
    Output('recording-dropdown', 'options'),
    Output('recording-dropdown', 'value'),
    Input('participant-dropdown', 'value'),
    prevent_initial_call=True
)
def user_changed_participant_dropdown_selection(selection):
    recordings = sorted([int(file.replace('.csv', '')) for file in os.listdir(f'{DATA_DIR}/4_cropped/{selection}') if file.endswith('.csv')])
    options = [{'label': str(recording), 'value': recording} for recording in recordings]
    value = recordings[0] if recordings else None
    return options,value

@app.callback(
    Output('acceleration-graph', 'figure'),
    [Input('participant-dropdown', 'value'),
     Input('recording-dropdown', 'value')],
)
def user_changed_recording_dropdown_selection(participant,recording):
    print(f'here! {participant} {recording}')
    df = load_data(participant, recording)
    labels_path = f'{DATA_DIR}/4_cropped/{participant}/{recording}.json'
    with open(f'{labels_path}', 'r') as f:
        labels = json.load(f)

    # Assuming you have a function to create a figure from the dataframe
    fig = create_figure(df,labels)
    return fig

def create_figure(df,labels):
    fig = px.line(df, x='timestamp', y=['x','y','z'])

    # Adding rectangles for labels
    for arm in labels:
        for label_type in labels[arm]:
            color = None
            if label_type == 'water':
                color = "Blue"
            elif label_type == 'listerine':
                color = "Green"
            else:
                color = "Black"

            for interval in labels[arm][label_type]:
                start = interval['start']
                end = interval['end']
                fig.add_shape(
                    type="rect",
                    xref="x",
                    yref="paper",
                    x0=start,
                    y0=0,
                    x1=end,
                    y1=1,
                    line=dict(color=color),
                    fillcolor=color,
                    opacity=0.5,
                )
    # Update layout with taller graph
    fig.update_layout(
        title="Accelerometer Data with Labeled Intervals",
        xaxis_title="Time (seconds)",
        yaxis_title="Acceleration (m/s^2)",
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
