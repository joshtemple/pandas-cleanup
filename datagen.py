import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

product_names = {
    'CONE': ['Dipped Waffle Cone', 'Sugar Cone', 'Waffle Cone', 'Cookie Cone', 'Brownie Cone'],
    'MISC': ['Ice Cream Cake'],
    'ICE CREAM': ['Vanilla Bean', 'Dark Chocolate', 'Strawberry', 'Peanut Fudge', 'Earl Gray',
        'Candied Bacon', 'Dulce De Leche', 'Rocky Road', 'Maple Brown Sugar', 'Matcha', 'Mint Chip',
        'Wildberry', 'Double Fudge Chunk'],
    'SORBET': ['Raspberry', 'Blood Orange', 'Lychee', 'Lemon', 'Watermelon'],
    'BEVERAGE': ['Iced Coffee', 'Tea', 'Espresso']}
NUM_ORDERS = 10000

def get_quantity():
    return random.randint(1, 3)

def get_price():
    return random.randrange(1, 9, 1) / 2

def get_product():
    return random.choice(products).copy()

def adjust_line(row):
    if random.random() < 0.001:
        if random.random() > 0.5:
            row['line_total'] += 1
        else:
            row['line_total'] -= 1
    elif random.random() < 0.01:
        row['line_total'] = -row['line_total']
        row['price'] = -row['price']
    elif random.random() < 0.05:
        row['name'] = np.nan
    else:
        pass
    return row

if __name__ == '__main__':
    products = []

    for category, name_list in product_names.items():
        for name in name_list:
            product = {
                'name': '"{}" {}'.format(category, name),
                'price': get_price()}
            products.append(product)

    order_id = 10000
    date = datetime(2018, 1, 1, 11, 30)

    sales = []
    for i in range(NUM_ORDERS):
        for j in range(random.randint(1, 5)):
            line = get_product()
            line['quantity'] = get_quantity()
            line['order_id'] = order_id
            line['ordered_at'] = date
            sales.append(line)

        delta = timedelta(
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59))
        date += delta
        order_id += 1

    sales = pd.DataFrame(sales).set_index('order_id').sort_index()
    sales['line_total'] = sales['price'] * sales['quantity']

    # Mess with the totals so they don't add up
    sales = sales.apply(adjust_line, axis=1)

    # Cast the money columns to strings with $ in front
    for money_col in ['price', 'line_total']:
        sales[money_col] = sales[money_col].apply(lambda x: '${:.2f}'.format(x))

    # Create some duplicate records
    sales = pd.concat([sales, sales.sample(int(NUM_ORDERS * 0.01))])

    sales.to_csv('sales.csv')
