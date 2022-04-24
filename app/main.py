# import requirements needed
from flask import Flask, render_template, request, url_for
from utils import get_base_url
from collections import Counter
import matplotlib.pyplot as plt

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')

@app.route('/form')
def get_paragraph():
    return render_template('form.html')

@app.route('/form', methods=['POST'])
def get_graph():
    text = request.form['text_box']
    processed_text = text.split(" ")
    counted = Counter(processed_text)

    x = [tag for tag, count in counted.most_common(20)]
    y = [count for tag, count in counted.most_common(20)]

    fig = plt.figure()
    plt.bar(x, y, color='crimson')
    plt.title("Frequencies of words in entered text")
    fig.savefig('static/saved_img.png')
    return render_template('image.html')

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'url'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
