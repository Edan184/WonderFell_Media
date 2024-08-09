from app import app, bootstrap, profconn, musicconn, db, credentials
import json, html, bcrypt, uuid, math, os, socket, asyncio, websockets
from flask import render_template, request, session, redirect, url_for, flash
from flask_paginate import Pagination, get_page_args, get_page_parameter
from werkzeug.datastructures import ImmutableMultiDict

with open(os.path.expanduser("/short/keys/Wonderfell/Salt")) as file:
    temp_key = file.read().replace('\n', '')
    
app.secret_key = bytes(temp_key, "utf-8")
salt = bcrypt.gensalt()

def ip_query():
# Returns Local IP Address

    return credentials("wonderfell_database")["ip"]

def log_the_user_in(username_inp, password_inp):
# Handler for credentials
# Takes String username and String password and verfies credentials in dictionary
# TODO: associate to database and investigate further cookie enryption
# TODO: Implement classes to pass into pages

    try:
        payload_prime = user_check(username_inp, password_inp)
        payload = payload_prime[0][0]
        sid = uuid.uuid4()

        update_query = "UPDATE client_user SET sid = '{0}' WHERE user = '{1}';".format(sid, username_inp)

        cursor = profconn.cursor()
        cursor.execute(update_query)
        cursor.execute("commit;")
        cursor.close()
        profconn.close()
        profconn.ping()

        if payload_prime[2] == True:
            # If username and password match, 
            #session['id'] = payload[0]
            session['username'] = username_inp
            #session['first_name'] = payload[2]
            #session['last_name'] = payload[3]
            #session['sex'] = payload[4]
            #session['email'] = payload[5]
            #session['bio'] = payload[7]
            session['sid'] = sid
            session['filter'] = []

            if 'sid' in session:
                return False
            else:
                return True
            # Apply cookie
        else:
            # Fail intentionally to move to except clause
            session['sid'] != None
            return True

    except Exception as e:
        print("Log_the_user_in failed, error:", e)
        return True
        # Apply True state to failed boolean and return to login() function to set

def user_check(username_inp, password_inp):
# Checks to see if user exists and to pull user information

    try:
        query = 'SELECT id, user, first_name, last_name, sex, email, password_hash, bio FROM client_user WHERE user = "{0}";'.format(username_inp)
        query2 = 'SELECT (user) FROM client_user WHERE user = "{0}";'.format(username_inp)

# User info dictionary
        cursor = profconn.cursor()
        cursor.execute(query)
        logged = cursor.fetchall()
        cursor.close()
        profconn.ping()

# User exists (T/F)
        cursor = profconn.cursor()
        cursor.execute(query2)
        existing = cursor.fetchall()
        cursor.close()
        profconn.close()
        profconn.ping()

        if (existing == ()) == True:
            print("User doesn't exist, failing user_check()")
            logged = [""]
            existing = [[""]]
            phash = False
        else:
            phash = bcrypt.checkpw(password_inp.encode(), logged[0][6].encode())
        user_log = [logged, existing, phash]
        return user_log

    except Exception as error:
        # TODO: Make more appropriate exit
        print("User_check failed, error:", error)
        return redirect(url_for("login"))

def session_info():
    try:
        query = 'SELECT id, user, first_name, last_name, sex, email, bio FROM client_user WHERE user = "{0}" and sid = "{1}";'.format(session['username'], session['sid'])

        cursor = profconn.cursor()
        cursor.execute(query)
        logged = cursor.fetchall()
        cursor.close()
        profconn.close()
        profconn.ping()

        if (logged == ()) == True:
            print("Failing session_check()")
            return False

        user_log = [logged]
        return user_log

    except Exception as e:
        # TODO: Make more appropriate exit
        print("Session_info failed, error:", e)
        return False


def total_recs():

    query = """SELECT * FROM music ORDER BY artist ASC;"""
    cursor = musicconn.cursor()
    cursor.execute(query)
    payload = cursor.fetchall()
    cursor.close()
    musicconn.close()
    musicconn.ping()

    return payload

