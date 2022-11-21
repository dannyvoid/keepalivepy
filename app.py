import time
import subprocess
import psutil
import pathlib
import cursor
import os
import tomli

current_dir = pathlib.Path(__file__).parent.absolute()
os.chdir(current_dir)

with open("config.toml", "rb") as f:
    try:
        config = tomli.load(f)

    except tomli.TOMLDecodeError as e:
        print(e)
        print("config.toml is invalid")
        input("Press enter to exit...")
        exit(1)

apps = config["user"]["apps"]
wait_mins = config["user"]["wait_mins"]


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        msg = "Checking again in {}".format(timer)
        print(msg, end="\r")
        time.sleep(1)
        t -= 1


def check_status(executable):
    exe = pathlib.Path(executable).name
    for proc in psutil.process_iter():
        if exe in proc.name():
            msg = "[OK] {} is running"
            print(msg.format(exe))
            return True

    msg = "[ERROR] {} is not running"
    print(msg.format(exe))
    return False


def start_app(executable):
    exe = pathlib.Path(executable).name
    try:
        subprocess.Popen(executable)

    except Exception as e:
        msg = "[ERROR]: {}"
        print(msg.format(e))

    finally:
        msg = "[OK] {} is started"
        print(msg.format(exe))


def stop_app(executable):
    exe = pathlib.Path(executable).name

    try:
        for proc in psutil.process_iter():
            if exe in proc.name():
                proc.kill()

    except Exception as e:
        msg = "[ERROR]: {}"
        print(msg.format(e))

    finally:
        msg = "[OK] {} is stopped"
        print(msg.format(exe))


def main():
    while True:
        os.system("cls")

        for app in apps:

            if pathlib.Path(app).exists():
                if not check_status(app):
                    start_app(app)
            else:
                msg = "[ERROR] {} does not exist"
                print(msg.format(app))

        msg = "Waiting {} seconds before checking again..."
        countdown(wait_mins * 60)


if __name__ == "__main__":
    try:
        cursor.hide()
        main()
    except KeyboardInterrupt:
        cursor.show()
        print("Exiting..." + " " * 20, end="\r")
