from flask import Flask, render_template, request, redirect, flash, abort
import smtplib
from email.message import EmailMessage


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Email configuration
EMAIL_ADDRESS = 'your_email@example.com'   # <-- put your email here
EMAIL_PASSWORD = 'your_email_password'     # <-- put your app password here

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

if __name__ == '__main__':
    app.run(debug=True)
