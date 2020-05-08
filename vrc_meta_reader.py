import datetime
import os
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


def main(args):
    image_path = args[1]
    print(image_path)
    with open(image_path, "rb") as image:
        data = image.read()

    assert data[:8] == b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    print("-" * 80, "chunks of: %s" % image_path, "-" * 80, sep="\n")

    for chunk_type, chunk_data in chunk_iter(data):
        if chunk_type == b"vrCu":
            print("User:", chunk_data.decode())
        if chunk_type == b"vrCd":
            print("Date:", datetime.datetime.strptime(chunk_data.decode()[:-3], '%Y%m%d%H%M%S'))
        elif chunk_type == b"vrCw":
            print("World:", chunk_data.decode())


if __name__ == "__main__":
    main(sys.argv)
