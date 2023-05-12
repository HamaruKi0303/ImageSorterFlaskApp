import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

IMG_FOLDER = 'static/images'
SORTED_FOLDER = 'static/sorted'
ROOT_PATH = '/home/src'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        concept = request.form['selected_concept']
    else:
        concepts = os.listdir(os.path.join(ROOT_PATH, IMG_FOLDER))
        if concepts:
            concept = concepts[0]
        else:
            return "コンセプトが見つかりませんでした。"

    images = os.listdir(os.path.join(ROOT_PATH, IMG_FOLDER, concept))
    if images:
        image = images[0]
        if(image.endswith(".jpg") or image.endswith(".png")):
            image_path = f"{IMG_FOLDER}/{concept}/{image}"
        else:
            image_path = "None"
    else:
        image_path = "None"

    concepts = os.listdir(os.path.join(ROOT_PATH, IMG_FOLDER))
    image_counts = {c: get_image_counts(c) for c in concepts}

    return render_template('index.html', concepts=concepts, concept=concept, image_path=image_path, image_counts=image_counts)
    
@app.route('/sort', methods=['POST'])
def sort():
    concept = request.form['concept']
    image = request.form['image']
    button = request.form['button']

    source_path = os.path.join(ROOT_PATH, IMG_FOLDER, concept, image)
    dest_dir = os.path.join(ROOT_PATH, SORTED_FOLDER, concept, button)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, image)

    try:
        os.rename(source_path, dest_path)
    except:
        pass

    # 画像がなくなったらフォルダ名にアンダーバーを付与
    remaining_images = os.listdir(os.path.join(ROOT_PATH, IMG_FOLDER, concept))
    if not any(img.endswith(".jpg") or img.endswith(".png") for img in remaining_images):
        os.rename(os.path.join(ROOT_PATH, IMG_FOLDER, concept),
                  os.path.join(ROOT_PATH, IMG_FOLDER, f"_{concept}"))

    return redirect(url_for('index'))
def get_image_counts(concept):
    concept_path = os.path.join(ROOT_PATH, IMG_FOLDER, concept)
    total_images = len([img for img in os.listdir(concept_path) if img.endswith(".jpg") or img.endswith(".png")])
    
    sorted_counts = {}
    for label in ['OK', 'NG', 'R18', 'R20']:
        if concept.startswith('_'):
            label_path = os.path.join(ROOT_PATH, SORTED_FOLDER, concept[1:], label)
        else:
            label_path = os.path.join(ROOT_PATH, SORTED_FOLDER, concept, label)

        if os.path.exists(label_path):
            sorted_counts[label] = len([img for img in os.listdir(label_path) if img.endswith(".jpg") or img.endswith(".png")])
        else:
            sorted_counts[label] = 0

    return total_images, sorted_counts

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7007, debug=True)