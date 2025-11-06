from dash import Dash
from env import PORT
from layout import add_layout

def main():
    app = Dash(__name__)
    add_layout(app)
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()