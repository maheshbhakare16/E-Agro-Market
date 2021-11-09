import mysql.connector
from flask import Flask, render_template,request,redirect,flash,session
import json
import os
from werkzeug.utils import secure_filename
import random
from flask_mail import Mail
from datetime import datetime


#    ------------------------ OPENED CONFIG.JSON FILE -------------------
with open('config/config.json', 'r') as c:
    param=json.load(c)['params']
    
    
app=Flask(__name__)

app.config['upload_folder']=param['upload_location']


# ----------------------- mail server configuration ---------------------------------

app.config.update(
MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = param['gmail-user'],
    MAIL_PASSWORD=  param['gmail-password']
)
mail = Mail(app)

# ------------------------- database server configuration ------------------------------------

connection = mysql.connector.connect(host='localhost', database='eagromarket',username='mahesh', password='mahesh12@')
cursor = connection.cursor(dictionary = True)


# home
@app.route('/')
def home():
    return render_template('index.html')



# ----------------------------------- farmer_signup ---------------------------------------------


@app.route('/farmer_signup', methods=['GET', 'POST'])
def farmer_signup():
    if(request.method=='POST'):
        fname=request.form.get('first_name')
        lname=request.form.get('last_name')
        uname=request.form.get('username')
        address=request.form.get('address')
        email=request.form.get('email')
        dob=datetime.strptime(request.form.get('DOB'),'%Y-%m-%d').date()
        gender=request.form.get('gender')
        password=request.form.get('Password')
        conf_password = request.form.get('Confirm_Password')
        print(dob)
        if(password==conf_password):
            try:
                query = f"insert into farmer_lc (fname,lname,uname,address,email,dob,gender,password) values('{fname}','{lname}','{uname}','{address}','{email}','{dob}','{gender}','{password}');"
                cursor.execute(query)
                connection.commit()
            except Exception as e:
                print(e)
                flash("username or Email ID already taken please enter other username", "warning")
                return render_template('farmer_signup.html', head=param['head'])
            else:
                flash("You have successfully created account . Please, Go to Login page to Login into your account","success")

                return render_template('farmer_signup.html', head=param['head1'])
        else:
            flash("You have entered wrong confirmation password...!", "danger")
            return render_template('farmer_signup.html', head=param['head2'] )


    return render_template('farmer_signup.html')



# ----------------------- farmer_login ---------------------------------------



@app.route('/farmer_login', methods=['GET', 'POST'])
def farmer_login():
    if 'user' in session:
        return redirect('/farmer_dashboard')
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        try:
            query = "select count(uname) as count from farmer_lc where uname = '"+username+"' and password = '"+password+"';"
            cursor.execute(query)
            login = cursor.fetchone()            
            if (login['count'] == 1 ):
                    session['user'] = username
                    return redirect('/farmer_dashboard')
            else:
                flash("wrong Username or Password, Please enter proper Detail....!", "danger")
                return render_template('farmer_login.html', head=param['head2'])

        except:
            flash("Something went Wrong..........!\n    Please try again after some time ", "danger")
            return render_template('farmer_login.html', head=param['head2'])

    return render_template('farmer_login.html')




# ------------------------- Farmer Dashboard ---------------------------------------



@app.route('/farmer_dashboard')
def dashboard_farmer():
    for f in os.listdir(param['upload_location']):
        os.remove(os.path.join(param['upload_location'], f))
    if 'user' in session:
        try:
            query = "select * from product_details where uname = '"+session['user']+"';"
            cursor.execute(query)
            results = cursor.fetchall()
            return render_template('dashboard.html', results=results, username=session['user'])
        except Exception as e:
            print(e)
    return render_template('dashboard.html', results=results, username=user_name)



# ------------------------ Farmer -add new product- ----------------------------------------

@app.route('/farmer_dashboard/add_new_product', methods=['GET','POST'])
def add_new_product():
    if 'user' in session:
        if request.method=='POST':
            username = request.form.get('username')
            productname = request.form.get('productname')
            quantity = request.form.get('quantity')
            contact_no = request.form.get('contact_no')
            price = request.form.get('price')
            fullname = request.form.get('fullname')
            f_bin = request.files['photo'].read()
            try:
                query = "insert into product_details (product_name,quantity,contact_no,price,full_name,upload_date,photo,uname) values(%s,%s,%s,%s,%s,%s,%s,%s);"
                values=(productname,quantity,contact_no,price,fullname,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),f_bin,username)
                cursor.execute(query,values)
                connection.commit()
                return redirect('/farmer_dashboard')
            except Exception as e:
                print(e)
    return render_template('add_new_product.html', u_name=session['user'])



