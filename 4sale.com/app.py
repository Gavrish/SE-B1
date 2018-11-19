from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import db_utils
from argon2 import PasswordHasher
from collections import defaultdict
import map
import greencover 
import os
from flask_mail import Mail,Message
import price
from flask_dropzone import Dropzone
from utils import *
from filter import *

#basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# app configuration
app.config.update(
    UPLOADED_PATH='static/images/properties',
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=5,
    DROPZONE_MAX_FILES=30,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='handle_upload',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='estate_contact_send_btn',
)
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_USERNAME'] = '4.sale.real.estate.property@gmail.com'
app.config['MAIL_PASSWORD'] = 'forsaleestate'
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
mail=Mail(app)
dropzone = Dropzone(app)

# Handling main page
@app.route('/')
@app.route('/index.html', methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
            data = request.form
            #print(data)
            hashedPassword = ph.hash(data["password"])
            db.insert('users',username=data["username"],passwd=hashedPassword,firstname=data["firstname"],lastname=data["lastname"],email=data["emailid"],phone=data["phone"])
    db.cursor.execute("select tag,count(tag) from tags group by tag")
    tags = db.cursor.fetchall()[:10]
    return render_template('index.html',tags=tags)

# Handling about page
@app.route('/about.html')
def about_page():
    return render_template('about.html')

# Handling contact page
@app.route('/contact.html')
def contact_page():
    return render_template('contact.html')

# Handling listings_single page
@app.route('/listings_single.html')
def listings_single():
    pid = request.args.get('id')
    print(type(pid))
    data = db.query('properties',pid=pid)[0]
    tags = db.query('tags',pid=pid)
    print(data)
    #print(tags)
    images = db.query('property_images',cols=['image'],pid=pid)
    address = " ".join([data["address"],data["city"],str(data["pincode"])])
    places = db.query('property_analytics',pid=pid)[0]
    #print(distances)
    ward = db.query('ward_mapping',cols=['ward'],locality=data["locality"])[0]['ward']
    print(ward)
    complaints = db.query('complaints',cols=['complaint'],ward=ward)
    print(complaints)
    return render_template('listings_single.html', images = images, data = data, tags = tags, places = places,prop_id=pid, complaints= complaints)

# To process login
@app.route('/process_login',methods=['POST'])
def process_login():
    if request.method == 'POST':
        data = request.form
        user = db.query('users',username=data['username'])
        if(len(user) == 1):
            print('Success: valid username')
            password = user[0]['passwd']
            try:
                if(ph.verify(password,data['password'])):
                    print('Success: valid password')
                    print(user[0]['username'])
                    session['username'] = user[0]['username']
                    print(session['username'])
                    return redirect(url_for('listings'))
            except:
                print('Failure: invalid password')
                return redirect(url_for('login'))
        else:
            print('Failure: invalid username')
            return redirect(url_for('login'))
        
# Handling listings page
@app.route('/listings.html')
def listings():
    data = db.query('properties')
    #print(data)
    tags = db.query('tags')
    #print(tags)
    images = db.query('property_images')
    d1 = defaultdict(list)
    d2 = defaultdict(list)
    for tag in tags:
        d1[tag["pid"]].append(tag["tag"])
    for image in images:
        d2[image["pid"]].append(image["image"])
    print(d1)
    print(d2)
    for elem in data:
        elem['tags'] = d1[elem['pid']]
        elem['images'] = d2[elem['pid']]
    print(data)
    return render_template('listings.html', data = data[::-1])

# Handling login page
@app.route('/login.html')
def login():
    return render_template('login.html')

# Handling post-ad page
@app.route('/post-ad.html')
def post_ad_page():
    if('username' in session):
        return render_template('post-ad.html')
    else:
        return redirect(url_for('login'))

# Handling advanced_filter page
@app.route('/advanced_filter.html')
def advanced_filter():
    db.cursor.execute("select tag,count(tag) from tags group by tag")
    tags = db.cursor.fetchall()[:10]
    return render_template('advanced_filter.html',tags=tags,place_types=map.MapServices().place_types)

# To process advanced_filter
@app.route('/process_advanced_filter',methods=['POST'])
def process_advanced_filter():
    data = request.form
    print(data)
    basicFilter = Filter()
    properties = basicFilter.basic_filter(data,db)
    print(properties)
    tags = db.query('tags')
    #print(tags)
    images = db.query('property_images')
    d1 = defaultdict(list)
    d2 = defaultdict(list)
    for tag in tags:
        d1[tag["pid"]].append(tag["tag"])
    for image in images:
        d2[image["pid"]].append(image["image"])
    print(d1)
    print(d2)
    print(properties)
    for elem in properties:
        print(type(elem))
        elem['tags'] = d1[elem['pid']]
        elem['images'] = d2[elem['pid']]
    return render_template('listings.html', data = properties[::-1])

# To handle image uploads
@app.route('/upload', methods=['POST'])
def handle_upload():
    pid = db.query('properties',cols=['max(pid)'])
    print(pid)
    pid = 0 if pid[0]['max']==None else pid[0]['max']
    if(not(os.path.isdir(os.path.join(app.config['UPLOADED_PATH'],str(pid+1))))):
        os.mkdir(os.path.join(app.config['UPLOADED_PATH'],str(pid+1)))
    if(not(os.path.isdir(os.path.join(app.config['UPLOADED_PATH'],str(pid+1),'property_pics')))):
        os.mkdir(os.path.join(app.config['UPLOADED_PATH'],str(pid+1),'property_pics'))
    for key, f in request.files.items():
        if key.startswith('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'],str(pid+1),"property_pics",f.filename))
            db.insert('property_images',pid=pid+1,image=f.filename)
    print('NNNNOOOOO')
    return '', 204

