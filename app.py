from flask import Flask, render_template, request, redirect, flash, abort, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.message import EmailMessage
import requests
from dotenv import load_dotenv
import os


load_dotenv() 
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace('postgres://', 'postgresql://')
else:
    raise ValueError("DATABASE_URL is not set in environment variables")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# initialize the database (run once)
# with app.app_context():
#     db.create_all()

# Utility
def is_logged_in():
    return 'user_id' in session

# --- PAYSTACK CONFIG ---
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
PAYSTACK_INITIALIZE_URL = os.getenv('PAYSTACK_INITIALIZE_URL')
PAYSTACK_VERIFY_URL = os.getenv('PAYSTACK_VERIFY_URL')

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


SECTIONS = {
    'Gentle': 'Gentle Art',
    'Love': 'Love Art',
    'Personality': 'Personality Art',
    'Soul': 'Soul Art'
}

ARTWORK = {
    'Gentle_Art': [
        {
            'src': 'Images/Gentle/drop.jpg',
             'title': 'Ink Dream',
             'desc': 'A dreamy illustration in monochrome.'
        },
        {
            'src': 'Images/Gentle/self-doubt.jpg',
            'title': 'Self Doubt Art',
            'desc': 'Quick urban life capture.'
        },
        {
            'src': 'Images/Gentle/future-love.jpg',
            'title': 'Future Love',
            'desc': 'A speculative scene of tomorrow’s romance.'
        },
        {
            'src': 'Images/Gentle/Helping-Hand.jpg',
            'title': 'Helping Hand',
            'desc': 'Reaching out in gentle solidarity.'
        },
        {
            'src': 'Images/Gentle/Motherly-Love.jpg',
            'title': 'Motherly Love',
            'desc': 'Soft warmth and protection.'
        },
        {
            'src': 'Images/Gentle/The-birth-of-music.jpg',
            'title': 'The Birth of Music',
            'desc': 'An ode to first melodies.'
        }
    ],
    'Love_Art': [
        {
            'src': 'Images/Love/bleeding-heart.jpg',
            'title': 'Bleeding Heart',
            'desc': 'Raw emotion laid bare.'
        },
        {
            'src': 'Images/Love/choked-love.jpg',
            'title': 'Choked Love',
            'desc': 'When passion constricts.'
        },
        {
            'src': 'Images/Love/eternal-love.jpg',
            'title': 'Eternal Love',
            'desc': 'Devotion without end.'
        },
        {
            'src': 'Images/Love/Helpless-Love.jpg',
            'title': 'Helpless Love',
            'desc': 'Surrender to the heart will.'},
        {
            'src': 'Images/Love/Loveless-Life.jpg',
            'title': 'Loveless Life',
            'desc': 'Existence void of warmth.'},
        {
            'src': 'Images/Love/Opposite-Love.jpg',
            'title': 'Opposite Love',
            'desc': 'Contrasting forces entwined.'},
        {
            'src': 'Images/Love/Painful-Love.jpg',
            'title': 'Painful Love',
            'desc': 'Beauty tinged with sorrow.'},
        {
            'src': 'Images/Love/Prisoner.jpg',
            'title': 'Prisoner',
            'desc': 'Captive of one own heart.'},
        {
            'src': 'Images/Love/Puppet-heart.jpg',
            'title': 'Puppet Heart',
            'desc': 'Strings pulled by desire.'},
        {
            'src': 'Images/Love/True-love.jpg',
            'title': 'True Love',
            'desc': 'Pure, authentic connection.'},
        {
            'src': 'Images/Love/Undying-Love.jpg',
            'title': 'Undying Love',
                'desc': 'A bond beyond time.'}
    ],
    'Personality_Art': [
        {
            'src': 'Images/Personality/Broken-Personality.jpg',
            'title': 'Broken Personality',
            'desc': 'Fractured pieces revealing the self.'
        },
        {
            'src': 'Images/Personality/Hidden-Personality.jpg',
            'title': 'Hidden Personality',
            'desc': 'Layers beneath the surface.'
        },
        {
            'src': 'Images/Personality/Ignorance.jpg',
            'title': 'Ignorance',
            'desc': 'Unknown corners of the mind.'
        },
        {
            'src': 'Images/Personality/Mentaity.jpg',
            'title': 'Mentality',
            'desc': 'Thoughtscapes in flux.'
        },
        {
            'src': 'Images/Personality/Mixed-Personality.jpg',
            'title': 'Mixed Personality',
            'desc': 'Dualities in harmony.'
        },
        {
            'src': 'Images/Personality/Multiple-Personality.jpg',
            'title': 'Multiple Personality',
            'desc': 'Many selves within one.'
        },
        {
            'src': 'Images/Personality/One-Personality.jpg',
            'title': 'One Personality',
            'desc': 'Unified identity at rest.'
        },
        {
            'src': 'Images/Personality/Split-Personality.jpg',
            'title': 'Split Personality',
            'desc': 'Opposing selves collide.'
        },
        {
            'src': 'Images/Personality/Yin-Yang-Personality.jpg',
            'title': 'Yin-Yang Personality',
            'desc': 'Balance of opposing forces.'
        }
    ],
    'Soul_Art': [
        {'src': 'https://via.placeholder.com/600x400', 'title': 'Texture Fusion', 'desc': 'Combining textures and ink.'},
        {'src': 'https://via.placeholder.com/600x400', 'title': 'Contrast Play', 'desc': 'High-contrast experiment.'},
    ]
}

