
from flask_login.utils import login_required
from flask_restful import Resource
from flask import Response, request, jsonify, redirect, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect
from .models import Coin, Account, User, Transaction

class Home(Resource):
    def get(self):
        if current_user.is_authenticated:
            return 'bienvenido ' + current_user.email
        else:        
            return 'no logueado'

class Redirect(Resource):
    def get(self):
        return redirect('/')


#--Auth resources--

class SignupApi(Resource):
    def post(self):        
        body = request.get_json()
        user = User(**body)
        if User.objects(email=user.email):
            return 'el email ya se encuentra en uso'
        else:
            user.hash_password()
    #a los fines de test, al crear el usuario se crea la cuenta en peso argentino con saldo inicial            
            user.save()                     
            account = Account()
            coin = Coin.objects.get(name="peso argentino")
            account.user = user
            account.coin = coin    
            account.balance = 1000
            account.save()
            user.accounts.append(account)
            user.save()        
            userId = user.id
            return {'userId': str(userId)}, 200

class LoginApi(Resource):
    def post(self):
            body = request.get_json()        
            user = User(**body)
            if not user == None:       
                try:        
                    result = User.objects.get(email = user.email)
                except:
                    return 'usuario y/o contraseña incorrectos'
                if not result.check_password(user.password):
                    return 'usuario y/o contraseña incorrectos'        
                else: 
                    login_user(result)            
                    return current_user.get(id)

class LogoutApi(Resource):
    def get(self):        
        logout_user()
        return 'logged out'            

#---coin resources---
class CoinApi(Resource):
    #get a coins
    def get(self, id):
        coin = Coin.objects(id=id)
        return jsonify(coin)

    #create a coin
    @login_required
    def post(self):
        body = request.get_json()
        coin =  Coin(**body)        
        if Coin.objects(name = coin.name):
            return 'el nombre de la moneda ya se encuentra en uso'
        elif Coin.objects(currency = coin.currency):
            return 'la sigla ya se encuentra en uso'
        else:
                coin.save()
                id = coin.id
                return {'id': str(id)}, 200
      
class CoinsApi(Resource):
    #get all coins
    def get(self):    
        coins = Coin.objects()
        return jsonify(coins)

#--User Resources--

class UsersApi(Resource):
        def get(self):
            users = User.objects.account()
            return jsonify(users)

class UserApi(Resource):
        def get(self, id):
            user = User.objects(id=id)   
            return  jsonify(user)

#--Account Resources--

class AccountApi(Resource):
    def get(self, id):
        account = Account.objects(id=id)
        return jsonify(account)

class AccountsApi(Resource):
    def get(self):
        accounts = Account.objects.coin(name='peso argentino')
        return jsonify(accounts)
        

#--Transaction Resources--

class TransactionApi(Resource):
    def get(self, id):
        transaction = Transaction.objects(id=id)
        return jsonify(transaction)

class TransactionsApi(Resource):
    #get all transactions
    def get(self):
        transactions = Transaction.objects()
        return jsonify(transactions)
            
    #create transaction    
    def post(self):
        body = request.get_json()
        transaction = Transaction()        
        fromAccount = Account.objects.get(id = body['fromAccount'])

        #el usuario debe estar logueado y no puede hacer transferencias desde una cuenta diferente a la suya
        if not fromAccount.user == current_user:
            return 'operacion no permitida' 

        #el usuario no puede transferir a una cuenta inexistente o de otra moneda
        try:
            toAccount = Account.objects.get(id = body['toAccount'], coin = fromAccount.coin)
        except:
            return "la cuenta de destino es incorrecta o inexistente"
        #el usuario no puede transferirse a si mismo
        if fromAccount == toAccount:
            return 'la cuenta de destino es incorrecta o inexistente'
        
        amount = body['amount']
        
        if amount <= 0:
            return 'El monto a transferir no puede ser cero'
        
        #el usuario no puede transferir mas de lo que tiene en su cuenta.
        if amount > fromAccount.balance:
            return 'el importe ingresado supera el saldo de la cuenta'        
        else:
            transaction.fromAccount = fromAccount
            transaction.toAccount = toAccount
            transaction.amount = amount
            toAccount.balance += amount
            toAccount.save() 
            fromAccount.balance -= amount
            fromAccount.save()                     
            transaction.save()
            transactionId = transaction.id
            return {'transactionId': str(transactionId)}, 200