# ---------------------------------- Delete Product ------------------------------

@app.route('/farmer_dashboard/delete/<string:upload_date>')
def delete(upload_date):
    if 'user' in session:
        u_name=session['user']
        try:
            query = "delete from product_details where upload_date = '"+upload_date+"' ;"
            cursor.execute(query)
            connection.commit()
            return redirect('/farmer_dashboard')
        except Exception as e:
            print(e)



# -------------------------------- farmer Product Image View --------------------------


def convertBinarytoFile(filename,binary_data):
    with open(filename, 'wb') as file:
        return file.write(binary_data)



@app.route('/farmer_dashboard/view/<string:upload_date>')
def view_farmer_image(upload_date):
    if 'user' in session:
        user_name = session['user']
        try:
            query = f"select photo from product_details where upload_date = '{upload_date}';"
            cursor.execute(query)
            results = cursor.fetchone()
            #f_name = param['upload_location']+user_name+'.jpg'
            file = convertBinarytoFile(param['upload_location']+user_name+'.jpg',results['photo'])
            return render_template('image_farmer.html', result = user_name+'.jpg',username=user_name)
        except Exception as e:
            print(e)
            flash("May be product has been deleted...!", "warning")
            return redirect('/farmer_dashboard')
    return render_template('farmer_dashboard.html', result=results,username=user_name)

    


# ---------------------------------- Farmer logout ----------------------------------------


@app.route('/logout')
def logout_farmer():
    session.pop('user')
    return redirect('/farmer_login')





# ---------------------------------------- merchant_signup ----------------------------------------


@app.route('/merchant_signup', methods=['GET', 'POST'])
def merchant_signup():


    if (request.method == 'POST'):
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        uname = request.form.get('username')
        address = request.form.get('address')
        email = request.form.get('email')
        dob=datetime.strptime(request.form.get('DOB'),'%Y-%m-%d').date()
        gender = request.form.get('gender')
        password = request.form.get('Password')
        conf_password = request.form.get('Confirm_Password')
        gstn=request.form.get('gstn')

        if (password == conf_password):
            try:
                query = f"insert into merchant_lc (fname,lname,uname,address,email,dob,gender,gstn,password) values('{fname}','{lname}','{uname}','{address}','{email}','{dob}','{gender}','{gstn}','{password}');"
                cursor.execute(query)
                connection.commit()
            except Exception as e:
                print(e)
                flash("username or Email ID already taken please enter other username", "warning")
                return render_template('merchant_signup.html',head= param['head'])
            else:
                flash("you have successfully created account . please, goto login page to login into your account","success")
                return render_template('merchant_signup.html', head=param['head1'])
        else:
            flash("you have entered wrong confirmation password...!", "danger")
            return render_template('merchant_signup.html', head=param['head2'])

    return render_template('/merchant_signup.html')




# ---------------------------------------------------- merchant_login -----------------------------------


@app.route('/merchant_login', methods=['GET', 'POST'])
def merchant_login():
    if 'user_merchant' in session:
        return redirect('/merchant_dashboard')
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        try:
            query = "select count(uname) as count from merchant_lc where uname = '"+username+"' and password = '"+password+"';"
            cursor.execute(query)
            login = cursor.fetchone()            
            if (login['count'] == 1 ):
                    session['user_merchant'] = username
                    return redirect('/merchant_dashboard')
            else:
                flash("wrong password, Please enter proper password", "danger")
                return render_template('merchant_login.html', head=param['head2'])
        except:
            flash("user not found please signup", "danger")
            return render_template('merchant_login.html', head=param['head2'])

    return render_template('merchant_login.html')




# ------------------------------------ merchant Dashboard -----------------------------------------


@app.route('/merchant_dashboard', methods=['GET', 'POST'])
def dashboard_merchant():
    for f in os.listdir(param['upload_location']):
        os.remove(os.path.join(param['upload_location'], f))
    user_name = session['user_merchant']
    if request.method=='POST':
        search=request.form.get('search')
        try:
            query = f"select * from product_details where product_name = '{search}';"
            cursor.execute(query);
            results = cursor.fetchall();
            return render_template('dashboard_merchant.html', results=results, username=user_name)
        except Exception as e:
            print(e)
    return render_template('dashboard_merchant.html', username=user_name)



# ---------------------------------- Merchant Product image View -----------------------------


