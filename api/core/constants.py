from selenium.webdriver.chrome.options import Options

WEBSITE_KEY = 'website_hash'
MSE_THRESHOLD = 30

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')