def query_mysql(search_inp, page_inp):
# Used to search for track metadata

    payload = {}
    for i in search_inp:
        query = """SELECT * FROM music WHERE (id LIKE '%{0}%' OR artist LIKE '%{0}%' OR title LIKE '%{0}%' OR album LIKE '%{0}%' OR length LIKE '%{0}%' OR genre LIKE '%{0}%' OR bitrate LIKE '%{0}%' OR filename LIKE '%{0}%');""".format(i)
        query2 = """SELECT * FROM music WHERE (id LIKE '%{0}%' OR artist LIKE '%{0}%' OR title LIKE '%{0}%' OR album LIKE '%{0}%' OR length LIKE '%{0}%' OR genre LIKE '%{0}%' OR bitrate LIKE '%{0}%' OR filename LIKE '%{0}%') ORDER BY artist ASC LIMIT {1} OFFSET {2};""".format(i, 250, page_inp)
        # print(i)

        if page_inp != None:
            cursor = musicconn.cursor()
            cursor.execute(query2)
            for i in cursor.fetchall():
                payload[i[0]] = i
            cursor.close()
            musicconn.close()
            musicconn.ping()
            return payload        
        else:
            cursor = musicconn.cursor()
            cursor.execute(query)
            for i in cursor.fetchall():
                payload[i[0]] = i
            cursor.close()
            musicconn.close()
            return payload

def query_mysql2(per_page, offset):
# To controll the offset of entries for searched queries

    query = '''SELECT * FROM music ORDER BY artist ASC LIMIT {0} OFFSET {1};'''.format(per_page, offset)
    cursor = musicconn.cursor()
    cursor.execute(query)
    payload = cursor.fetchall()
    cursor.close()
    musicconn.close()
    return payload

def refresh_user(username_inp, password_inp):
    # Handler for credentials
    # Takes String username and String password and verfies credentials in dictionary
    # TODO: Implement classes to pass into pages

    if 'METHOD' == "POST":
        return redirect(url_for('home'))
    elif session_info() is not True:
        try:
            cursor = profconn.cursor()
            query = '''SELECT password_hash FROM client_user WHERE user = "{}";'''.format(username_inp)
            cursor.execute(query)
            hashed_pass = cursor.fetchall()[0][0]
            cursor.close()
            profconn.close()
            profconn.ping()

            payload = user_check(username_inp, password_inp)[0][0]
            sid = uuid.uuid4()

            cursor = profconn.cursor()
            cursor.execute("""UPDATE client_user SET sid = '{0}' WHERE user = '{1}';""".format(sid, username_inp))
            cursor.close()
            profconn.close()
            profconn.ping()

            hash_check = bcrypt.checkpw(password_inp.encode(), hashed_pass.encode())
            if hash_check == True:
                # If username and password match, 
                #session['id'] = payload[0]
                session['username'] = payload[1]
                #session['first_name'] = payload[2]
                #session['last_name'] = payload[3]
                #session['sex'] = payload[4]
                #session['email'] = payload[5]
                #session['bio'] = payload[7]
                session['sid'] = sid
                return True
                # Apply cookie
            else:
                # Fail intentionally to move to except clause
                session['username'] != None

        except Exception as e:
            print("Error:" + e)
            return False
            # Apply True state to failed boolean and return to login() function to set
    else:
        return redirect(url_for(login))

def change_user_info(payload):
    # payload is dict with 'password' key and associated input in profile page password
    # if len(new_password) != 0 and len(old_password) != 0:
    #    if len(user_check(session['username'], old_password)[0][0]) == 0:
    #        error = "Invalid password configuration"
    #        return redirect(url_for("profile"))

    #changes_dict = {}
    #changes = {'user': user, 'first_name': first_name, 'last_name': last_name, 'sex': sex, 'email': email, 'bio': bio}
    #for k, v in changes.items():
    #    if len(v) != 0:
    #        changes_dict[k] = changes[k]
    payload_new = session_info()[0][0]
    if user_check(payload_new[1], payload['password'])[2] == True:
        query = '''UPDATE client_user SET'''
        query_end = ''' WHERE user = "{0}";'''.format(payload_new[1])

        if len(payload.keys()) == 0:
            error = "No information to update"
            return error

        # iterate through form keys and values to update in MySQL database
        for k, v in payload.items():
            if len(payload.keys()) == 1 and k == "password":
                error = "No information to update"
                return error
            elif len(payload.keys()) > 1 and k != "password":
                query += ' {0} = "{1}",'.format(k, v)
            elif len(payload.keys()) == 1 and k != "password":
                query = '''UPDATE client_user SET {0} = "{1}" '''.format(k, v)

        query = query[:-1] + query_end 
        cursor = profconn.cursor()
        cursor.execute(query)
        cursor.execute("commit;")
        cursor.close()
        profconn.close()
        profconn.ping()
        refresh_user(payload_new[1], payload['password'])
        
        error = ""
        return error
    
    else:
        error = "Invalid password"
        return error

def sanitize_input(input):
# Sanitizes input by getting rid of Python special chars

    i_log = []
    for i in input:
        if i == """\\""" or i == '''%''' or i == '''"''' or i == """'""":
            i_log.append(i)
        else:
            pass

    if len(i_log) > 0:
        error = "Invalid input"
        return error
    else:
        return input
        

