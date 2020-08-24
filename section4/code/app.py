from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'no-telling!'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

def get_item(name):
    return next(filter(lambda x: x['name'] == name, items), None)

class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {'items': items}

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    # @jwt_required()
    def get(self, name):
        item = get_item(name)
        return {'item': item}, 200 if item else 404

    # @jwt_required()
    def post(self, name):
        if get_item(name):
            return {'message': "an item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    # @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = get_item(name)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        return item

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=5000, debug=True)


