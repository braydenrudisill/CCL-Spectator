from flask import Flask, request
from flask_cors import CORS

from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import time

import threading

PLAYERS = ['Hikaru', 'Jumbo']
PROFILES = ['d6yazgt3.default-release', 't0vwinqt.User1']

app = Flask(__name__)
CORS(app)

options = {}
for player, profile in zip(PLAYERS, PROFILES):
    options[player] = Options()
    options[player].add_argument('-headless')
    options[player].add_argument("-profile")
    options[player].add_argument(f'/Users/braydenrudisill/Library/Application Support/Firefox/Profiles/{profile}/')

browsers = {}

N = 5   # Number of browsers to spawn
thread_list = list()

def create_browser(player):
    browsers[player] = Firefox(options=options[player])

    browsers[player].get(f'https://www.chess.com/member/{player}')
    time.sleep(2)

    profile_header = browsers[player].find_element(By.CSS_SELECTOR, '.profile-header-info')
    profile_urls = profile_header.find_elements(By.TAG_NAME,'a')

    live_url = None
    for url in profile_urls:
        href = url.get_attribute('href')
        if 'live' in href:
            live_url = href
            break

    if not live_url:
        print(f"Couldn't find a live game for {player}.")
        browsers[player].quit()
        return
    else:
        print(f"loaded {player} at {live_url}")

    browsers[player].get(live_url)

# Start test
for player in PLAYERS:
    print(player)
    t = threading.Thread(name='Player {}'.format(player), target=create_browser(player))
    t.start()
    print(t.name + ' started!')
    thread_list.append(t)

# # Wait for all threads to complete
# for thread in thread_list:
#     thread.join()

@app.route(f'/get_live_data')
def get_live_data():
    player = request.args.get('username')
    try:
        pgn = browsers[player].find_element(By.CSS_SELECTOR,'#live-game-tab-scroll-container')
    except:
        ids = browsers[player].find_elements(By.XPATH,'//*[@id]')
        return [ii.get_attribute('id') for ii in ids]
             
    moves = pgn.text.split('.\n')[1:]
    moves = [move.split('\n')[:4:2] for move in moves]

    return moves