from dash import Dash, html, dash_table
import pandas as pd

from env import DATASET_URL, PORT

df = pd.read_csv(DATASET_URL)

def main():
    app = Dash(__name__)
    app.layout = [
        html.Div(children='BTC Prediction'),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10)
    ]
    app.run(port=PORT)

if __name__ == "__main__":
    main()