# Redirects if ip is given to home screen, if no session cookie is present, redirects to login via home() function
@app.route('/static')
@app.route('/', methods=['GET'])
def global_redirect():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET'])
def home():
    if session_info() is not False: 
        payload = session_info()[0][0]
        # Checks for session cookie, if not present, redirects to login
        return render_template('index.html', title='Hello', ip=ip_query(), user=payload[1], name=payload[2], bio=payload[6])
    else:
        return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if session_info() is not False:  
        # Checks for session cookie, if not present, redirects to login   
        payload = session_info()[0][0]
        posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Seattle!'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }
        ]
        return render_template('index.html', title='Home', ip=ip_query(), user=payload[1], posts=posts, name=payload[2])
    else:
        return redirect(url_for('login'))

@app.route('/music_database', methods=['GET'])
def json_get():
    if session_info() is not False: 
        # Checks for session cookie, if not present, redirects to login   
        json_payload = json.dumps(session["username"], indent=4)
        content = total_recs()
        payload = session_info()[0][0]

        return render_template('json_temp.html', title='JSON', ip=ip_query(), id = payload[0], user = payload[1], name = payload[2], lastname = payload[3], sex = payload[4], email = payload[5], bio = payload[6], jspy = json_payload, content = content)
    else:
        return redirect(url_for('login'))

@app.route('/music_database_v2', defaults={'page':1}, methods=['GET', 'POST'])
@app.route('/music_database_v2/<int:page>', methods=['GET', 'POST'])
def json_get2(page):
    # Checks for session cookie, if not present, redirects to login  
    if session_info() is not False: 
        filename = False
        total = 0
        page_input = 0
        per_page = 250
        payload = session_info()[0][0]

        if request.method == 'POST':
            imd = request.form
            # Use eimd as container to modify request elements
            eimd = imd.to_dict(flat=False)

# If changing page on master song list or accessing Music DB v.2 page
        try:
            if request.method == 'POST' and int(eimd['page_input'][0]) > 0:  
                page = int(request.form['page_input'])
                content = query_mysql2(per_page, (page - 1) * per_page)

                for i in total_recs():
                    total += 1
                
                count = math.ceil(total / per_page)
                
                return render_template('json_temp.php', title='JSON', ip=ip_query(), id = payload[0], 
                user = payload[1], name = payload[2], lastname = payload[3], 
                content = content, page=page, count=count, total=total)
            else:
            
                content = query_mysql2(per_page, (page - 1) * per_page)

                for i in total_recs():
                    total += 1
                
                count = math.ceil(total / per_page)
                
                return render_template('json_temp.php', ip=ip_query(), title='Music Database v.2', id = payload[0], 
                user = payload[1], name = payload[2], lastname = payload[3], content = content, page=page, count=count, total=total)

        except Exception as e:
            print("Music_database_v2 failed, error:", e)
            pass

# If searching for track
        try:
            if request.method == 'POST' and eimd['search_bar']:

                payload_updated = {}
                rev_multi = {}
                search_bar = sanitize_input(eimd['search_bar'])
                content = query_mysql(search_bar, None)
                filter_term = [search_bar]
                session['filter'].append(filter_term)

                for k, v in content.items():
                    if v != ():
                        payload_updated[k] = v
                        rev_multi.setdefault(v, set()).add(k)
                        total += 1

                #TODO Cleanup / break POST if statements to render templates with changed payload
                #work = [values for key, values in rev_multi.items() if len(values) > 1][0]

                count = math.ceil(total / per_page)

                return render_template('json_results.html', ip=ip_query(), title='Music Database v.2', id = payload[0], 
                user = payload[1], name = payload[2], lastname = payload[3], 
                content = payload_updated.values(), page=page, count=count, total=total, filter_term=filter_term)             

            if request.method == 'POST' and eimd['search_bar'] and eimd['page_input']:

                payload_updated = {}
                rev_multi = {}
                search_bar = str(sanitize_input(eimd['search_bar']))
                filter_term = [search_bar]
                content = query_mysql(search_bar, eimd['page_input'])

                for k, v in content.items():
                    if v != ():
                        payload_updated[k] = v
                        rev_multi.setdefault(v, set()).add(k)
                        total += 1

                #TODO Cleanup / break POST if statements to render templates with changed payload
                #work = [values for key, values in rev_multi.items() if len(values) > 1][0]

                count = math.ceil(total / per_page)

                return render_template('json_results.html', ip=ip_query(), title='Music Database v.2', id = payload[0], 
                user = payload[1], name = payload[2], lastname = payload[3], 
                content = payload_updated.values(), page=page, count=count, total=total, filter_term=filter_term)

            else:
            
                content = query_mysql2(per_page, (page - 1) * per_page)

                for i in total_recs():
                    total += 1
                
                count = math.ceil(total / per_page)
                
                return render_template('json_temp.php', ip=ip_query(), title='Music Database v.2', id = payload[0], 
                user = payload[1], name = payload[2], lastname = payload[3], content = content, page=page, count=count, total=total)

        except Exception as e:
            print("Music_database_v2 failed, outer error, error:", e)
            return redirect(url_for("index"))
        
    else:
        return redirect(url_for('login'))

