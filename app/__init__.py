import logging.config
from flask import Flask, render_template, request, redirect, url_for, jsonify, redirect, session
from flask_bcrypt import Bcrypt
from flask_session import Session
import logging
import os
from app.config import Config
from app.services.db import delete_file_db, get_download_file, get_file_share_list, update_fileshare, validateUser, isUsernameUnique, insert_user
from app.services.webservices import create_s3_bucket, delete_file_bucket, is_email_verified, upload_and_notify

def setup_logging(app):
    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(
        app.config.get('LOGS_PATH'), encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(name)s | %(asctime)s | %(process)d | %(levelname)s | %(filename)s | %(lineno)s | %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_class)
    Session(app)
    app_bcrypt = Bcrypt(app)

    setup_logging(app)

    @app.route('/')
    def main():
        """
        Function to display the index page of the application
        
        Params:
        =======
        None
        
        Returns:
        ========
        Renders the index page"""
        return render_template("index.html")

    @app.route('/signin')
    def login():
        """
        Function to display login page
        
        Params:
        =======
        None
        
        Returns:
        ========
        Renders the login page if user is not authenticated else redirected to home"""
        # if ("user" in session):
        #     return redirect(url_for("home"))
        # else:
        return render_template('login.html')

    @app.route('/signup')
    def signup():
        """
        Function to display signup page
        
        Params:
        =======
        None
        
        Returns:
        ========
        Redirects to register page if user is not registered
        """
        if ("user" in session):
            return redirect(url_for("home"))
        else:
            return render_template('register.html')

    @app.route('/validateUser', methods=['POST'])
    def validateLogin():
        """
        Function to execute user validation procedure when url is invoked

        Params:
        =======
        None

        Returns:
        (json) : Return a JSON object representing if the user credentials are valid or not
        """
        username = request.get_json()['username']
        # TODO: app_bcrypt.generate_password_hash()
        password = request.get_json()['password']
        app.logger.info(request.get_json())
        validation = validateUser(username, password)
        session_id = 'user'
        if (validation):
            session["name"] = username
            temp = app_bcrypt.generate_password_hash(username)
            session["user"] = temp
            session_id = temp.decode('utf-8')

        valdiationResult = str(validation).lower()
        return jsonify({'valid_credentials': valdiationResult, 'session_id': session_id})

    @app.route('/checkunique', methods=['POST'])
    def check_unique():
        """
        Function to check the uniqueness of username during registration

        Params:
        =======
        None

        Returns:
        ========
        (json) : Returns a JSON object representing if the username is unique or not
        """
        username = request.get_json()['username']
        app.logger.info(request.get_json())
        isunique = isUsernameUnique(username)
        isunique = str(isunique).lower()
        return jsonify({'isunique': isunique})

    @app.route('/home')
    def home():
        """
        Function to display the homepage of a logged in user

        Params:
        =======
        None

        Returns:
        ========
        redirection to specific page based on authentication
        """
        if ("name" in session):
            return render_template('mainpage.html')
        else:
            return redirect(url_for('login'))
        
    
    @app.route('/displayhome', methods=['POST'])
    def displayhome():
        if ("name" in session):
            user = request.get_json()["user"]
            res = app_bcrypt.check_password_hash(user, session["name"]) 
            app.logger.info(f'User Authentication: {res}')
            username = session["name"]
            payload = get_file_share_list(username)
            payload["route"] = ''
            return jsonify(payload)
        else:
            return jsonify({"route": '/login'})

    @app.route('/upload', methods=['POST'])
    def upload():
        if ("name" in session):
            data = request.form
            app.logger.info(f'form data {data}')
            app.logger.info(f'form data {request.files}')
            userid = data['user_sessionid']

            if(app_bcrypt.check_password_hash(userid, session["name"]) 
                    and request.form['emaillist'] != ''):
                file = request.files['fileupload[]']
                app.logger.info(f'file {file}')
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                emaillist = request.form['emaillist'].split(',')


                is_uploaded = upload_and_notify(user=session['name'], filepath=file_path, emaillist=emaillist)
                if(is_uploaded):
                    os.remove(file_path)
                is_uploaded = str(is_uploaded).lower()
                return jsonify({"isUploaded": is_uploaded, "route_to": '/home'})
            else:
                return jsonify({"isUploaded": 'false', "route_to": '/signin'})
        else:
            return jsonify({"isUploaded": 'false', "route_to": '/signin'})

    
    @app.route('/registeremail', methods=['POST'])
    def registeremail():
        email = request.get_json()['email']
        isVerified = is_email_verified(email)
        isVerified = str(isVerified).lower()
        return jsonify({"isVerified": isVerified})

    @app.route('/registeruser', methods=['POST'])
    def registeruser():
        """
        Function to register a new user
        
        Params:
        =======
        None
        
        Returns:
        ========
        (json) : JSON Object representing the status of adding a new user"""
        finalBucket = ''
        data = request.get_json()

        name = data['firstname'] + ' ' + data['lastname']
        username = data['username']
        email = data['email']
        password = data['password']
        password = app_bcrypt.generate_password_hash(password)
        bucketname = app.config.get('PROJECT_NAME').lower() + '-' + username.lower()
        bucket_result = create_s3_bucket(bucketname)
        if(bucket_result == 0):
            return jsonify({'isuserregistered': "false"})

        if(bucket_result == 1):
            finalBucket = bucketname

        if(bucket_result == 2):
            tempBkt = bucketname + 'usr'
            bucket_result = create_s3_bucket(tempBkt)
            if(bucket_result == 1):
                finalBucket = tempBkt
        
        userDetails = {
            "name": name,
            "username": username,
            "email": email,
            "password": password,
            "bucketname": finalBucket,
        }
        insert_result = insert_user(userdetails=userDetails)
        insert_result = str(insert_result).lower()
        app.logger.info(f'insertion result: {insert_result}')
        return jsonify({'isuserregistered': insert_result})

            
    @app.route('/downloads', methods=['GET'])
    def download():
        sender_email = request.args.get('sender')
        recipient = request.args.get('recipient')
        filename = request.args.get('filename')

        if(sender_email is None
                or recipient is None
                or filename is None):
            return redirect('/')
        
        file_payload = get_download_file(sender_email, recipient, filename)

        if(file_payload['statusCode'] == 200):
            return render_template('download.html', data=file_payload)
        else:
            return render_template('download.html', data={})
        
    @app.route('/downloadupdate', methods=['POST'])
    def downloadupdate():
        data = request.get_json()
        sender = data['sender'] if 'sender' in data else ''
        recipient = data['recipient'] if 'recipient' in data else ''
        filename = data['filename'] if 'filename' in data else ''
        fileurl = data['fileurl'] if 'fileurl' in data else ''

        if(sender == ''
                or recipient == ''
                or filename == ''
                or fileurl == ''):
            return False
        
        result, bucketname, fileid = update_fileshare(sender, recipient, filename, fileurl)
        if(result):
            delete_res = delete_file_bucket(filename, bucketname)
            if(delete_res):
                delete_file_db(fileid)
        return jsonify({'statusCode': 200})

    @app.route('/logout')
    def logout():
        """
        Function to execute logout procedure

        Params:
        =======
        None

        Returns:
        ========
        login page redirect
        """
        session.pop('user', None)
        session.pop('name', None)
        session.clear()
        return redirect(url_for('login'))      
    
    return app
