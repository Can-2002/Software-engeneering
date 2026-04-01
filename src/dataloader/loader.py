import pandas as pd
def load_data(data):
    data = pd.read_csv(data)
    return data