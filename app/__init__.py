import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  model = tf.keras.models.load_model(__name__ + "/model")
  
  
  UPLOAD_FOLDER = "static/uploads"
  class_names = ['NORMAL', "PNEUMONIA"]
  app.secret_key = 'pneumonia-detection-ai'
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
  ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
  
  def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  

  def get_image(filepath):
    # Read image
    img = tf.io.read_file(filepath)

    # Decode image
    img = tf.io.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, [256, 256])
    return img
  
  def make_prediction(img):
    img = tf.expand_dims(img, 0)
    result = model.predict(img)
    score = tf.nn.softmax(result[0])
    return np.argmax(score)

  @app.route("/")
  def index():
    return render_template('index.html')

  @app.route("/", methods=["POST"])
  def upload_image():
    if 'image' not in request.files:
      flash("No file part")
      return redirect(request.url)
    
    image = request.files['image']

    if image.filename == '':
      flash("No image selected for uploading")
      return redirect(request.url)
    
    if image and allowed_file(image.filename):
      filename = secure_filename(image.filename)
      filepath = os.path.join(__name__ + "/" + app.config['UPLOAD_FOLDER'], filename)
      image.save(filepath)
      
      predict_image = get_image(filepath)
      result = class_names[make_prediction(predict_image)]
      flash("Image successfully to save")
      return render_template('index.html', filename=filename, result=result)
    else:
      flash("Image format must be png, jpg or jpeg")
      return redirect(request.url)

  @app.route('/display/<filename>')
  def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
  return app