# necessary Imports
from logging import exception
from flask import Flask, request, session
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import models
from base import Session

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app, 
    version='1.0', 
    title='Test',
    description='My test Flask',
)

quote = api.model('Quote', models.quote_serializer)
user = api.model('User', models.user_serializer)

session = Session()

ns = api.namespace('quotes', description='quotes operations')

@ns.route('/')
class QuoteList(Resource):
    @ns.doc('list_quotes')
    @ns.marshal_list_with(quote)
    def get(self):
        quotes = session.query(models.Quote).all()
        return [quote for quote in quotes]
    
    @ns.doc('create_quote')
    @ns.expect(quote)
    def post(self):
        try:
            session.add(models.Quote(**request.get_json()))
            session.commit()
        except:
            print(exception)
            session.rollback()
            return '', 500
        return '', 201

@ns.route('/<int:id>')
@ns.response(404, 'Quote not found')
@ns.param('id', 'The quote identifier')
class Quote(Resource):
    '''Show a single quote item and lets you delete them'''
    @ns.doc('get_quote')
    @ns.marshal_with(quote)
    def get(self, id):
        '''Fetch a given resource'''
        return session.query(models.Quote)\
                        .filter_by(quote_id=id)\
                        .first()

    @ns.doc('delete_quote')
    @ns.response(204, 'Quote deleted')
    def delete(self, id):
        '''Delete a quote given its identifier'''
        try:
            session.query(models.Quote)\
                    .filter_by(quote_id=id)\
                    .delete()
        except:
            session.rollback()
            return '', 500
        return '', 204

    @ns.expect(quote)
    # @ns.marshal_with(quote)
    def put(self, id):
        '''Update a quote given its identifier'''
        try:
            session.query(models.Quote)\
                    .filter_by(quote_id=id)\
                    .update(request.get_json())
            session.commit()
        except:
            session.rollback()
            return '', 500
        return '', 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
