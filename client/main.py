from flask import Flask, render_template

app = Flask(__name__, template_folder='flask')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/<path:page>')
def fallback(page):
    return render_template('index.html')

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", use_debugger=True)