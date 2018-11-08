import time
import glob
from tqdm import tqdm

from config_drone import BaseConfig as Config
from clients.ldm_client import Livedronemap


def start_image_check():
    img_fname_list = glob.glob('%s/*.JPG' % Config.DIRECTORY_IMAGE_CHECK)

    ldm = Livedronemap(Config.LDM_ADDRESS)
    project_id = ldm.create_project('This is for test', project_type='1')
    ldm.set_current_project(project_id)

    for img_fname in tqdm(img_fname_list):
        eo_fname = img_fname.split('.')[0] + '.txt'
        result = ldm.ldm_upload(img_fname, eo_fname)
        if result.status_code != 200:
            print('Image: %s, EO: %s, Result: %s' % (img_fname, eo_fname, result.status_code))
        time.sleep(1)


if __name__ == '__main__':
    start_image_check()