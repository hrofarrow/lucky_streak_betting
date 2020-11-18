from flask import Flask, request, jsonify
from model_files.ml_model import model

# creating a flask app and naming it "app"
app = Flask('app')


@app.route('/test', methods=['GET'])
def test():
    return 'Pinging Model Application!!'


if __name__ == "__main__":
    app.run(debug=True, port=9696)


@app.route('/predict', methods=['POST'])
def predict():
    vehicle = request.get_json()
    print(vehicle)
    with open('./model_files/model.bin', 'rb') as f_in:
        model = pickle.load(f_in)
        f_in.close()
    predictions = predict_mpg(vehicle, model)

    result = {
        'mpg_prediction': list(predictions)
    }
    return jsonify(result)