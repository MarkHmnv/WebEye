import io
import logging

import numpy as np
from PIL import Image
from numpy import signedinteger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from celery import shared_task

from api.core.constants import WEBSITE_KEY, MSE_THRESHOLD
from api.core.redis_config import rd

options = Options()
options.add_argument('--headless=new')
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


@shared_task
def monitor_website(url: str, website_id: int, user_id: int):
    """
    Celery task to monitor websites for changes by taking screenshots
    and comparing them with cached images using Mean Squared Error.
    """
    try:
        with webdriver.Chrome(options=options) as driver:
            driver.implicitly_wait(5)
            driver.get(url)
            screenshot = driver.get_screenshot_as_png()
            new_img = np.asarray(Image.open(io.BytesIO(screenshot)))
            cached_img = rd.hget(WEBSITE_KEY, f'{website_id}_{user_id}')
            if cached_img is None:
                rd.hset(WEBSITE_KEY, f'{website_id}_{user_id}', new_img.tobytes())
                logging.info('Added to cache')
                return

            cached_img = np.frombuffer(cached_img, dtype=new_img.dtype).reshape(new_img.shape)
            _mse = mse(new_img, cached_img)
            logging.info(f'MSE: {_mse}')
            if _mse < MSE_THRESHOLD:
                logging.info('No changes detected')
                return

            rd.hset(WEBSITE_KEY, f'{website_id}_{user_id}', new_img.tobytes())
            logging.info('Changes detected')
    except Exception as e:
        logging.error(e)


def mse(img1: np.ndarray, img2: np.ndarray) -> signedinteger[float]:
    err = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
    err /= float(img1.shape[0] * img2.shape[1])
    return err
