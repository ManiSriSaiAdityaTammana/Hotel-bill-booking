
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key

# Menu items and their prices
menu = {
    1: {"name": "FISH AND CHIPS", "price": 425.80},
    2: {"name": "SPAGHETTI", "price": 375.50},
    3: {"name": "PENNE PASTA", "price": 425.00},
    4: {"name": "DOUGHNUTS", "price": 180.00},
    5: {"name": "CHICKEN PIZZA", "price": 220.00},
    6: {"name": "RED BBQ CHICKEN", "price": 240.00},
    7: {"name": "APPOLO FISH", "price": 300.00},
    8: {"name": "BUBBLE TEA", "price": 320.00},
    9: {"name": "SOFT DRINKS", "price": 80.00},
    10: {"name": "ICE CREAMS", "price": 150.00},
    11: {"name": "WATER BOTTLE", "price": 50.00},
    12: {"name": "KUNAFA", "price": 280.00},
    13: {"name": "APRICOT DELIGHT", "price": 300.00}
}


class MenuItemForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[NumberRange(min=0)], default=0)


class OrderForm(FlaskForm):
    adults = IntegerField('Adults', validators=[NumberRange(min=0)], default=0)
    children = IntegerField('Children', validators=[NumberRange(min=0)], default=0)
    menu_items = FieldList(FormField(MenuItemForm), min_entries=13)
    submit = SubmitField('Calculate Total')


# Calculate total price for an order
def calculate_order(order, is_child=False):
    total = 0
    for item in order:
        price = menu[item]["price"]
        if is_child:
            price *= 0.6  # Apply 60% discount for children
        total += price * order[item]
    return total


# Apply discount based on the total bill
def apply_discount(total):
    if total < 10:
        return total - (total * 0.005)
    elif 10 <= total < 20:
        return total - (total * 0.01)
    elif 20 <= total < 30:
        return total - (total * 0.015)
    elif 30 <= total < 40:
        return total - (total * 0.02)
    else:
        return total - (total * 0.05)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    if form.validate_on_submit():
        total_price = 0
        orders = {}
        for i, item in enumerate(form.menu_items.entries):
            if item.data['quantity'] > 0:
                orders[i + 1] = item.data['quantity']
        for _ in range(form.adults.data):
            total_price += calculate_order(orders)
        for _ in range(form.children.data):
            total_price += calculate_order(orders, is_child=True)
        total_price = apply_discount(total_price)
        return render_template('result.html', total_price=total_price)
    return render_template('index.html', form=form, menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
