from flask import Flask, render_template, request, redirect,  url_for
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout #подключение системы оплаты от fondy. Перед этим прописать pip install cloudipsp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tour.db' #config - настройка
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #настройка, позволяющая изменять БД (лучше прописать, чтобы не вылазили ошибки)
db = SQLAlchemy(app) #создаем объект db на основе sqlalchemy. (app) - принадлежит к приложение app
#python
#from app import db
#db.create_all() - создает саму БД и добавляет все таблички. Выполнять эту команду при создании каждой новой таблички

class Item(db.Model): #создание таблички для БД
    id = db.Column(db.Integer, primary_key=True) #Primary_key - автоматическая простановка id с увеличением на 1 (первичный ключ)
    title = db.Column(db.String(100), nullable=False) #nullable=false - нельзя оставить пустое поле
    price = db.Column(db.Integer, nullable=False) #nullable=false - нельзя оставить пустое поле
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)
    



@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all() #query - sql запрос. order_by(Item.price) - сортировка по
    return render_template('index.html', data=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id) #получаем цену товара. get - запрос одной позиции из бд 


    api = Api(merchant_id=1396424,     #стандартный код из https://github.com/cloudipsp/python-sdk. id - id компании
            secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + '00' #str() +'00' - добавление копеек.
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/create', methods=['POST','GET']) # methods=['POST'] - указываем для возможности получать данные методом post и get
def create():
    if request.method == 'POST': #с помощью request можно брать данные, переданные методом post
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        

        item = Item(title=title, price=price, text=text)
        def __repr__(self): #функция для вывода названия элемента в html структуре
            return {self.title}
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Получилась ошибка'
    else:
        return render_template('create.html')

if __name__ == '__main__': #если файл запускается как основной (main)
    app.run(debug=True) # вызов функции run. 