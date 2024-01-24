from flask import Flask, request
from flask_cors import CORS

from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


app = Flask(__name__)
CORS(app)

opts1 = Options()
opts1.add_argument('-headless')
opts1.add_argument("-profile")
opts1.add_argument(r'/Users/braydenrudisill/Library/Application Support/Firefox/Profiles/d6yazgt3.default-release/')

opts2 = Options()
opts2.add_argument('-headless')
opts2.add_argument("-profile")
opts2.add_argument(r'/Users/braydenrudisill/Library/Application Support/Firefox/Profiles/t0vwinqt.User1')

	

a = Firefox(options=opts1)
b = Firefox(options=opts2)

a.get('https://www.chess.com/member/Hikaru')
b.get('https://www.chess.com/member/')