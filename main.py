from flask import Flask

# creating a flask app and naming it "app"
app = Flask('app')


@app.route('/test', methods=['GET'])
def test():
    return 'Pinging Model Application!!'


if __name__ == "__main__":
    app.run(debug=True, port=9696)