@app.route('/merchant_dashboard/view/<string:upload_date>')
def view_merchant_image(upload_date):
    if 'user_merchant' in session:
        user_name = session['user_merchant']
        try:
            query = f"select photo from product_details where upload_date = '{upload_date}';"
            cursor.execute(query);
            results = cursor.fetchone();
            file = convertBinarytoFile(param['upload_location']+user_name+'.jpg',results['photo'])
            return render_template('image.html', result = user_name+'.jpg',username=user_name)
        except:
            flash("May be product has been deleted...!", "warning")
            return render_template('dashboard_merchant.html', username=user_name,head=param['head3'])

# ------------------------------ Merchant LogOut -----------------------------------------


@app.route('/logout_merchant')
def logout_merchant():
    session.pop('user_merchant')
    return redirect('/merchant_login')




# ------------------------------------------------ About Us ---------------------------------------------


@app.route('/about')
def about():
    return render_template('about.html')


#contact us
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        subject=request.form.get('subject')
        msg=request.form.get('msg')
        mail.send_message( 'name: ' + name + ' Email ID:' + email +  ' Topic :' + subject,sender=msg,recipients=[param['gmail-user']],body=msg )
        flash("you have successfully send the message. We will replay you under 24hrs.",
              "success")
        return render_template('contact_us.html', head=param['head1'])

    return render_template('contact_us.html')


# --------------------------------- forgot_password --------------------------------------------


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method=='POST':
        username=request.form.get('username')
        try:
            query = f"select * from signup where uname = '{username}';"
            cursor.execute(query)
            res = cursor.fetchone()
            if(res['uname'] == username):
                session['username'] = res['uname']
                otp=random.randrange(100000,999999)
                session['otp'] = str(otp)
                msg="your OTP is" + str(otp)
                mail.send_message('verification otp ....!' ,sender=param['gmail-user'],recipients=[res['email']],body=msg)
                return redirect('/otp_verification')
        except Exception as e:
            print(e)
            flash("username not found.. please create account or Enter proper username...","danger")
            return render_template('forgot_password.html', head=param['head2'])
    return render_template('forgot_password.html')



# ------------------------------- otp_verify ------------------------------------------------------


@app.route('/otp_verification', methods=['GET','POST'])
def otp_verification():
    otp=session.get('otp')
    print(otp)
    if request.method=='POST':
        otp_page=request.form.get('otp')
        print(otp_page)
        if otp_page==otp:
            return redirect('/new_password')
        else:
            flash("wrong otp please enter again...", "warning")
            return render_template('otp_verify.html', head=param['head2'])

    flash("OTP has been send successfully, Check your mailbox and enter otp in below filed...", "success")
    return render_template('otp_verify.html', head=param['head1'])


# ------------------------------------------- new_password -------------------------------------------


@app.route('/new_password', methods=['GET','POST'])
def new_password():
    if request.method=='POST':
        password=request.form.get('password')
        conf_password=request.form.get('conf_password')
        if password==conf_password:
            query = f"update signup set password = '{password}' where uname = '{session['uername']}';"
            cursor.execute(query)
            cursor.commit()
            flash("New password set Successfully Goto login page to login your account..Thank you","success")
            return render_template('enter_new_password.html', head=param['head1'])
        else:
            flash("your password and confirmation passwords are not same... Please Enter Same password in both the Fields..", "warning")
            return render_template('enter_new_password.html', head=param['head2'])
    flash("OTP verified successfully", "success")
    return render_template('enter_new_password.html', head=param['head1'])





# -------------------------------------- forgot_username --------------------------------------------


@app.route('/username_forgot', methods=['GET', 'POST'])
def forgot_username():
    if request.method=='POST':
        email=request.form.get('email')
        try:
            query = f"select uname, email from signup where email = '{email}';"
            cursor.execute(query)
            res=cursor.fetchone()
            if res['email']==email:
                msg = "your username of E-AGRO-MARKET login is :   " + str(res['uname'])
                mail.send_message('E-AGRO-MARKET', sender=param['gmail-user'], recipients=[res['email']], body=msg)
                flash("Username has been send successfully goto check your mailbox and login.... Thank you", "success")
                return render_template('username_forgot.html', head=param['head1'])
        except:
            flash("wrong Email ID entered....Please enter proper Email ID..","danger")
            return render_template('username_forgot.html', head=param['head2'])
    return render_template('username_forgot.html')



# ---------------------------------- main_function ---------------------------------------------------


if __name__ == '__main__':
    app.secret_key = 'mykey'
    app.run()
