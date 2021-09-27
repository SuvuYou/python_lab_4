from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "/api/v1/hello-world-2"

@app.route('/api/v1/hello-world-<var_num>')
def DynamicUrl(var_num):
    return "Hello World " + str(var_num)

if __name__ == "__main__":
    app.run()    