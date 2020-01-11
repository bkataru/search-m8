from flask import Flask, render_template, send_file

app = Flask(__name__)

@app.route('/')
def main():
    return send_file("static/pages/home.html")
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="6969", use_debugger=True)