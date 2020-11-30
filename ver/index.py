from flask import abort, Flask, flash,g , redirect ,render_template, request, session, url_for

class User:
    def __init__(self, id, username,password):
        self.id=id
        self.username=username
        self.password=password

    def __repr__(self):
        return f'{self.username} ({self.id}) ' 

users = []
users.append(User(0,"stembex_rpa","fj2349jfsjdkj234lkj6sdflsdn43"))
users.append(User(1,"rpa","fj2349jfsjdkj234lkj6sdflsdn43"))


app = Flask(__name__)
app.secret_key = 'secretkey'
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user =[x for x in users if x.id==session['user_id']][0]
        g.user = user
# Creating simple Routes 
@app.route('/login', methods=['GET','POST'])
def login():
    session.pop('user_id',None)
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        user =[x for x in users if x.username==username]
        if user:
            if password == user[0].password:
                session['user_id'] = user[0].id
                return redirect(url_for('home'))
            else:
                flash('Password incorrecto')
                return redirect(url_for('login'))
        else:
            flash('Usuario no existe')
            return redirect(url_for('login'))

    return render_template("login.html")

# Routes to Render Something
@app.route('/')
def home():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("home.html")

@app.route('/forb')
def forb():
    abort(403)

@app.route('/embarques')
def emb():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("embarques.html")

@app.route('/embarques/maritimo')
def mar():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("maritimo.html")

@app.route('/embarques/maritimo/2020')
def a2020():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("2020.html")

@app.route('/embarques/maritimo/2017')
def a2017():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("2017.html")


# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
