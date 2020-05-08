import datetime
import glob
import os
import re
import shutil
import time
import yaml

from struct import pack
from zlib import crc32

# ログツール関連共通化したい
def select_log():
    vrc_dir = os.environ["USERPROFILE"] + "\\AppData\\LocalLow\\VRChat\\VRChat\\"
    log_files = glob.glob(vrc_dir + "output_log_*.txt")
    log_files.sort(key=os.path.getctime, reverse=True)
    return log_files[0]


def tail(thefile):
    # thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.5)
            continue
        line = line.rstrip("\n").rstrip("\r")
        if line != "":
            yield line


class LogToolBase:
    def init():
        pass

    def execute(line):
        pass


# 本体
class VrcMetaTool(LogToolBase):
    config = []
    regex = {}
    world = ""
    users = []
    date_regex = ""

    def __init__(self, config):
        os.makedirs(config["out_dir"], exist_ok=True)
        self.config = config

        self.regex["PlayerJoin"] = re.compile(
            ".*?\[NetworkManager\] OnPlayerJoined (.*)"
        )
        self.regex["PlayerLeft"] = re.compile(".*?\[NetworkManager\] OnPlayerLeft (.*)")
        self.regex["EnterRoom"] = re.compile(".*?\[RoomManager\] Entering Room: (.*)")
        self.regex["ScreenShot"] = re.compile(".*?Took screenshot to: (.*)")

        self.date_regex = re.compile(
            ".*VRChat_[0-9]*x[0-9]*_([0-9]{4})-([0-9]{2})-([0-9]{2})_([0-9]{2})-([0-9]{2})-([0-9]{2}).([0-9]{3}).png"
        )

    def execute(self, line):
        for event in self.regex:
            match = self.regex[event].match(line)
            if match:
                print(datetime.datetime.now(), "\t" + event + ": " + match.group(1))
                if event == "PlayerJoin":
                    self.users.append(match.group(1))
                elif event == "PlayerLeft":
                    self.users.remove(match.group(1))
                elif event == "EnterRoom":
                    self.world = match.group(1)
                    self.users = []
                elif event == "ScreenShot":
                    if not os.path.exists(match.group(1)):
                        print(
                            "\tError", os.path.abspath(match.group(1)), "is not found."
                        )
                        return
                    date = "".join(self.date_regex.match(match.group(1)).groups())
                    self.write(match.group(1), "".join(date))

                    print(
                        "\tWrite:",
                        match.group(1),
                        "\n\t\t->",
                        os.path.abspath(
                            os.path.join(
                                self.config["out_dir"], os.path.basename(match.group(1))
                            )
                        ),
                    )
                    print("\t", date, self.world)
                    print("\t", self.users)

    # pngチャンク関連関数
    def chunk(self, name, data):
        return pack("!I4s%dsI" % len(data), len(data), name, data, crc32(name + data))

    def write(self, file, date):
        self.users.sort()
        shutil.copy2(os.path.abspath(file), self.config["out_dir"])
        with open(
            os.path.join(self.config["out_dir"], os.path.basename(file)), "r+b"
        ) as f:
            # IEND以降を上書きする
            f.seek(-12, 2)
            f.write(self.chunk(b"vrCd", date.encode("utf-8")))
            f.write(self.chunk(b"vrCw", self.world.encode("utf-8")))
            for user in self.users:
                f.write(self.chunk(b"vrCu", user.encode("utf-8")))
            f.write(self.chunk(b"IEND", b""))


def main():
    config = []
    with open("config.yml", "r") as conf:
        config = yaml.load(conf, Loader=yaml.SafeLoader)

    log_file = config["log_file"]
    if log_file == "":
        log_file = select_log()

    vrc_meta_tool = VrcMetaTool(config)

    with open(log_file, "r", encoding="utf-8") as f:
        print("open logfile : ", log_file)

        lines = tail(f)
        for line in lines:
            vrc_meta_tool.execute(line)


if __name__ == "__main__":
    main()