# Handling register page
@app.route('/register.html')
def register_page():
    return render_template('register.html')

# Handling username check
@app.route('/check_username_taken')
def sql_object():
    name = request.args.get('user')
    res = {"exists": False}
    users = db.query('users', username=name)
    if len(users) > 0:
        print("TAKEN")
        res["exists"] = True
    return jsonify(res)

# Handling forums page
@app.route('/news.html')
def news():
    questions = db.query('questions')
    return render_template('news.html',questions=questions)

# Handling question page
@app.route('/question.html')
def question_page():
    return render_template('question.html')

# Handling discussion page
@app.route('/discuss.html')
def discuss_page():
    qid = request.args.get('qid')
    question = db.query('questions',qid=qid)[0]
    print(question)
    comments = db.query('comments',qid=qid)
    return render_template('discuss.html',question=question,comments=comments)

# Handling question posting processing
@app.route('/process_question',methods=['POST'])
def process_question():
    data = request.form
    db.insert('questions',username=session['username'],title=data['title'],body=data['description'],category=data['category'])
    return redirect(url_for('question_page'))

#  Handling comment posting processing
@app.route('/process_comment',methods=['POST'])
def process_comment():
    data = request.form
    db.insert('comments',username=session['username'],body=data['comment'],qid=data['qid'])
    return redirect(url_for('discuss_page',qid=data['qid']))

# Handling price estimation page
@app.route('/reco.html',methods=['GET','POST'])
def reco():
    if request.method == 'POST':
        data = request.form
        print(data)
        pred = []
        for k in data:
            pred.append(data[k])
        print(pred)	
        p = price.price_est(pred)
        res = p.est(pred)[0]
        print(res) 
        return render_template('reco.html', data = res)
    else:
        return render_template('reco.html')

# Handling vastu page
@app.route('/vastu.html')
def vastu():
	return render_template('vastu.html')

