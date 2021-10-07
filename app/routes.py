from werkzeug.utils import redirect
from app import api
from .resources import *


api.add_resource(Home, '/')
api.add_resource(Redirect, '/redirect')

api.add_resource(CoinsApi, '/api/coins')
api.add_resource(CoinApi, '/api/coin/<id>','/api/coin')

api.add_resource(UsersApi, '/api/users')
api.add_resource(UserApi, '/api/user/<id>')

api.add_resource(TransactionsApi, '/api/transactions')
api.add_resource(TransactionApi, '/api/transactions/<id>')

api.add_resource(AccountApi, '/api/account/<id>')
api.add_resource(AccountsApi, '/api/accounts')

api.add_resource(SignupApi, '/api/signup')
api.add_resource(LoginApi, '/api/login')
api.add_resource(LogoutApi, '/api/logout')

# api.add_resource(MyTransactions, '/api/mytransactions')



