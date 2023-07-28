# Agar same email id register page mai daaloge toh Integrity error show krga
from flask import Flask,render_template, request, flash, redirect
# database bnane ke lye import kr rahe hai or pip install flask-sqlalchemy cmd m like hai
from flask_sqlalchemy import SQLAlchemy
# configuring ur application mai se code copy kye hai flask in login pe jaake google pe ye 2nd step
from flask_login import LoginManager, login_user, UserMixin, logout_user
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/bigda/OneDrive/Desktop/Flask/instance/mydb.db'
# ye secret key daal rahe login.html ka jhamela khtam krne ke baad,jab hmlog chah rhe the ki register singin krne ke baad jo message dkhye vo login page mai dkhye tab error show kr rha tha ki secret key daalo islye daale hai
# The secret key is needed to keep the client-side sessions secure.
app.config['SECRET_KEY'] = 'thisissecret' 
db = SQLAlchemy(app)
# ye object create kye login ka ye 3rd step
login_manager = LoginManager()
login_manager.init_app(app)
app.app_context().push()

# TO CREATE A MODEL OR TABLE
# Nullable ka mtlab ki hum khali ny chod sakte fill krna he padga
# jo v tum bnaya hai table usko database mai store krane ke lye command lkhna pdga
#  from app import db
#  db.create_all()
# data ko database m store krwaarahe h
#  from app import User
# data ko fetch kra rahe h,query se hota hai ki model mai jo v data hai vo retrieve ho jyga database m
#  user=User.query.all()
#  user
# cd mai ek data bnye jaise ki ye= user=User(username='kanhaiya kumar',email='daddy347@gmail',fname='kanhaiya',lname='yadav',password='1234') dkhne ke lye ki ye databse m store ho rha h ki ny, toh dkhne se phle add krte hai aise = db.session.add(user) fir usko save krte hai aise= db.session.commit() fir data=User.query.all() fir  'data' lkhne ke baaad enter

# ye hmlog model create kr rhe h
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    username =db.Column(db.String(50), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    fname = db.Column(db.String(120), nullable = False)
    lname = db.Column(db.String(120),  nullable = False)
    password = db.Column(db.String(120), nullable = False)

    def __repr__(self):
       return f'<User {self.username}>'

# login wla system kaise kaam krga how it works ye ,load hoga kaise yahi sb 4th step
# ye userloader function hai
@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id)
     return User.query.get(int(user_id))


# to create url
# to return any text,template in home page
# / blank page mai tm kuch return kr rha h jaise ki home page
# @app.route("/")
# def home():
#     return("Home page")

@app.route("/")
def home():
    # blog table m jtna v blog hai database m unsabko home page pe display or return krw rhe h
    data=Blog.query.all()
    return render_template("index.html",data=data)


# main.hmtl ko link krdye hai routing or url se
@app.route("/main")
def main():
    return render_template("main.html")

# index.hmtl ko link krdye hai routing or url se
@app.route("/index")
def index():
    return render_template("index.html")


#to make a new route for login and registration pages
# /register ka mtlab local host m /register krne se register page khul jyga
# @app.route("/register")
# def register():
#     return("register page")

