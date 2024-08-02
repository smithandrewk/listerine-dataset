
import pandas as pd
DATA_DIR = f'../'

def load_data(id, recording):
    recording_path = f'{DATA_DIR}/4_cropped/{id}/{recording}'
    df = pd.read_csv(f'{recording_path}')
    return df