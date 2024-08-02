import os
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json
def load_data(id, recording):
    recording_path = f'{DATA_DIR}/4_cropped/{id}/{recording}'
    df = pd.read_csv(f'{recording_path}')
    return df

app = dash.Dash(__name__)
DATA_DIR = f'../'

# Load initial IDs and recordings
ids = sorted([int(dir) for dir in os.listdir(f'{DATA_DIR}/4_cropped')])
id = ids[0]
recordings = os.listdir(f'{DATA_DIR}/4_cropped/{id}')
recording = recordings[0] if recordings else None

# Create Dash app layout
app.layout = html.Div([
    html.H1("Accelerometer Data with Labeled Intervals", style={'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='id-dropdown',
            options=[{'label': str(id), 'value': str(id)} for id in ids],
            value=str(id),
            clearable=False,
            style={'width': '48%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='recording-dropdown',
            value=recording,
            placeholder="Select a recording",
            style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'}
        ),
    ], style={'marginBottom': '10px'}),
    dcc.Graph(id='acceleration-graph', style={'height': '80vh'})  # Set the height of the graph
])

# Update recording options based on selected ID
@app.callback(
    [Output('recording-dropdown', 'options'),
     Output('recording-dropdown', 'value')],
    [Input('id-dropdown', 'value')]
)
def update_recordings_dropdown(selected_id):
    recordings = os.listdir(f'{DATA_DIR}/4_cropped/{selected_id}')
    options = [{'label': recording, 'value': recording} for recording in sorted(recordings) if recording.endswith('.csv')]
    default_recording = recordings[0] if recordings else None
    return options, default_recording

# Load and update graph based on selected ID and recording
@app.callback(
    Output('acceleration-graph', 'figure'),
    [Input('id-dropdown', 'value'),
     Input('recording-dropdown', 'value')]
)
def update_graph(selected_id, selected_recording):
    labels_path = f'{DATA_DIR}/4_cropped/{selected_id}/{selected_recording.replace(".csv",".json")}'
    with open(f'{labels_path}', 'r') as f:
        labels = json.load(f)

    df = load_data(selected_id, selected_recording)

    # Plotting with Plotly Express
    fig = px.line(df.iloc[::1], x='timestamp', y=['x','y','z','x_gyr','y_gyr','z_gyr'])

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
        height=800  # Adjust the height of the graph here (in pixels)
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)