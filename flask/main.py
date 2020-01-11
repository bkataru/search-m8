from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    if request.method == "POST":
        search = request.form['search']
        return url_for('search')
    else:
        return render_template('index.html')

@app.route('/search', methods=['POST'])
def main():
    if request.method == "POST":
        search = request.form['search']
        return url_for('search')
    else:
        return render_template('index.html')


    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", use_debugger=True)