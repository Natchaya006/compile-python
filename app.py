from flask import Flask, render_template, request
import sys
from io import StringIO
import contextlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@app.route('/', methods=['POST'])
def getDataToCompile():
    with stdoutIO() as s:
        result = ''
        try:
            exec(request.form['input'])
        except:
            import traceback
            err = traceback.format_exc()
            out = err.split(', ')
            result = out[3] + ' ' + out[4]
    return s.getvalue() + result

if __name__ == '__main__':
    app.run(debug=True)
