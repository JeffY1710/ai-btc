from dash import Dash, html

def main():
    app = Dash(__name__)
    app.layout = html.Div(children='Hello World')
    app.run()

if __name__ == "__main__":
    main()
