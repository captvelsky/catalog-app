from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER_NAME = "postgres"
DB_PASSWORD = "123456"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Integer)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


def addProduct(product):
    db.session.add(product)
    db.session.commit()


def getProduct(id):
    product = Product.query.filter_by(id=id).first()
    return product


def getAllProducts():
    products = Product.query.all()
    return {
        'products': products,
        'count': len(products)
    }


def updateProduct(id, product):
    old = Product.query.filter_by(id=id).first()
    old.name = product.name
    old.description = product.description
    old.price = product.price
    db.session.commit()


def deleteProduct(id):
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()


@app.route('/')
def homePage():
    data = getAllProducts()
    return render_template('home.html', data=data)


@app.route('/tambah', methods=["GET", "POST"])
def tambahKatalogPage():
    if request.form:
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        product = Product(name, description, price)
        addProduct(product)
        return redirect('/')
    return render_template('tambah.html')


@app.route('/hapus/<id>')
def hapusKatalog(id):
    deleteProduct(id)
    return redirect('/')


@app.route('/edit/<id>', methods=["GET", "POST"])
def editKatalog(id):
    if request.form:
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        new = Product(name, description, price)
        updateProduct(id, new)
        return redirect('/')
    product = getProduct(id)
    return render_template('edit.html', data=product)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
