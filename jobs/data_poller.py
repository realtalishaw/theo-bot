# jobs/data_poller.py

import time
from api.user import get_all_users
from api.universe import get_all_planets, get_all_moons, get_all_satellites
from api.project import get_all_projects

def poll_data():
    while True:
        poll_users()
        poll_planets()
        poll_moons()
        poll_satellites()
        poll_projects()
        time.sleep(3600)  # Poll every hour

def poll_users():
    get_all_users()

def poll_planets():
    get_all_planets()

def poll_moons():
    get_all_moons()

def poll_satellites():
    get_all_satellites()

def poll_projects():
    get_all_projects()

if __name__ == "__main__":
    poll_data()
