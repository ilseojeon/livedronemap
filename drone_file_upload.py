import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config_drone import BaseConfig as Config

image_list = []
eo_list = []


def upload_data(image_fname, eo_fname):
    from clients.ldm_client import Livedronemap
    ldm = Livedronemap(Config.LDM_ADDRESS)
    ldm.create_project(Config.LDM_PROJECT_NAME)
    ldm.set_current_project(Config.LDM_PROJECT_NAME)
    result = ldm.ldm_upload(image_fname, eo_fname)
    print(result)


class Watcher:
    def __init__(self, directory_to_watch):
        self.observer = Observer()
        self.directory_to_watch = directory_to_watch

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            file_name = event.src_path.split('\\')[-1].split('.')[0]
            extension_name = event.src_path.split('.')[1]

            if Config.IMAGE_FILE_EXT in extension_name:
                image_list.append(file_name)
            else:
                eo_list.append(file_name)

            for i in range(len(image_list)):
                if image_list[i] in eo_list:
                    upload_data(
                        os.path.join(Config.DIRECTORY_TO_WATCH, file_name + '.' + Config.IMAGE_FILE_EXT),
                        os.path.join(Config.DIRECTORY_TO_WATCH, file_name + '.' + Config.EO_FILE_EXT)
                    )
                    eo_list.remove(image_list.pop(i))


if __name__ == '__main__':
    w = Watcher(directory_to_watch=Config.DIRECTORY_TO_WATCH)
    w.run()