# USERS = {}
# def is_logged_in():
#     return session.get('user_email') in USERS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', sections=SECTIONS)

@app.route('/gallery/<section_key>')
def section(section_key):
    if section_key not in SECTIONS:
        abort(404)
    lookup_key = f"{section_key}_Art"
    artworks = ARTWORK.get(lookup_key, [])
    return render_template('section.html',
                            section_title=SECTIONS[section_key],
                            artworks=artworks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        purpose = request.form['purpose']
        message = request.form['message']

        full_message = f"From: {name} <{email}>\nPurpose: {purpose}\n\n{message}"

        try:
            send_email('New Contact Form Submission', full_message)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            print('Error sending email:', e)
            flash('Failed to send message. Please try again later.', 'error')

        return redirect('/contact')

    return render_template('contact.html')

def send_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # Send to yourself
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/buy/<art_title>', methods=['GET'])
def buy(art_title):
    # find the piece
    found = None
    for lst in ARTWORK.values():
        for art in lst:
            if art['title'] == art_title:
                found = art
                break
        if found: break
    if not found: abort(404)
    return render_template('buy.html', art=found, paystack_pk=PAYSTACK_PUBLIC_KEY)

@app.route('/initialize_payment', methods=['POST'])
def initialize_payment():
    email = request.form['email']
    amount_naira = float(request.form['price'])
    amount_kobo = int(amount_naira * 100)
    title = request.form['title']

    callback_url = url_for('paystack_callback', _external=True)

    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'amount': amount_kobo,
        'callback_url': callback_url,
        'metadata': {'custom_fields': [{'display_name': 'Art Title','variable_name':'art_title','value': title}]}
    }

    resp = requests.post(PAYSTACK_INITIALIZE_URL, json=data, headers=headers)
    resp.raise_for_status()
    link = resp.json()['data']['authorization_url']
    return redirect(link)

@app.route('/paystack_callback')
def paystack_callback():
    reference = request.args.get('reference')
    resp = requests.get(PAYSTACK_VERIFY_URL + reference,
                        headers={'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
    resp.raise_for_status()
    status = resp.json()['data']['status']

    if status == 'success':
        art_title = resp.json()['data']['metadata']['custom_fields'][0]['value']
        flash(f"Payment for “{art_title}” successful! Thank you.", 'success')
    else:
        flash("Payment failed or was canceled.", 'error')

    return redirect(url_for('gallery'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            user = User(
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            flash('Account created!', 'success')
            return redirect(url_for('store'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Welcome back!', 'success')
            return redirect(url_for('store'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out', 'success')
    return redirect(url_for('home'))

@app.route('/store')
def store():
    if not is_logged_in():
        flash('Please log in to access the store', 'error')
        return redirect(url_for('login'))
    # flatten all ARTWORK lists into one
    all_art = sum(ARTWORK.values(), [])
    return render_template('store.html', artworks=all_art)


if __name__ == '__main__':
    app.run(debug=True)
