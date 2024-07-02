import numpy as np
from PIL import Image, ImageOps
from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def give_most_hex(file_stream, code):
    my_image = Image.open(file_stream).convert('RGB')
    size = max(my_image.size)
    if size < 400:
        return "Image size is too small. Please upload an image with a size of atleast 400x400 pixels."
    scale_factor = 1.0
    if size >= 1200:
        scale_factor = 0.6
    elif size >= 800:
        scale_factor = 0.5
    elif size >= 600:
        scale_factor = 0.4
    elif size >= 400:
        scale_factor = 0.2

    my_image = ImageOps.scale(my_image, scale_factor)
    my_image = ImageOps.posterize(my_image, 2)
    image_array = np.array(my_image)

    unique_colors = Counter(tuple(rgb) for row in image_array for rgb in row)

    top_10 = [color for color, count in unique_colors.most_common(10)]

    if code == 'hex':
        return [rgb_to_hex(color) for color in top_10]
    
    return top_10

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        colour_code = request.form.get('colour_code', 'rgb')
        colours = give_most_hex(f.stream, colour_code)
        return render_template('index.html', colors_list=colours, code=colour_code)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
