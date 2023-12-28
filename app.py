from flask import Flask, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
import itertools
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "a4b2zt745srty"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Tournament.sqlite3"
app.config["UPLOAD_FOLDER"] = "static"

db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name",db.String(300))
    pname = db.Column("Player name",db.String(300))
    phone = db.Column("Phone",db.String(300))
    points = db.Column("Points",db.Integer)
    profilepic = db.Column("profilepic",db.String(300))
    status = db.Column("status", db.String(300))
    matchpic =db.Column("matchpic", db.String(750))
    
    def __init__(self, id, name, pname, points,profilepic, phone, status, matchpic):
        self.id = id
        self.name = name
        self.pname = pname
        self.points = points 
        self.profilepic = profilepic
        self.phone = phone
        self.status = status
        self.matchpic = matchpic
    
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p1 = db.Column(db.String(300))
    p2 = db.Column(db.String(300))
    score1 = db.Column(db.String(300))
    score2 = db.Column(db.String(300))
    status = db.Column(db.String(500))
    
    def __init__(self, id, p1, p2, score1, score2,status):
        self.id = id
        self.p1 = p1 
        self.p2 = p2
        self.score1 = score1 
        self.score2 = score2
        self.status = status
        
with app.app_context():
    db.create_all()
    
def get_id(CLASS):
    idlist = []
    
    try:
        for instance in CLASS.query.all():
            idlist.append(instance.id)
            
        return max(idlist) + 1
    
    except:
        return int(1)

@app.route("/")

def index():
    try:
        print(session["player"])
        
    except:
        session["loggedin"] = "False"
        
    current = datetime.datetime.today()
    return render_template("index.html", date=current)
    
@app.route("/tournament/signup")
def signup():
    return render_template("signup.html")
    
@app.route("/tournament/register",methods=["POST", "GET"] )
    
def register():
    current = datetime.datetime.today()
    if request. method == "POST":
        """collect data""" 
        name = request.form["name"]
        pname = request.form["playername"]
        phone = request.form["phone"]
        
        for player in Player. query.all():
            if player.name == name or player.pname == pname or player.phone == phone:
                return render_template("signup_failed.html")
                
            else:
                pass           
        
        player = Player(get_id(Player) , name, pname, 0, "", phone, "Alive", "")
        session["status"] = "Alive"
        db.session.add(player)
        db.session.commit()
        return render_template("signup_success.html")
        
    else:
        return render_template("index.html", date=current)
        
#admin command
@app.route("/table/p")

def view():
    query = Player.query.all()
    return render_template("table.html", Allplayers=query)
    
    #admin command
    
@app.route("/start_mixup")

