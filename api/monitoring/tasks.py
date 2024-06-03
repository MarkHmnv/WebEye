import io
import logging
import smtplib
from email.message import EmailMessage

import numpy as np
from PIL import Image
from numpy import signedinteger
from selenium import webdriver
from celery import shared_task

from api.core import config
from api.core.constants import WEBSITE_KEY, MSE_THRESHOLD, options
from api.core.redis_config import rd


@shared_task
def monitor_website(
        url: str,
        website_id: int,
        user_id: int,
        username: str,
        email: str,
        width: int,
        height: int
):
    """
    Celery task to monitor websites for changes by taking screenshots
    and comparing them with cached images using Mean Squared Error.
    """
    try:
        with webdriver.Chrome(options=options) as driver:
            driver.implicitly_wait(5)
            driver.set_window_size(width, height)
            driver.get(url)
            screenshot = driver.get_screenshot_as_png()
        new_img = np.asarray(Image.open(io.BytesIO(screenshot)))
        cached_img = rd.hget(WEBSITE_KEY, f'{website_id}_{user_id}')
        cached_img = np.asarray(Image.open(io.BytesIO(cached_img)))

        _mse = mse(new_img, cached_img)
        logging.info(f'MSE: {_mse}')
        if _mse < MSE_THRESHOLD:
            logging.info('No changes detected')
            return

        rd.hset(WEBSITE_KEY, f'{website_id}_{user_id}', screenshot)
        logging.info('Changes detected')
        send_email_notification(
            to_email=email,
            username=username,
            screenshot=screenshot,
            url=url
        )
    except Exception as e:
        logging.error(e)


def mse(img1: np.ndarray, img2: np.ndarray) -> signedinteger[float]:
    err = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
    err /= float(img1.shape[0] * img2.shape[1])
    return err


def send_email_notification(to_email: str, username: str, screenshot: bytes, url: str):
    email = _get_email_template(to_email, username, screenshot, url)
    with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port) as server:
        server.login(config.smtp_user, config.smtp_password)
        server.send_message(email)


def _get_email_template(to_email: str, username: str, screenshot: bytes, url: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Notification from WebEye: Website changed'
    email['From'] = config.smtp_user
    email['To'] = to_email
    screenshot_cid = 'screenshot'
    email.set_content(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Website Change Notification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                h1 {{
                    color: #333;
                }}
                p {{
                    font-size: 14px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Hello, {username}</h1>
                <p>The website <a href="{url}" target="_blank">{url}</a> has been changed. Please see the screenshot below.</p>
                <img src="cid:{screenshot_cid}" alt="Screenshot" style="max-width: 100%; height: auto; border-radius: 5px;">
            </div>
        </body>
        </html>
        """,
        subtype='html'
    )
    email.add_attachment(
        screenshot,
        maintype='image',
        subtype='png',
        filename='screenshot.png',
        cid=screenshot_cid
    )

    return email
