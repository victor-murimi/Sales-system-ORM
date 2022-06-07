from flask import Flask, request, render_template, redirect, flash, session
from sqlalchemy import extract,func
from flask_login import LoginManager , login_user, login_required,logout_user,current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import true
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from flask.helpers import url_for


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:0742978312@localhost:5432/ORM'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = true
app.config['SECRET_KEY'] = 'Super_secret_key'

login_manager =LoginManager(app)
db=SQLAlchemy(app)
def init_app(app):  
    db.init_app(app)

from models.products import Products
from models.sales import Sales
from models.users import Users
from models.stock import Stocks


@app.before_first_request
def create_table():
 db.create_all()
 db.session.commit()
 
 login_manager=LoginManager()
 login_manager.login_view='login'
 login_manager.init_app(app)

 @login_manager.user_loader
 def load_user(user_id):
     return Users.query.get(int(user_id))


 
@app.route('/')
def index():
    #return home
    return render_template("index.html")


@app.route('/signup')  
def signup():

    return render_template('signup.html')

            

@app.route("/signup", methods=["POST"])
def signup_post():

        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')

        user=Users.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('signup'))
       

        new_user=Users(email=email,username=username,password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))


@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))

@app.route("/login", methods=['POST'] )
def login_post():

     if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
 
        user=Users.query.filter_by(email=email).first()
        
        if not user or not  check_password_hash(user.password,password):
            flash('Please check your login details and try again')
            return redirect(url_for('login'))

        print("user has been logged in")
        login_user(user)
        #if the above check passes, we know the user has the credentials
        return redirect(url_for('index'))
    
     return render_template('login.html')
    
    

@app.route("/inventory", methods=["POST", "GET"])
@login_required
def inventory():    
    if request.method == "POST":
        name=request.form['name']
        BP=request.form['BP']
        SP=request.form['SP']
        quantity=request.form['quantity']

        new_product=Products(name=name,buying_price=BP,Selling_price=SP,product_quantity=quantity)
        db.session.add(new_product)
        db.session.commit() 

        # id=Products.query.filter_by(product_name=product_name).all()
        # pid=id.id
        # newstock=Stocks(pid=pid,stock_quantity=product_quantity)
        # db.session.add(newstock)
        # db.session.commit()
        return redirect(url_for('inventory'))
    
    all_products=Products.query.all()
    return render_template('inventory.html',y=all_products)

    
@app.route("/sales", methods=["POST", "GET"])
@login_required
def sales_post():
    # if "user" in session:
    #     user=session["user"]
    if request.method == "POST":
        
        product_id=request.form["product_id"]
        stock_quantity=request.form["quantity"]
        
        g=int(stock_quantity)
        st=Products.query.filter_by(id=product_id).all()
        y=st[0].product_quantity

        rem=y-g
        
        if rem < 0:
            flash('Quantity ordered is higher than stock available')
            return redirect(url_for("inventory"))
        else:    
            print(rem)
            updated=Products.query.filter_by(id=product_id).update({Products.product_quantity:rem})
            db.session.commit()
            new_sale=Sales(product_id=product_id,quantity=stock_quantity)
            db.session.add(new_sale)
            db.session.commit()
            return redirect("/sales")
        
    else:
        sale=Sales.query.all()
        # print(sale)
        # lst4=sale
        # print(sale[0].product.id)
        # sale=Sales.query.filter_by(product.__name__).all()
        # print(sale)

        return render_template("sales.html", x=sale)
    # else:
    #     return redirect(url_for("login"))

@app.route("/edit",methods=["POST","GET"])
def edit():
    if request.method=="POST":
        id=request.form["Item-id"]
        name=request.form["name"]
        bp=request.form["buyingprice"]
        sp=request.form["sellingprice"]
        stock=Stocks.query.filter_by(id=id).all()
        sbp=stock[0].buying_price
        ssp=stock[0].selling_price

        bp=int(bp)
        sp=int(sp)
        sbp=bp-sbp
        ssp=sp-ssp
        updated=Products.query.filter_by(id=id).update({Products.name:name,Products.buying_price:bp,Products.Selling_price:sp})
        db.session.commit()
    

    return redirect("/products")


@app.route("/stock")
@login_required
def stock():
    if request.method=="POST":
        pid= request.form["item-id"]
        stock_added=request.form["stock"]
        created_at='NOW()'


        
        # stock_added=Stocks.query.filter_by(pid=pid).all()
        # sst=Stocks[0].stock_quanity
        # s=int(stock_added)
        # newstock=sst+s
        # update=Stocks.query.filter_by(pid=pid).update({Stocks.stock_quantity:newstock})
        # db.session.add
        # db.session.commit

        
  
        return redirect("/stock")
    else:

        all_products=Stocks.query.all()
        list1=all_products

        return render_template("stock.html",list1=list1)    


@app.route("/dashboard")
@login_required
def dashboard():
   
#pie-chart for the top five products
    prod=[]
    data5=[]
    top5 = Sales.query.with_entities(Products.name, func.sum(Sales.quantity)).join(Products).group_by(Products.name ).order_by(func.sum(Sales.quantity)).limit(5) 
    
    for i in top5:
        prod.append(i[0])
        data5.append(int(i[1]))
    print(data5)

#bar-chart for the sales per month
    spm = Sales.query.with_entities(func.sum(Sales.quantity * Products.Selling_price),extract('month',Sales.created_at)).join(Products).group_by(extract('month',Sales.created_at))
    monthspm=[]
    dataspm=[]
    for x in spm:
        monthspm.append(x[1])
        dataspm.append(int(x[0]))
    print("dataspm",dataspm)


    # sbp = Sales.query.with_entities(func.sum(Sales.quantity * Products.Selling_price),Products.name.join(Products).group_by(Products.name).order)
    
    return render_template("dashboard.html", prod=prod,data5=data5,monthspm=monthspm,dataspm=dataspm)

if __name__ == "__main__":
    app.run(debug=True)
