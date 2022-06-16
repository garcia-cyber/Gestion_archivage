from flask import Flask ,render_template , request ,redirect , url_for , session ,flash
import mysql.connector as mysql
from datetime import timedelta


# 


sql = mysql.connect(host='localhost', user = 'linux' , password = 'data', database = 'sonas')

sonas = Flask(__name__)
sonas.secret_key = " glody sonas"
sonas.permanent_session_lifetime =timedelta(minutes=4) 

#interface d'accueil 
@sonas.route('/')
@sonas.route('/home')
def home():
    return render_template('index.html')
#login secret histoire d'evite l'entre of all world  and verify login
@sonas.route('/secret')
def secret():

    return render_template('secret.html')


@sonas.route('/secret_verify',methods=["GET","POST"])
def verif():
    if request.method == 'POST':
        
        global sql 
        pw = request.form['code']
        
        session['validate']= pw
        
        print(pw)
        cu = sql.cursor()
        cu.execute("SELECT * FROM secret where pwd = %s " ,(pw,))
        v = cu.fetchone()
        
        if v:
            return redirect(url_for('login'))
        else:
            flash('code non reconnu')
            return redirect(url_for('secret'))
 
    return 'hello'

#login pour se connecte  verification du mot de passe 
@sonas.route('/login')
def login():
    if 'validate' in session:
        validate = session['validate']
        cur = sql.cursor()
        cur.execute("select * from acces")
        all_verify = cur.fetchall()
        return render_template('login.html' , af = all_verify,user = session['validate'])
    else:
        return redirect(url_for('secret'))
@sonas.route('/login_verify',methods=["GET","POST"])
def login_verify():
    if request.method == 'POST':
        acces = request.form['acces']
        user = request.form['user']
        pwd = request.form['pwd']
        
        print(acces)
        
        cur = sql.cursor()
        cur.execute('select * from logins where username = %s and pwd = %s',(user,pwd,))
        
        verify = cur.fetchone()
        
        if acces == '1':
            se = sql.cursor()
            se.execute("select * from logins where username = %s and pwd = %s and type_acces = 1 ",(user,pwd,))
            adm_verify = se.fetchall()
            if adm_verify:
                return redirect(url_for('index3'))
            else:
                flash('mot de passe secretaire incorrect')
                return redirect(url_for('login'))
        elif  acces == '2':
            
            se = sql.cursor()
            se.execute("select * from logins where username = %s and pwd = %s and type_acces = 2 ",(user,pwd,))
            secretaire_verify = se.fetchall()
            if secretaire_verify:
                return redirect(url_for('secretaire'))
            else:
                flash('mot de passe secretaire incorrect')
                return redirect(url_for('login'))
            
             
           
        else:
            ar = sql.cursor()
            ar.execute("select * from logins where username = %s and pwd = %s and type_acces = 3 ",(user,pwd,))
            archiviste_verify = ar.fetchall()
            if archiviste_verify:
                return redirect(url_for('archive'))
            else:
                flash('mot de passe  archiviste incorrect') 
                return redirect(url_for('login'))
           
                
    return 'hello'

#register 

@sonas.route('/register')
def register():
    if 'validate' in session:
        validate = session['validate']
        cur = sql.cursor()
        cur.execute("select * from acces")
        all_verify = cur.fetchall()
        return render_template('register.html',af = all_verify,user = session['validate'])
    else:
        return redirect(url_for('secret'))
@sonas.route('/register_verify',methods=["GET","POST"])
def register_verify():
    if request.method == 'POST':
        acces = request.form['acces']
        user = request.form['user']
        pwd = request.form['pwd']
        pwdc = request.form['pwdc']
        mail = request.form['mail']
        
        if pwd != pwdc:
            #flash("mot de passe doit etre conforme")
            return redirect(url_for('register'))
        else:
            #flash('envoie bon ')  
            if acces == '1':
                cur = sql.cursor()
                cur.execute("insert into logins(username,pwd,email,type_acces)values(%s,%s,%s,%s)",(user,pwd,mail,acces,))
                sql.commit()
                cur.close()
                return redirect(url_for('index3')) 
                
            
            elif acces == '2':
                cur = sql.cursor()
                cur.execute("insert into logins(username,pwd,email,type_acces)values(%s,%s,%s,%s)",(user,pwd,mail,acces,))
                sql.commit()
                cur.close()
                return redirect(url_for('secretaire'))  
                
            else:
                cur = sql.cursor()
                cur.execute("insert into logins(username,pwd,email,type_acces)values(%s,%s,%s,%s)",(user,pwd,mail,acces,))
                sql.commit()
                cur.close()
                return redirect(url_for('archive'))  

    return 'hello'


#page secretaire et son envoie
@sonas.route('/secretaire')
def secretaire():
    cur = sql.cursor()
    cur.execute("select * from communes")
    all2 = cur.fetchall()
    
    x = sql.cursor()
    x.execute("select * from departements")
    twos = x.fetchall()
    return render_template('secretaire.html',on = all2 , two = twos)

@sonas.route('/secretaire_send' ,methods = ['POST'])
def secretaire_send():
    if request.method == 'POST':
        nom     = request.form['nom']
        postnom = request.form['postnom']
        prenom  = request.form['prenom']
        sexe    = request.form['sexe']
        adresse = request.form['adresse']
        commune = request.form['commune']
        phone   = request.form['phone']
        derpt   = request.form['departement']
        
        tel = str(phone)
        global sql 
        send = sql.cursor()
        send.execute("insert into agents(nom,postnom,prenom,sexe,adresse,commune,phone,departement)values(%s,%s,%s,%s,%s,%s,%s,%s)",
                     (nom,postnom,prenom,sexe,adresse,commune,tel,derpt,)) 
        
        sql.commit()
        send.close()   
        flash('agent enregistre'.title())
        return redirect(url_for('secretaire'))
        
        
        
    return render_template('secretaire.html')
#interface d'archivage   
@sonas.route('/archive')
def archive():
    cur = sql.cursor()
    cur.execute("select id_agent, nom,postnom,prenom,sexe,adresse,libelle,phone,date_embauche,upper(type_depart) from agents inner join communes on agents.commune = communes.id_commune inner join departements on agents.departement = departements.id_depart")
    data = cur.fetchall()

    return render_template('archive.html',data = data)


#admin


@sonas.route('/index3')
def index3():
    global sql

    cur = sql.cursor()
    cur.execute("select id_agent, nom,postnom,prenom,sexe,adresse,libelle,phone,date_embauche,upper(type_depart) from agents inner join communes on agents.commune = communes.id_commune inner join departements on agents.departement = departements.id_depart")
    data = cur.fetchall()

    return render_template('index3.html',data=data)


@sonas.route('/delete/<string:id_agent>',methods = ['GET','POST'])
def delete(id_agent):

    #recuperation
    cur = sql.cursor()
    cur.execute("DELETE FROM agents WHERE id_agent = %s",[id_agent])
    sql.commit()
    cur.close()
    return redirect(url_for('index3'))


if __name__ == '__main__':
    sonas.run(debug = True,port = 2022)