# register.html ko link krdye hai routing or url se
@app.route("/register",methods=['GET','POST'])
def register():
    # yha pe check kr rhe h ki data aya hai ki ny jo tum bhja hai method=post krke register.html mai or check kr rhe hai ki method konsa hai
    if request.method=='POST':
        # register.html name dye hai sbko ki name ke through wha se data ko fetch krke yha lynge .form.get('email) hai vo name dye hai email islye lkhe hai bracket ma email waise he sbka lkhe hai
        # register.html m jo value dalega jaise email ya kuch v jab signup krga toh waha se sab value fetch hoke yha jo niche lkhe hai save ho jyga
        # yha se un value ko fetch kr rhe h
     email = request.form.get('email')
     password = request.form.get('password')
     fname = request.form.get('fname')
     lname = request.form.get('lname')
     username = request.form.get('uname')
     #  print ko comment kye hai qki print krne se ye terminal mai data show krta hai jab tum sign krga
     #  print(email,password,fname,lname,username)
     # hmlog chahenge ki data mydb.db m save ho
     # user=User(username=username) mtlab phla user variable hai =ke baad wla User model ka name hai or tisra username model ke field ka name hai or =ke baad wla username jo hmlog data fetch kye hai jo request wla hai vo hai
     #  or yha se un value ko database m save kr rhe h
     user=User(username=username,email=email,fname=fname,lname=lname,password=password)
     # ab user ko add krnge database mai
     db.session.add(user)
     db.session.commit() 

     #  return 'Registered Successfully'
     
     #  user ko database m save krne ke baad ab message ko display krwa rhe
     #  google pe search krna flash message to ye syntax hai uska message ko display krane ke lye
     #  flash ko import krwye hai upar
     #   flash ka syntax= flash(message='user has been registered succcessfully',category='success')
     #  message: The message to display
     #  category: An Optional parameter, which can be set to “error,” “info,” or “warning.”
     #  hmlog chahte hai ki ye message jo hai vo login page pe show kre,toh islye flash ka code or bootstrap ka code login page pe paste kye hai jaise ki flash ka (flash with categories ka code) and bootstrap ka alerts ka code
     #  ye google pe search krna message flashing flask document uska code uthakar login.html ke body me paste kye hai
     #  ye jo niche message hai ye jyga login.html mai wha pe {{category}} and {{message}} ke andar show krga.
     flash('User has been Registered Succcessfully','success')

     #  agr hmara user successfully register krdta hai toh fir vo login page pe direct aajyga
     #  redirect is a technique used to send users from one URL to another.
     #  redirect ko import krwaye hai upar
     return redirect('/login')


    return render_template("register.html")

# @app.route("/login")
# def login():
#     return("login page")

# login.html ko link krdye hai routing or url se
# post ka mtlab login page m data ko fill krke bhj rhe hai fir uske baad request.form.get means catch kr rha data ko
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
       
        username = request.form.get('username')
        password = request.form.get('password')
        # yha pe field ke username mtlab jo tum daaloge login page mai or data base ke username mai match ho rha h ki ny check kr rhe h
        # Querying the user from the database
        user = User.query.filter_by(username=username).first()
        # yha pe check kr rhe hai ki password hmara agar database se  equal mtlab register krne ke baad hua toh login ho jyga ny toh  error hoga 
        # Checking if the user exists and if the password matches
        if user and password==user.password:
            login_user(user)
            return redirect('/')
        else:
            # ye hai message ka code flash('category','message') jo  hum logi.html pe lgye hai {{category}} and {{message}}
            flash('Invalid Credentials','danger')
            # return login pe islye krwa rhe h ki agar galat password ya username dalega toh login form pe he rhga
            return redirect('/login')
    return render_template("login.html")
    # upar lkhne ke baad hmlog login wla system bnane ke lye terminal m pip install flask-login lkhna pdga 1st step
    # fir uske baad upar import krynge jaise from flask_login import LoginManager or fir object create krnge

@app.route("/logout")
def logout():
    # iska mtlab jo user mra login hai jab hum logout pe click krnge toh user logout ho jyga or import krwye hai logout_user()
    logout_user()
    # or fir logout hone ke baad seedha hm home page pe return krwynge
    return redirect('/')



# yha pe hm blog ka model create kye hai
class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)  # unique
    title = db.Column(db.String(80),nullable=False)
    author = db.Column(db.String(50),nullable=False)
    content = db.Column(db.Text(), nullable=False )
    # datetime likh rhe h qki pta chlga ki vo post hum kab dale hai or datetime ko upar import v krwye hai
    pub_date= db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)
    # islye lkhe qki blog ka title ko return krwana hai jab hmlog database se fetch krnge tab
    def __repr__(self):
       return f'<Blog {self.title}>'
     #    [<Blog First blog>]
