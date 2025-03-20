from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv, os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Map (URL)', validators=[URL(), DataRequired()])
    open_time = StringField('Open Time e.g. 9AM', validators=[DataRequired()])
    close_time = StringField('Close Time e.g. 5PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', 
                                choices=['☕️','☕️☕️','☕️☕️☕️','☕️☕️☕️☕️','☕️☕️☕️☕️☕️'],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength', 
                              choices=['✘','💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪'],
                              validators=[DataRequired()])
    power_availability = SelectField('Power Socket Availability',
                                     choices=['✘','🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'],
                                     validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

CSV_FILE_PATH = 'Flask/Coffee and Wifi/cafe-data.csv'

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_csv_row = [form.cafe.data, form.location.data, form.open_time.data, form.close_time.data,
                       form.coffee_rating.data, form.wifi_rating.data, form.power_availability.data]
        csv_header = ['Cafe Name','Location','Open','Close','Coffee','Wifi','Power']
        # print(new_csv_row)
        
        file_exists = os.path.exists(CSV_FILE_PATH)

        last_char = None
        with open(CSV_FILE_PATH, 'rb') as file:
            file.seek(-1, 2)  # Move to the last byte of the file
            last_char = file.read(1)
        
        with open(CSV_FILE_PATH, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(csv_header)
            
            if last_char != '\n':
                file.write('\n')
            
            # append a row to existing file
            writer.writerow(new_csv_row)

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
