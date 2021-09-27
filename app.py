from flask import Flask
from wsgiref.simple_server import make_server

app = Flask(__name__)

@app.route('/')
def index():
    return "/api/v1/hello-world-2"

@app.route('/api/v1/hello-world-<var_num>')
def DynamicUrl(var_num):
    return "<h1>" + "Hello World " + str(var_num) + "</h1>"

# simple run
# if __name__ == "__main__":
#     app.run()    

with make_server("", 8000, app) as server:
    print("Serving on port 8000...\nVisit http://127.0.0.1:8000")

    server.serve_forever()