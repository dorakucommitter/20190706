###
# 下記サイトの解説からisaaxとRaspberryPiとFlaskを取ったソース
#ß
# * [ラズパイを使ってモノの判別を行なってみよう – Isaax Camp](https://camp.isaax.io/ja/tips-ja/handson-object-detection)
#

import cv2
import numpy as np

FRAME_HEIGHT = 1280
FRAME_WIDTH = 800

# 認識対象のインデックスと対応するラベル
CLASS_LABEL = {
    0: "background",
    1: "aeroplane",
    2: "bicycle",
    3: "bird",
    4: "boat",
    5: "bottle",
    6: "bus",
    7: "car",
    8: "cat",
    9: "chair",
    10: "cow",
    11: "diningtable",
    12: "dog",
    13: "horse",
    14: "motorbike",
    15: "person",
    16: "pottedplant",
    17: "sheep",
    18: "sofa",
    19: "train",
    20: "tvmonitor"
}

# モデルのロード
net = cv2.dnn.readNetFromCaffe('/tmp/models/MobileNetSSD_deploy.prototxt',
    '/tmp/models/MobileNetSSD_deploy.caffemodel')

def detect(frame):
    # モデルが期待する形状に画像データを前処理する
    frame = cv2.resize(frame, (300, 300))
    blob = cv2.dnn.blobFromImage(
        image=frame,
        scalefactor=0.007843,
        size=(300, 300),
        mean=127.5
    )

    # データの入力・結果の取り出し
    net.setInput(blob)
    out = net.forward()
    # 出力結果の取り出し
    boxes = out[0,0,:,3:7] * np.array([300, 300, 300, 300])
    classes = out[0,0,:,1]
    confidences = out[0,0,:,2]

    for i, box in enumerate(boxes):
        confidence = confidences[i]
        if confidence < 0.5:
            continue

        idx = int(classes[i])
        # 背景は無視
        if idx == 0:
            continue

        (startX, startY, endX, endY) = box.astype('int')
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        label = '{}: {:.2f}%'.format(CLASS_LABEL[idx], confidence * 100)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    frame = cv2.resize(frame, (FRAME_HEIGHT, FRAME_WIDTH))
    return frame


def capture_camera(mirror=True):
    """Capture video from camera"""
    # カメラをキャプチャする
    cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号

    ### 下記はMac Bookの設定
    #cap.set(cv2.CAP_PROP_FPS, 60)           # カメラFPSを60FPSに設定
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_HEIGHT) # カメラ画像の横幅を1280に設定
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_WIDTH) # カメラ画像の縦幅を720に設定
    
    ### 手持ちのLogicool Webカメラだと毎秒10フレーム程度が限界っぽい
    cap.set(cv2.CAP_PROP_FPS, 10)

    while True:
        # retは画像を取得成功フラグ
        ret, frame = cap.read()

        # 鏡のように映るか否か
        if mirror is True:
            frame = frame[:,::-1]

        processed_frame = detect(frame.copy())

        # フレームを表示する
        cv2.imshow('camera capture', frame)
        cv2.imshow('object recognition', processed_frame)

        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break

    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture_camera(mirror=True)
