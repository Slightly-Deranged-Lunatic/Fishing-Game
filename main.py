import contextlib
import os
import datetime
import logging

if not os.path.exists("Logs"):
    os.mkdir("Logs")
logging.basicConfig(
    filename=f"Logs/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log",
    encoding="utf-8",
    filemode="w",
    format="{asctime} - {levelname} - {message}",
    style="{",
)

def main():
    clear_logs()

def clear_logs():
    # Clears all but 5 most recent logs
    with(contextlib.chdir("Logs")):
        files = os.listdir()
        files.sort()
        files.reverse()
        FILES_TO_REMOVE = files[5:]
        for file in FILES_TO_REMOVE:
            os.remove(file)
        logging.info("Logs cleaned")

if __name__ == "__main__":
    main()