
import cv2

def capture_camera(mirror=True, size=None):
    """Capture video from camera"""
    # カメラをキャプチャする
    cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号

    ### 下記はMac Bookの設定
    #cap.set(cv2.CAP_PROP_FPS, 60)           # カメラFPSを60FPSに設定
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # カメラ画像の横幅を1280に設定
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # カメラ画像の縦幅を720に設定

    ### 手持ちのLogicool Webカメラだと毎秒10フレーム程度が限界っぽい
    cap.set(cv2.CAP_PROP_FPS, 10)

    while True:
        # retは画像を取得成功フラグ
        ret, frame = cap.read()

        # 鏡のように映るか否か
        if mirror is True:
            frame_mirror = frame[:,::-1]

        # フレームをリサイズ
        # sizeは例えば(800, 600)
        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)
            frame_mirror = cv2.resize(frame_mirror, size)

        # フレームを表示する
        cv2.imshow('camera capture', frame)
        cv2.imshow('camera capture mirror', frame_mirror)

        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break

    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture_camera(mirror=True)
