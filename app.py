# necessary Imports
from flask import Flask, jsonify, request
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix


# application & documentation setup
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Swagger enabled Quotes API',description='A simple Quotes API')

# namespace definition
ns = api.namespace('quotes', description='Quote CRUD operations')

# model definition - would be automatically displayed as part of API documentation
quote = api.model('quote', {
    'id': fields.Integer(readonly=True, description="Quote's unique identifier"),
    'quote_desc': fields.String(required=True, description="Quote"),
    'quote_type': fields.String(required=True, description="quote's type"),
    'author': fields.String(required=True, description="quote's author")
})

# Quote class containing CRUD methods
class QuoteDAO(object):
    def __init__(self):
        self.counter = 0
        self.quotes = []

    def get(self, id):
        for q in self.quotes:
            if q['id'] == id:
                return q
        api.abort(404, "Quote {} doesn't exist".format(id))

    def create(self, data):
        q = data
        q['id'] = self.counter = self.counter + 1
        self.quotes.append(q)
        return q

    def update(self, id, data):
        q = self.get(id)
        q.update(data)
        return q

    def delete(self, id):
        q = self.get(id)
        self.quotes.remove(q)


# Initialize DAO & create sample quotes
DAO = QuoteDAO()
DAO.create({'quote_desc':'It always seem impossible until it is done.', 'quote_type': 'Motivation', 'author': 'Nelson Mandela'})
DAO.create({'quote_desc':'With the new day comes new strength and new thoughts.', 'quote_type': 'Motivation', 'author': 'Eleanor Roosevelt'})
DAO.create({'quote_desc':'The secret of getting ahead is getting started.', 'quote_type': 'Motivation', 'author': 'Mark Twain'})


# API Endpoints for listing and creating new quotes
@ns.route('/')
class QuoteList(Resource):
    '''Shows a list of all quotes, and lets you POST to add new quotes'''
    @ns.doc('list_quotes')
    @ns.marshal_list_with(quote)
    def get(self):
        '''List all quotess'''
        return DAO.quotes

    @ns.doc('create_quote')
    @ns.expect(quote)
    @ns.marshal_with(quote, code=201)
    def post(self):
        '''Create a new quote'''
        return DAO.create(api.payload), 201



# API Endpoints for rest of CRUD operations
@ns.route('/<int:id>')
@ns.response(404, 'Quote not found')
@ns.param('id', 'The quote identifier')
class Quote(Resource):
    '''Show a single quote item and lets you delete them'''
    @ns.doc('get_quote')
    @ns.marshal_with(quote)
    def get(self, id):
        '''Fetch a quote given its identifier'''
        return DAO.get(id)

    @ns.doc('delete_quote')
    @ns.response(204, 'Quote deleted')
    def delete(self, id):
        '''Delete a quote given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(quote)
    @ns.marshal_with(quote)
    def put(self, id):
        '''Update a quote given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
