from aws_studio import * 
from start_chrome import start
import random
from time import sleep
import subprocess
from xdotool_commands import * 
import subprocess
import os
import argparse
from argparse import ArgumentError
from titles_db import titles 
# from titles_db_sandeep import titles 

# from ytdeb.main import yt_engine
from ytdeb_content.main import yt_engine


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--acc",
        dest="acc",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-z",
        "--slot",
        dest="slot",
        type=str,
        required=True,
    ) 
    
    parser.add_argument(
        "-y",
        "--target_url",
        dest="target_url",
        type=str,
        required=True,
    ) 

    # parser.add_argument(
    #     "-a",
    #     "--type_content",
    #     dest="type_content",
    #     type=str,
    #     required=True,
    # ) 
    return parser


def setup_chrome_acc(_acc, target_url):
    _lor = target_url
    _target = f"{_lor}{_acc}.zip" 

    subprocess.run(f"sudo wget --directory-prefix=/home/circleci/project/ {_target}", shell=True)
    sleep(2)
    subprocess.run(f"unzip -q /home/circleci/project/chrome_data_{_acc}.zip -d /home/circleci/project/", shell=True)
    sleep(2)

    # initial start
    start()
    sleep(10)
    subprocess.run("sudo killall chrome", shell=True)
    sleep(3)

    subprocess.run("sudo rm -r /root/.config/google-chrome/Default", shell=True)
    sleep(3)
    subprocess.run("sudo mv /home/circleci/project/root/.config/google-chrome/Default /root/.config/google-chrome/", shell=True)
    sleep(3)


def upload():
    ts = titles
    parser = get_arg_parser()
    args = parser.parse_args()

    _acc = args.acc
    _slot = args.slot
    target_url = args.target_url

    # setting up chrome data folder
    setup_chrome_acc(_acc, target_url)

    # subprocess.run("sudo rm /root/*.mp4", shell=True)

    if _slot == "day":
        ss = ["01:00", "03:00", "06:00", "09:00", "07:00", "08:00"]
        # ss = ["05:00", "07:00"]
        # ss = ["05:00"]
    else: 
        ss = ["13:00", "15:00", "18:00", "21:00", "19:00", "20:00"]

    # Generate content 
    for i in ss:
        yt_engine()
        sleep(5)

    # Starting chrome...
    start()

    sleep(5)
    # scrot_()
    close_all_popups()
    make_chrome_default()
    # # scrot_()
    
    for i in ss:
        print(f"Uploading {ss.index(i) + 1} of shorts...")
        tss = random.choice(ts) 
        _title = tss + " #shorts #trending"

        _time = i
        _date = None
        _item = ss.index(i)

        studio_main(_title, _time, _date, _item)
        sleep(8)
     
def main():
    # subprocess.run("sudo su -", shell=True)
    # Uploading short
    upload()

    # Updating the slot
    print("Process completed.")


if __name__ == "__main__":
    main()