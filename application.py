import os
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        print(request.form)
        # get input
        total_isk = request.form['total_isk']
        tenure_modifier = request.form['tenure_modifier']
        if not tenure_modifier:
            tenure_modifier = 0.35
        finder = request.form['finder']
        raw_names = request.form['names'].strip().split("\n")
        # parse list of names 
        pilots = []
        tenured_pilot_count = 0
        for name in raw_names:
            pilot = {
                "name": name.split('\t')[0],
                "tenured": name.split('\t')[1].rstrip()
            }
            print(pilot)
            if pilot['tenured'].upper() == 'TRUE':
                tenured_pilot_count += 1
            pilots.append(pilot)

        tenured_pilot_shares = tenured_pilot_count * 1
        untenured_pilot_shares = (len(pilots) - (tenured_pilot_count)) * (1 - float(tenure_modifier))
        
        if finder:
            finders_fee = float(total_isk) * 0.1
            total_isk = float(total_isk) * 0.9 
            
        share_value = float(total_isk) / (tenured_pilot_shares + untenured_pilot_shares)
        
        print(share_value)

        for pilot in pilots:
            if pilot['tenured'].upper() == 'TRUE':
                pilot['payout'] = "%.2f" % share_value
            else:
                pilot['payout'] = "%.2f" % (share_value * (1 - float(tenure_modifier)))
            if pilot['name'] == finder: 
                pilot['payout'] = "%.2f" % (float(pilot['payout']) + finders_fee)

        return render_template("output.html", data=pilots)
    else:
        return render_template("input.html", message="Hello Flask!")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
