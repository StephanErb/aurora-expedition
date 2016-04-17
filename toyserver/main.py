from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    content = """
    <html><head><title></title></head>
      <body>
        <pre>
         ______________
        < Hello World! >
         --------------
                \   ^__^
                 \  (oo)\_______
                    (__)\       )\/
                        ||----w |
                        ||     ||
        </pre>
      </body>
    </html>
    """
    return content


if __name__ == "__main__":
    app.run()
