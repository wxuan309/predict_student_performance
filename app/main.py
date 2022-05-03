# import requirements needed
from flask import Flask, render_template, request
from utils import get_base_url
import cv2
import numpy as np

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

#encryption key
def create_key(size1, size2):
    np.random.seed(42)
    key = np.random.randint(low=1, high=255, size=(size1, size2), dtype=np.uint8)
    key = key.reshape(size1, size2)
    return key


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')

@app.route(f'{base_url}/upload')
def upload():
    return render_template('image_upload.html')

def encrypt_image(image):
    #create random key of given size
    key = create_key(image.shape[0], image.shape[1])

    #XOR each color channel of the image with the key
    ciphertext_B = cv2.bitwise_xor(image[:,:,0], key)
    ciphertext_G = cv2.bitwise_xor(image[:,:,1], key)
    ciphertext_R = cv2.bitwise_xor(image[:,:,2], key)

    #recombine color channels to get final encrypted or decrypted image (based on what is passed in)
    cypher_BGR = cv2.merge([ciphertext_B, ciphertext_G, ciphertext_R])
    return cypher_BGR

@app.route(f'{base_url}/display', methods=["POST"])
def display():
    if request.method=="POST":

        #get cv2 image from file
        uploaded_file = request.files['file']
        npimg = np.fromfile(uploaded_file, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        #encrypt image
        encrypted = encrypt_image(image)

        #write image to file system and then display
        cv2.imwrite('static/saved_image.png', encrypted)
        return render_template('image_display.html')

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
