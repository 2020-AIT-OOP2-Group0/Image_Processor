import os
import time
import cv2

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

BASEDIR = os.path.abspath(os.path.dirname(__file__))
OUT_DIR = "./output_images/"


def get_ext(filename):
    return os.path.splitext(filename)[-1].lower()


def process(filepath):
    out_filename = os.path.basename(filepath)
    img_bgr = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(OUT_DIR + out_filename, img_gray)


class ChangeHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return
        if get_ext(event.src_path) in ('.jpg', '.jpeg'):
            print('%s has been created.' % event.src_path)
            process(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        if get_ext(event.src_path) in ('.jpg', '.jpeg'):
            print('%s has been modified.' % event.src_path)
            process(event.src_path)


if __name__ == '__main__':
    print('watch on %s' % BASEDIR + "/upload_images")
    while 1:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, BASEDIR + "/upload_images", recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
