from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    content = """
    <html><head><title></title></head>
      <body>
        <pre>
              \\
               \\
                \\\\
                 \\\\
                  >\\/7
              _.-(6'  \\
             (=___._/` \\
                  )  \\ |
                 /   / |
                /    > /
               j    < _\\
           _.-' :      ``.
           \\ r=._\\        `.
          <`\\\\_  \\         .`-.
           \\ r-7  `-. ._  ' .  `\\
            \\`,      `-.`7  7)   )
             \\/         \\|  \\'  / `-._
                        ||    .'
                        \\\\  (
       Yeah, WOHOO!      >\\  >
                      ,.-' >.'
                     <.'_.''
                       <'
        </pre>
      </body>
    </html>
    """
    return content


if __name__ == "__main__":
    app.run()
