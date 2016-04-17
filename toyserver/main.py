from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    content = """
    <html><head><title></title></head>
      <body>
        <pre>
              \
               \
                \\
                 \\
                  &gt;\/7
              _.-(6'  \
             (=___._/` \
                  )  \ |
                 /   / |
                /    &gt; /
               j    &lt; _\
           _.-' :      ``.
           \ r=._\        `.
          &lt;`\\_  \         .`-.
           \ r-7  `-. ._  ' .  `\
            \`,      `-.`7  7)   )
             \/         \|  \'  / `-._
                        ||    .'
                         \\  (
        Yeah, WOHOO!      &gt;\  &gt;
                      ,.-' &gt;.'
                     &lt;.'_.''
                       &lt;'
        </pre>
      </body>
    </html>
    """
    return content


if __name__ == "__main__":
    app.run()
