from flask import Flask, render_template, abort

app = Flask(__name__)

SECTIONS = {
    'Gentle': 'Gentle Art',
    'Love': 'Love Art',
    'Personality': 'Personality Art',
    'Soul': 'Soul Art'
}

ARTWORK = {
    'Gentle_Art': [
        {'src': 'https://via.placeholder.com/600x400', 'title': 'Ink Dream', 'desc': 'A dreamy illustration in monochrome.'},
        {
            'src': '/static/Images/Gentle/self-doubt.jpg',
            'title': 'Self Doubt Art',
            'desc': 'Quick urban life capture.'
        }
    ],
    'Love_Art': [
        {'src': 'https://via.placeholder.com/600x400', 'title': 'Geometric Form', 'desc': 'Abstract 3D shapes.'},
        {'src': 'https://via.placeholder.com/600x400', 'title': 'Monolith', 'desc': 'A lone structure in void.'},
    ],
    'Personality_Art': [
        {'src': 'https://via.placeholder.com/600x400', 'title': 'Texture Fusion', 'desc': 'Combining textures and ink.'},
        {'src': 'https://via.placeholder.com/600x400', 'title': 'Contrast Play', 'desc': 'High-contrast experiment.'},
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
    artworks = ARTWORK.get(section_key, [])
    return render_template('section.html',
                           section_title=SECTIONS[section_key],
                           artworks=artworks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