@app.route('/music_database_v2/results', defaults={'page':1}, methods=['GET', 'POST'])
@app.route('/music_database_v2/results/<int:page>', methods=['GET', 'POST'])
def json_get3(search_boxpage):
    # Checks for session cookie, if not present, redirects to login  
    if session_info() is not False: 
        filename = False
        total = 0
        page_input = 0
        per_page = 250
        payload = session_info()[0][0]

# If searching for track
        try:
            if request.method == 'POST' and request.form['search_bar']:

                payload_updated = {}
                rev_multi = {}
                search_bar = sanitize_input(request.form['search_bar'])
                content = query_mysql(search_bar, None)

                for k, v in content.items():
                    if v != ():
                        payload_updated[k] = v
                        rev_multi.setdefault(v, set()).add(k)
                        total += 1

                #TODO Cleanup / break POST if statements to render templates with changed payload
                #work = [values for key, values in rev_multi.items() if len(values) > 1][0]

                count = math.ceil(total / per_page)

                return render_template('json_results.html', ip=ip_query(), title='Music Database v.2', id = payload[0], 
                user = payload[1], name = payload[2], lastname = payload[3], 
                content = payload_updated.values(), page=page, count=count, total=total)             

            if request.method == 'POST' and request.form['search_bar'] and request.form['page_input']:

                payload_updated = {}
                rev_multi = {}
                search_bar = sanitize_input(request.form['search_bar'])
                content = query_mysql(search_bar, request.form['page_input'])

                for k, v in content.items():
                    if v != ():
                        payload_updated[k] = v
                        rev_multi.setdefault(v, set()).add(k)
                        total += 1

                #TODO Cleanup / break POST if statements to render templates with changed payload
                #work = [values for key, values in rev_multi.items() if len(values) > 1][0]

                count = math.ceil(total / per_page)

                return render_template('json_results.html', ip=ip_query(), title='Music Database v.2', id = payload[0], 
                user = payload[1], name = payload[2], lastname = payload[3], 
                content = payload_updated.values(), page=page, count=count, total=total)

            else:
            
                content = query_mysql2(per_page, (page - 1) * per_page)

                for i in total_recs():
                    total += 1
                
                count = math.ceil(total / per_page)
                
                return render_template('json_temp.php', ip=ip_query(), title='Music Database v.2', id = payload[0], 
                user = payload[1], name = payload[2], lastname = payload[3], content = content, page=page, count=count, total=total)

        except Exception as e:
            print("Music_database_v2 results failed, error:", e)
            return redirect(url_for("index"))

    else:
        return redirect(url_for('login'))

@app.route('/connect_four', methods=['GET'])
def connect_four():
    if session_info() is not False:
        # Checks for session cookie, if not present, redirects to login
        payload = session_info()[0][0]
        return render_template('connect_four.html', title='Connect Four!', ip=ip_query(), user=payload[1], name=payload[2])
    else:
        return redirect(url_for('login'))

@app.route('/mplayer', methods=['GET', 'POST'])
def mplayer():
    if session_info is not False: 
    # Checks for session cookie, if not present, redirects to login   

        json_payload = json.dumps(session["username"], indent=4)
        payload = session_info()[0][0]

        return render_template('mplayer.html', title='Music Player', ip=ip_query(), id = payload[0], user = payload[1], name = payload[2], lastname = payload[3], sex = payload[4], email = payload[5], bio = payload[6], jspy = json_payload)
    else:
        return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    error = None
    
    if session_info() is not False:
        payload = session_info()[0][0]
        if request.method == "POST":

            form_vals = {}
            for k, v in request.form.items():
                if v.strip() != "":
                    form_vals[k] = sanitize_input(v)
                    if form_vals[k] == "Invalid input":
                        return render_template('profile.html', ip=ip_query(), id = payload[0], user = payload[1], name = payload[2], lastname = payload[3], sex = payload[4], email = payload[5], bio = payload[6], error=form_vals[k])
            
            if "" in form_vals.values():
                return redirect(url_for('profile'))
            #if request.form['first']
            payload_form = form_vals
            if "password" in payload_form.keys(): 
                error = change_user_info(payload_form)

                payload = session_info()[0][0]

                return render_template('profile.html', ip=ip_query(), id = payload[0], user = payload[1], name = payload[2], lastname = payload[3], sex = payload[4], email = payload[5], bio = payload[6], error=error)

            else:
                error = "Invalid password"

                return render_template('profile.html', ip=ip_query(), id = payload[0], user = payload[1], name = payload[2], lastname = payload[3], sex = payload[4], email = payload[5], bio = payload[6], error=error)

        elif request.method == "GET":
            return render_template('profile.html', ip=ip_query(), id = payload[0], user = payload[1], name = payload[2], lastname = payload[3], sex = payload[4], email = payload[5], bio = payload[6])

        else:
            return redirect(url_for("login"))

    else:
        return redirect(url_for("login"))

