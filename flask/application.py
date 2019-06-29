import os, io, base64

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

import cv2
import numpy as np
from PIL import Image

import keras
from keras import backend as K
import pprint

application = Flask(__name__)
application.config['SECRET_KEY'] = os.urandom(24)

# MNIST Beginner推論
def predict_keras_mnist_beginner(srcimg):
    K.clear_session()
    # Model
    model = keras.models.load_model('./model/tf_keras_mnist_beginner_weights.h5')

    x = srcimg / 255.0
    src_array = np.array(x)
    src_array = src_array.reshape(1, 28, 28)
    print(src_array.shape)
    print(src_array)

    predict = np.argmax(model.predict(src_array))
    print(predict)
    return(predict)


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')

###
# WebAPI送受信サンプル
#
@application.route('/api/predict/beginner', methods=['POST'])
def apitest():
    #application.logger.warn('test message')
    if request.method == 'POST':
        json_data = request.get_json()
        encoded_img = json_data['image']
        decode_data = base64.b64decode( encoded_img.split(',')[1] )

        # バイトストリーム
        img_binarystream = io.BytesIO(decode_data)
        # PILイメージ <- バイナリーストリーム
        img_pil = Image.open(img_binarystream)
        # numpy配列(RGBA?) <- PILイメージ
        img_numpy = np.asarray(img_pil)

        # RGBAの分離（たぶん）
        r, g, b, a = cv2.split(img_numpy)
        # なぜかAのところに白黒反転した絵が保持られているので、それをそのまま入力画像として流用する
        # 細かい理屈はあとで考えよう．．．
        inputimg = cv2.resize(a, (28,28))

        result = predict_keras_mnist_beginner(inputimg)
        #print(result[0])

        #result = { 'predict_keras_beginner': str(predict_keras_beginner[0]) }
        result = { 'predict_keras_beginner': 1 }
        return jsonify( result )

if __name__ == '__main__':
    application.debug = True
    application.run()

