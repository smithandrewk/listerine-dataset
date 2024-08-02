
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



    return fig

if __name__ == '__main__':
    app.run_server(debug=True)