from flask import Flask, request

app = Flask(__name__)


@app.route('/model/summarize', methods=['POST'])
def summarize_text():
    print(request.json)
    return "Hello world"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
