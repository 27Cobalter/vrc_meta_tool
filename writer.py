import os
import ctypes
import shutil
import glob
from sys import stdout
from struct import pack
from zlib import crc32, compress


def chunk(name, data):
    return pack("!I4s%dsI" % len(data), len(data), name, data, crc32(name + data))


def write(file, out_dir, date, world, users):
    users.sort()
    shutil.copy2(file, out_dir)
    with open(os.path.join(out_dir,os.path.basename(file)), "r+b") as f:
        # IEND以降を上書きする
        f.seek(-12, 2)
        f.write(chunk(b"vrCd", date))
        f.write(chunk(b"vrCw", world))
        for user in users:
            f.write(chunk(b"vrCu", user))
        f.write(chunk(b"IEND", b""))

def select_log():
    vrc_dir = os.environ["USERPROFILE"] + "\\AppData\\LocalLow\\VRChat\\VRChat\\"
    log_files = glob.glob(vrc_dir + "output_log_*.txt")
    log_files.sort(key = os.path.getctime, reverse = True)
    return log_files[0]

def tail(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.5)
            continue
        line = line.rstrip("\n").rstrip("\r")
        if line != "":
            yield line


def main():
    out_dir = "chunk"
    #photo_reg = re.compile()
    log_file = select_log()
    with open(log_file, "rb") as f:
        print("open logfile : ", log_file)

    lines = tail(f)

    date = b"2019-09-29_13-17-05.189"
    world = b"Pandora ep.3"
    users = []
    users.append(b"bootjp")
    users.append(b"27Cobalter")
    write("./orig/VRChat_1920x1080_2019-09-29_13-17-05.189.png", out_dir, date, world, users)


if __name__ == "__main__":
    main()
