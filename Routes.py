import datetime
from decimal import Decimal
from flask import Flask,render_template,request,redirect, session,url_for
from flask_sqlalchemy import SQLAlchemy
from Models import db,User,Purchase

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HomeTrack.db'
db.init_app(app)
date_format='%D/%M/%Y'
# יצירת טבלת הנתונים בפעם הראשונה
with app.app_context():
    db.create_all()

# הגדרת ניתוב לפונקציה
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username=request.form.get('username')
    email = request.form.get('email')
    existing_email=User.query.filter_by(email=email).first()
    if existing_email:
         return "Existing email address"
    password = request.form.get('password')
    confirm=request.form.get('confirm')
    if confirm != password:
        return "Confirm filed"
    user=User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('profile',id=user.id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email=request.form.get('email')
    user=User.query.filter_by(email=email).first()
    if not user:
        return render_template('login.html',message="User not existing")
    password = request.form.get('password')
    if password!=user.password:
        return render_template('login.html',message="password incorrect")
    return redirect(url_for('profile',id=user.id))

@app.route('/profile/<int:id>')
def profile(id):
    purchases=Purchase.query.filter_by(user_id=id).all()
    user=User.query.get(id)
    return render_template('profile.html',purchases=purchases,user=user)


@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    purchase = Purchase.query.get_or_404(id)
    db.session.delete(purchase)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/add_purchase/<int:id>',methods=['GET','POST'])
def add_purchase(id):
    if request.method == 'GET':
        purchases_from_db=Purchase.query.filter_by().all()
        return render_template('add_purchase.html',purchases=purchases_from_db)
    product_name=request.form['product_name']
    quantity = request.form['quantity']
    price = request.form['price']
    category = request.form['category']
    date_str = request.form['date']
    date_obj = datetime.strptime(date_str,date_format)
    # רכישה חדשה
    new_purchase = Purchase(product_name=product_name,quantity=quantity,price=price,category=category,date=date_obj)
    db.session.add(new_purchase)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)  # הרצת האפליקציה

