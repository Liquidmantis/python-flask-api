from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item { name: item_name, price: item_price }
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/items
@app.route('/store/<string:name>/items')
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({'items': store["items"]})
    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item/<string:item>')
def get_item_in_store(name, item):
    for store in stores:
        if store["name"] == name:
            for store_item in store["items"]:
                if store_item["name"] == item:
                    return jsonify({'item': store_item})
            return jsonify({'message': 'item not found'})
    return jsonify({'message': 'store not found'})

@app.route('/')
def home():
    return render_template('index.html') 

app.run(port=5000)
