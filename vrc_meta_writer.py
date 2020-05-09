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
        # VRChatが悪い
        if line == "\n" or line == "\r\n":
            continue
        line = line.rstrip("\n").rstrip("\r")
        yield line


class LogToolBase:
    def init():
        pass

    def execute(line):
        pass


# 本体
class VrcMetaTool(LogToolBase):
    config = []
    events = {}
    world = ""
    users = []
    photo_date_regex = re.compile(
        ".*VRChat_[0-9]*x[0-9]*_([0-9]{4})-([0-9]{2})-([0-9]{2})_([0-9]{2})-([0-9]{2})-([0-9]{2}).([0-9]{3}).png"
    )
    log_date_regex = re.compile(
        "([0-9]{4}\.[0-9]{2}\.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) .*?"
    )

    def __init__(self, config):
        os.makedirs(config["out_dir"], exist_ok=True)
        self.config = config

        self.events["PlayerJoin"] = "[NetworkManager] OnPlayerJoined "
        self.events["PlayerLeft"] = "[NetworkManager] OnPlayerLeft "
        self.events["EnterRoom"] = ".[RoomManager] Entering Room: "
        self.events["ScreenShot"] = "Took screenshot to: "

    def execute(self, line):
        for event in self.events:
            index = line.find(self.events[event])
            if index != -1:
                body = line[index + len(self.events[event]) :]
                print(
                    self.log_date_regex.match(line).group(1), "\t" + event + ": " + body
                )
                if event == "PlayerJoin":
                    self.users.append(body)
                elif event == "PlayerLeft":
                    self.users.remove(body)
                elif event == "EnterRoom":
                    self.world = body
                    self.users = []
                elif event == "ScreenShot":
                    if not os.path.exists(body):
                        print("\tError", os.path.abspath(body), "is not found.")
                        return
                    date = "".join(self.photo_date_regex.match(body).groups())
                    if not self.write(body, "".join(date)):
                        return

                    print(
                        "\tWrite:",
                        body,
                        "\n\t\t->",
                        os.path.abspath(
                            os.path.join(self.config["out_dir"], os.path.basename(body))
                        ),
                    )
                    print("\t", date, self.world)
                    print("\t", self.users)

    # pngチャンク関連関数
    def has_meta(self, image):
        total_length = len(image)
        end = 4
        while end + 8 < total_length:
            length = int.from_bytes(image[end + 4 : end + 8], "big")
            chunk_type = end + 8
            chunk_data = chunk_type + 4
            end = chunk_data + length
            if image[chunk_type:chunk_data] == b"vrCd":
                return True
        return False

    def chunk(self, name, data):
        return pack("!I4s%dsI" % len(data), len(data), name, data, crc32(name + data))

    def write(self, file, date):
        self.users.sort()
        if not os.path.samefile(os.path.dirname(file), self.config["out_dir"]):
            shutil.copy2(os.path.abspath(file), self.config["out_dir"])
        with open(
            os.path.join(self.config["out_dir"], os.path.basename(file)), "r+b"
        ) as f:
            image = f.read()
            assert image[:8] == b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
            if self.has_meta(image):
                print(file, "already has meta data")
                return False

            # IEND以降を上書きする
            f.seek(-12, 2)
            f.write(self.chunk(b"vrCd", date.encode("utf-8")))
            f.write(self.chunk(b"vrCw", self.world.encode("utf-8")))
            for user in self.users:
                f.write(self.chunk(b"vrCu", user.encode("utf-8")))
            f.write(self.chunk(b"IEND", b""))
            return True


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
