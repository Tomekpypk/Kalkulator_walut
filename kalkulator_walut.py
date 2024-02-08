from flask import Flask, render_template, request
import csv

app = Flask(__name__)
app.static_folder = 'static'



def load_exchange_rates():
    with open("kursy_walut.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        return list(reader)


@app.route('/', methods=['GET', 'POST'])
def index():
    rates = load_exchange_rates()

    if request.method == 'POST':
        selected_currency = request.form['currency']
        amount = float(request.form['amount'])

       
        selected_rate = next((rate for rate in rates if rate['code'] == selected_currency), None)

        if selected_rate:
            cost_in_pln = amount * float(selected_rate['ask'])
            return render_template('index.html', rates=rates, cost_in_pln=cost_in_pln)

    return render_template('index.html', rates=rates, cost_in_pln=None)

if __name__ == '__main__':
    app.run(debug=True)