# Handling post ad processing
@app.route('/process_post_ad', methods=['POST'])
def process_post_ad():
    data = request.form
    print(data)
    map_services = map.MapServices()
    map_services.set_coordinates(float(data['lat']),float(data['lng']))
    db.insert_from_dict_and_kw('properties',generate_property_dict(data),username=session['username'])
    pid = db.query('properties',cols=['max(pid)'])[0]['max']
    print(pid)
    map_services.generate_top_two_closest_places()
    map_services.generate_distances()
    img_processor = greencover.Image_Processor(map_services.lat,map_services.long)
    img_processor.store_images_for_pid(pid)
    tags = data['tags'].split(',')
    for tag in tags:
        db.insert('tags',pid=pid,tag=tag)
    db.insert_from_dict_and_kw('property_analytics',generate_property_analytics_dict(map_services.places,map_services.distances),pid=pid,green_cover=img_processor.green_percent)
    return redirect(url_for('listings'))

# Handling filtering properties 
@app.route('/filtering_properties',methods=['POST'])
def filtering_properties():
    data = request.form
    print(data)
    basicFilter = filter.Filter()
    properties = basicFilter.basic_filter(data,db)
    print(properties)
    tags = db.query('tags')
    #print(tags)
    images = db.query('property_images')
    d1 = defaultdict(list)
    d2 = defaultdict(list)
    for tag in tags:
        d1[tag["pid"]].append(tag["tag"])
    for image in images:
        d2[image["pid"]].append(image["image"])
    print(d1)
    print(d2)
    for elem in properties:
        elem['tags'] = d1[elem['pid']]
        elem['images'] = d2[elem['pid']]
    return render_template('listings.html', data = properties[::-1])

# Handling filtering tags 
@app.route('/filter_tags')
def filter_tags():
    tag = request.args.get('tag')
    properties_with_tag = db.query('tags',tag=tag,cols=['pid'])
    properties = []
    for property_item in properties_with_tag:
        properties.extend(db.query('properties',pid=property_item['pid']))
    print(properties)
    tags = db.query('tags')
    #print(tags)
    images = db.query('property_images')
    d1 = defaultdict(list)
    d2 = defaultdict(list)
    for tag in tags:
        d1[tag["pid"]].append(tag["tag"])
    for image in images:
        d2[image["pid"]].append(image["image"])
    print(d1)
    print(d2)
    for elem in properties:
        print('HEREEEEEEEEEEEE',elem)
        elem['tags'] = d1[elem['pid']]
        elem['images'] = d2[elem['pid']]
    return render_template('listings.html', data = properties[::-1])
 
# Handling traffic distance metrics calculation
@app.route('/traffic',methods=['POST'])
def get_traffic_details():
    data = request.form
    m = map.MapServices()
    traffic_details = m.get_distance_metrics(data['origin'],data['destination'])
    return ' '.join([traffic_details[0],traffic_details[1]])

# Handling requests on property ads
@app.route('/process_request',methods=['POST'])
def process_request():
    data = request.form
    db.insert('request',username=session['username'],pid=data['pid'],visit=data['visit'],message=data['message'])
    user = db.query('users',username=session['username'])
    user_email= user[0]["email"]
    user_phone= user[0]["phone"]
    user_firstname=user[0]["firstname"]
    user_lastname=user[0]["lastname"]
    owner=db.query('properties', pid=data['pid'])
    owner_username= owner[0]["username"]
    owner_details=db.query('users',username=owner_username)
    msg="New Message: "+ data['message']+"from user:"+user_firstname+ " "+user_lastname+" with number "+ user_phone +"and preference to site visit as: "+ data['visit']
    send_msg=Message(msg,sender=user_email, recipients=[owner_details[0]["email"]])
    mail.send(send_msg)
    return redirect(url_for('listings'))

# Handling logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home_page'))

if __name__ == '__main__':
    db = db_utils.db(database="forsale", user="root", password="root", host="localhost")
    ph = PasswordHasher()
    app.run()