# ab iske baad hmlog ko database m create krna hai ye av app.py file m create kye hai database m create krne ke lye hame terminal m lkhna hai   
# >>> from app import db
# >>> db.create_all()
# >>> from app import Blog
# >>> blog=Blog(title='First blog',author='Lucky',content='This is my first blog')
# >>> db.session.add(blog)
# >>> db.session.commit()
# ye line m dekh rahe h ki hmara data database m save hua hai ki ny islye query kr rhe h
# >>> b=Blog.query.all()
# >>> b
# [<Blog First blog>]

# ab hmlog ko kya krna hai jo hmara blog hai usko home page pe display krwana hai toh home page kaise display krga hmara bloga ka data,data ko bhjnge home page pe....dkho @app.route('/) wale m wha pe data dale hai fir return krwye hai index.html,data=data lkj ke

@app.route("/blogpost",methods=['GET','POST'])
def blogpost():
    # hmlog ye islye likhe methods=['GET','POST'] qki or if request wla code islye start kye qki hum chahte the ki hmara jo blog hai vo fetch hoke home page pe show kre ny thoh isse phle terminal mai ye lkna pad rha tha check krne ke lye blog=Blog(title='First blog',author='Lucky',content='This is my first blog') ki hmara blog wha show kr rha hai ki ny home page pe
    if request.method=='POST':
        title= request.form.get('title')
        author= request.form.get('author')
        content= request.form.get('content')
        blog=Blog(title=title,author=author,content=content)
        db.session.add(blog)
        db.session.commit() 
        # ye message konse page pe display krwynge islye login.html mai iska code {% with messages= uthakar kha tak yha tak {% endwith %} usko index.html ke body ke andar paste krdye 
        flash('Your blog has been successfully submitted','success')
        return redirect('/')
    return render_template("blog.html")
    
# jab continue reading pe click krga toh blog detail khulga wahi bna rhe niche,dkho index.html m continue reading mai {{blog_detail}}/{{blog_id}} lkhe hai wha se fetch krnge yha niche fir continue reading pe click krga toh new page khulga /blog_detail.html page pe show hoga detail
@app.route("/blog_detail/<int:id>",methods=['GET','POST'])
# AssertionError: View function mapping is overwriting an existing endpoint function: blogpost=agr ye error ayga toh smjh jana ki fuction ka name same lkha hua hai
def blogdetail(id):
    blog=Blog.query.get(id)
    return render_template('/blog_detail.html',blog=blog)

# yha pe dlete wla url lkh rhe hai
@app.route("/delete/<int:id>",methods=['GET','POST'])
def delete_post(id):
    blog=Blog.query.get(id)
    # yha pe delete method ko call kye hai or blog ko pass kye hai
    db.session.delete(blog)
    # commit islye kye hai ki jo changes kye hai database mai jaise ki delete kye hai usko save krde
    db.session.commit()
    # delete krne ke baad message display krwa rhe hai
    flash('Post has been deleted successfully','success')
    # fir usko home page pe return krwa rhe hai
    return redirect('/')
    # jab ye home page pe jyga mtlab index.html pe toh wha pe delete wla message phle se lkha hua hai konsa ye message niche wla 
#     {% with messages = get_flashed_messages(with_categories=true) %}
#   {% if messages %}
#     <ul class=flashes>

#     {% for category, message in messages %}
#       <div class="alert alert-{{category}}  alert-dismissible fade show" role="alert">
#      <strong>Message:</strong> {{message}}
#       <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
#     </div>

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit_post(id):
    blog=Blog.query.get(id)
    if request.method=='POST':
     blog.title=request.form.get('title')
     blog.author=request.form.get('author')
     blog.content=request.form.get('content')
     # yha pe db.session.add ny kr rhe h qki hum new post ny post kr rhe h existing mtlab jo post tha ussi mai kuch changes kr rhe h
     db.session.commit()
     flash('Post has been updated successfully','success')
     return redirect("/")
    
   
 # ye blog=blog islye lkhe hai ki jab edi.html page m jyga tohblog ka jo value hia jo title author content ka value hai vo wha pe dkhe jab edit kroge tab, islye hum edit.html mai value dye hai title author content ko dkho ye value='{{blog.author}}'
    return render_template('edit.html',blog=blog)




if __name__ == '__main__':
  app.run(debug=True)