def mixup(): 
    flist = []
    plist = [] 
    for player in Player.query. all(): 
        if player.status =="eliminated":
            pass
            
        else:
            
            plist.append(player.pname)
            for i in range(len(plist)//2):
                a = random. choice(plist)
                plist.remove(a)
                b = random.choice(plist)
                plist.remove(b)
                flist.append((a, b))
            
            
        
    #shake_up = itertools.combinations(plist, 2)
    
    try:
      for any_match in Match.query.all():
          db.session. delete(any_match)
          db.session.commit()
          
    except:
      pass
      
      
    for shake in flist:
        match = Match(get_id(Match), shake[0], shake[1] ,"- -", "- -", "-")
        db.session.add(match)
        db.session. commit()
    return render_template("vmad.html", all=Match.query.all())
    
@app.route("/clear_all")
 
def clear_all(): 
    for player in Player.query.all(): 
        db.session. delete(player) 
        db.session.commit()
         
    for match in Match.query.all():
        db.session. delete(match)
        db.session. commit()

    return """<h1> All Players And Matches Cleared </h1>"""

@app.route("/tournament/all_matchups")

def show_matchups():
    current = datetime.datetime.today()
    try:
        if session["loggedin"] == "True":
            return render_template("vm.html", all=Match.query.all())
    except KeyError: 
        return redirect(url_for("login"))
        
        
    else:
        return redirect(url_for("login"))
    
@app.route("/tournament/login")

def login():
    return render_template("login.html")
    
@app.route("/tournament/verification", methods=["POST", "GET"])

def verify():
    
    if request.method == "POST":
        pname = request.form["pname"]
        phone = request.form["phone"]
        
        if pname == "ADMINX" and str(phone) == "00000000049":
            return redirect(url_for("manage"))
        
        try:
            try:
                for player in Player. query.all():  
                    if player.pname == pname and str(player.phone)== str(phone): 
                        session["loggedin"] = "True" 
                        session["pname"] = pname 
                        session["name"] = player.name 
                        session["phone"] = str(player.phone)
                        session["profilepic"] = player.profilepic
                        session["id"] = player.id
                        return render_template("login_success.html")
                        
                return render_template("login_failed.html")
                        
                        
            except:
                 return render_template("login_failed.html")
                                
                    
        except:
            return "UNKNOWN ERROR"            
            
    else:
        return redirect(url_for("login"))

@app.route("/player/profile")

def profile():
    x = ""
    try:
        if session["loggedin"] == "True":
            p = Player.query. filter(Player.id == session["id"]).first()
            session["profilepic"] = p.profilepic
            return render_template("profile.html", picture=p.profilepic)

        else: 
            return redirect(url_for("login"))
  
    except: 
        return redirect(url_for("login"))
  
        
@app.route("/upload_pic", methods=["POST"])

def upload_pic():
    x = 1

    if request.method == "POST":
        pic = request.files["file"]
        
        if x == 1:
            
            player = Player.query.filter(Player.id==session["id"]).first() 
        
            if str(pic.filename) != "": 
                pic.save(app.config["UPLOAD_FOLDER"] + "/" + str(pic.filename))
                
            else: 
                return render_template("profile.html", picture=session["profilepic"])
                    
           # player = Player. query.filter(Player.id==session["id"]).first()
                    
            player.profilepic = str(pic.filename) 
            db.session.commit() 
            session["profilepic"] = str(str(app.config["UPLOAD_FOLDER"])+ "/"+ str(pic.filename)) 
            return render_template("profile.html", picture=player.profilepic)
                        
        else:
            return "%s Error Uploading File"
        
    else:
        return render_template("profile.html", picture=player.profilepic)
        
@app.route("/manage/admin")
    
def manage():
    return render_template("adminpage.html")
    
@app.route("/newscore/<int:id>/<int:s1>/<int:s2>")

def changescore(id,s1,s2):
    match_delta = Match.query.filter(Match.id==id).first()
    match_delta.score1 = s1 
    match_delta.score2 = s2
    db.session. commit()
  
    match_delta.status = "ended"
    db.session.commit()
    return "match %s vs %s ----%s : %s and match ended"%(match_delta.p1,match_delta.p2,match_delta.score1,match_delta.score2)
    
@app.route("/eliminate/<int:id>")

def eliminate(id):
    player = Player.query.filter(Player.id ==id).first()
    player.status = "eliminated"
    db.session.commit()
    return f"player {player.pname} has Been eliminated"
    
@app.route("/delmatch/<int:id>")

def remove_match(id): 
    match = Match.query. filter(Match.id ==id).first()
    db.session.delete(match)
    db.session. commit()
    return "%MATCH DELETED" #%(match.p1, match.p2)
    
@app.route("/logout")

def logout():
    current = datetime.datetime.today()
    if session["loggedin"] == "True":
        session["loggedin"] = "False"
      #  session.pop("loggedin", None)
        session.pop("name", None)
        session.pop("phone", None)
        session.pop("profilepic", None)
        session.pop("id", None)
        session.pop("pname", None)
        return render_template("index.html", date=current)
        
    else:
        return render_template("index.html", date=current)

