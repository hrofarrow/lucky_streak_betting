import flask
import pickle

# Use pickle to load in the pre-trained model.
with open(f'model/mlb_betting.pkl', 'rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def main():

    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))


    if flask.request.method == 'POST':

        FIELD = flask.request.form['FIELD']
        Side_Line = flask.request.form['Side Line']
        OU_Line = flask.request.form['O/U Line']
        OU_Odds = flask.request.form['O/U_Odds']

        input_variables = pd.DataFrame([[FIELD, Side_Line, OU_Line, OU_Odds]],
                                       columns=['FIELD', 'Side Line', "OU Line", "OU_Odds"],
                                       dtype=float)

        prediction = model.predict(input_variables)[0]

    return flask.render_template('index.html',
                                     original_input={'FIELD':FIELD,
                                                     'Side_Line':Side_Line,
                                                     'O/U Line':OU_Line,
                                                     'O/U Odds':OU_Odds},
                                     result=prediction,
                                     )

if __name__ == '__main__':
    app.run()