@app.route('/login', methods=['POST', 'GET'])
def login():
    # TODO: set so that users within active session get redirected
    if session_info() is not False:
        return redirect (url_for("home"))
    error = ""
    if request.method == "POST":
        creds = [html.escape(request.form['user']).lower(), request.form['password']]
        # Take input from page and apply to list
        try:
            failed = log_the_user_in(creds[0], creds[1])
            # Apply returned boolean of log_the_user_in() to 'failed' variable
            if failed == False:

                return redirect(url_for('home'))
                
            else:
                #Intentionally fail to go to except clause
                if session['username'] != creds[0]:
                   
                    pass # Shouldn't have to be used
        except:
            
            if failed == True:
                error = "Invalid login"
                return render_template('form.html', title='Failed Login', ip=ip_query(), error=error)
    return render_template("form.html", ip=ip_query(), error=error)
#    uname = request.form['text']
#    processed_text = uname.upper()
#    return processed_text

@app.route('/logout', methods=['GET'])
def logout():
    try:
        session['sid'] = ""
        session['first_name'] = ""
        session['last_name'] = ""
        session['sex'] = ""
        session['bio'] = ""
        session['username'] = ""

        return redirect(url_for("login"))
    except:
        return redirect(url_for("home"))

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    # TODO: set so that users within active session get redirected
    #session.pop('username', None)
    if session_info() is not False:
        return redirect (url_for("home"))
    error = ""
    if request.method == "POST":
        # Take input from page and apply to username variable and dictionary
        username = html.escape(request.form['username']).lower()
        creds = {username: [request.form['password'], 
        request.form['password2'], request.form['first_name'], request.form['last_name'],
        request.form['email'], request.form['sex'], request.form['bio'], bcrypt.hashpw(request.form['password'].encode(), salt).decode()]}
        # Check for whitespace
        # TODO: Sanitize
        for i in creds[username]:
            if i == creds[username][7]:
                pass
            i = i.strip()
            if len(i) == 0:
                error = "Please enter into all fields"
                return render_template('sign_up.html', ip=ip_query(), error = error)

        # If username is blank, return to sign up
        if username == "":
            error = "Please enter into all fields"
            return render_template('sign_up.html', ip=ip_query(), error = error)
        
        # If password do not match, return to sign up page
        elif creds[username][0] != creds[username][1]:
            error = "Passwords do not match"
            return render_template('sign_up.html', ip=ip_query(), error = error)

        try:
            if username != user_check(username, creds[username][0])[1][0][0]:
                query = '''INSERT INTO client_user (user, first_name, last_name, sex, email, password_hash, bio) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}");'''.format(username,
                creds[username][2], creds[username][3], creds[username][5], 
                creds[username][4], creds[username][7], creds[username][6])
                # Apply returned boolean of log_the_user_in() to 'failed' variable
                failed = log_the_user_in(username, creds[username][0])
                if failed == True:
                    cursor = profconn.cursor()
                    cursor.execute(query)
                    cursor.execute("commit;")
                    cursor.close()
                    profconn.close()
                    profconn.ping()

                    log_the_user_in(username, creds[username][0])

                    return redirect(url_for("home"))
                        
                elif failed == False:
                    error = "Username taken"
                    return render_template("sign_up.html", ip=ip_query(), error=error)
                    
            else:
                error = "User already exists"
                return render_template("sign_up.html", ip=ip_query(), error=error)

        except Exception as e:
            print("Sign_up failed, error", e)
            error = "Please report this problem to admin: " + str(e)  
            return render_template('sign_up.html', ip=ip_query(), title='Failed Login', error=error)
    else:
        return render_template("sign_up.html", ip=ip_query(), error=error)
