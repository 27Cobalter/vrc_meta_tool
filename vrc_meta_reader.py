import datetime
import glob
import os
import psutil
import re
import sys


def chunk_iter(data):
    total_length = len(data)
    end = 4

    while end + 8 < total_length:
        length = int.from_bytes(data[end + 4 : end + 8], "big")
        chunk_type = end + 8
        chunk_data = chunk_type + 4
        end = chunk_data + length

        yield (data[chunk_type:chunk_data], data[chunk_data:end])

def end():
    for p in psutil.process_iter(attrs=["pid", "name"]):
        if p.info["pid"] == os.getpid():
            if p.info["name"] != "vrc_meta_reader.exe":
                break
            print("\n\nEnterを押して終了")
            input()


def main(args):
    if len(args) == 1:
        print("Usage: vrc_meta_reader.py  file\r\n"
              "       vrc_meta_reader.py  file  user_name\r\n"
              "\r\n"
              "vrc_meta_reader.exeに画像ファイルをドラッグアンドドロップしてください")
        end()
        return
    files = []
    user_name = ""
    if os.path.isdir(args[1]):
        files = glob.glob(os.path.join(args[1], "*.png"))
    else:
        files.append(args[1])

    if len(args) == 3:
        user_name = args[2]

    for image_path in files:
        with open(image_path, "rb") as image:
            data = image.read()

        if data[:8] != b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A":
            continue
        if user_name == "":
            print(image_path)
            print("-" * 80, "chunks of: %s" % image_path, "-" * 80, sep="\n")

            for chunk_type, chunk_data in chunk_iter(data):
                if chunk_type == b"vrCu":
                    print("User:", chunk_data.decode())
                elif chunk_type == b"vrCd":
                    print(
                        "Date:",
                        datetime.datetime.strptime(
                            chunk_data.decode()[:-3], "%Y%m%d%H%M%S"
                        ),
                    )
                elif chunk_type == b"vrCw":
                    print("World:", chunk_data.decode())
        else:
            for chunk_type, chunk_data in chunk_iter(data):
                if chunk_type == b"vrCu":
                    user = chunk_data.decode()
                    if user_name in user:
                        print(image_path)
                        print(user)
    end()


if __name__ == "__main__":
    main(sys.argv)
