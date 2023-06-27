import datetime
import sys
from struct import pack
from zlib import crc32


class MetaData:
    FORMAT_DATE_USER_INPUT = "%Y-%m-%d %H:%M:%S"
    FORMAT_DATE_RAW_DATA = "%Y%m%d%H%M%S"

    def __init__(self):
        self.date = ""
        self.photographer = ""
        self.world = ""
        self.users = []
        # PNG ファイルシグネチャ
        self.other_data = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"

    def validate_date_format(self, str_date):
        try:
            datetime.datetime.strptime(str_date, self.FORMAT_DATE_USER_INPUT)
            return True
        except ValueError:
            return False

    def update_date(self, strdate):
        date = datetime.datetime.strptime(strdate, self.FORMAT_DATE_USER_INPUT)
        strdate = datetime.datetime.strftime(date, self.FORMAT_DATE_RAW_DATA) + "000"
        self.date = strdate

    def update_photographer(self, photographer):
        self.photographer = photographer

    def update_world(self, world):
        self.world = world

    def add_user(self, user):
        self.users.append(user)

    def update_user(self, index, vrcname, twitterid):
        user = self.users[index].rsplit(" : ", 1)

        # vrcnameまたはtwitteridが空文字のときは変更しない
        if vrcname != "":
            user[0] = vrcname
        if twitterid != "":
            if len(user) == 1:
                user.append(twitterid)
            else:
                user[1] = twitterid

        self.users[index] = " : ".join(user)

    def delete_users(self, delete_indexes):
        deleted_user = []

        for i in reversed(delete_indexes):
            deleted_user.append(self.users.pop(i))

        # 削除したユーザをリスト順で出したい
        return reversed(deleted_user)

    def sort_users(self):
        self.users.sort()

    def print_users(self):
        for i, user in enumerate(self.users):
            print("{0:2d} {1:s}".format(i, user))

    def print(self):
        print("-" * 80)
        print(
            "Date:",
            datetime.datetime.strptime(self.date[:-3], self.FORMAT_DATE_RAW_DATA),
        )
        print("Photographer:", self.photographer)
        print("World:", self.world)
        for user in self.users:
            print("User:", user)
        print("-" * 80)


class ChunkUtils:
    # pngチャンク関連関数
    def chunk_iter(self, data):
        total_length = len(data)
        end = 4

        while end + 8 < total_length:
            length = int.from_bytes(data[end + 4 : end + 8], "big")
            chunk_type = end + 8
            chunk_data = chunk_type + 4
            end = chunk_data + length

            yield (data[chunk_type:chunk_data], data[chunk_data:end])

    def chunk(self, name, data):
        return pack("!I4s%dsI" % len(data), len(data), name, data, crc32(name + data))

    def write(self, file_name, metadata):
        metadata.users.sort()

        with open(file_name, "w+b") as f:
            f.write(metadata.other_data)
            f.write(self.chunk(b"vrCd", metadata.date.encode("utf-8")))
            f.write(self.chunk(b"vrCp", metadata.photographer.encode("utf-8")))
            f.write(self.chunk(b"vrCw", metadata.world.encode("utf-8")))
            for user in metadata.users:
                f.write(self.chunk(b"vrCu", user.encode("utf-8")))
            f.write(self.chunk(b"IEND", b""))


def parse_number(user_input, length):
    words = user_input.split()
    exclude_indexes = set()

    for word in words:
        invert = False

        # 先頭が^なら否定
        if word[0] == "^":
            invert = True
            word = word[1:]

        ranges = word.split("-", 1)
        num1 = int(ranges[0])
        num2 = num1

        if len(ranges) == 2:
            num2 = int(ranges[1])
            if num1 > num2:
                num1, num2 = num2, num1

        indexes = set(range(num1, num2 + 1))
        if invert:
            indexes = set(range(length)) - indexes

        exclude_indexes = exclude_indexes | indexes

    # 範囲超えないように
    exclude_indexes = exclude_indexes & set(range(length))
    exclude_indexes = sorted(exclude_indexes)

    return exclude_indexes


def main(args):
    if len(args) == 1:
        print("Usage: vrc_meta_editor.py file\r\n")
        return

    image_path = args[1]
    data = None
    metadata = MetaData()
    chunkutils = ChunkUtils()

    with open(image_path, "rb") as f:
        data = f.read()
        assert data[:8] == b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"

    # 画像のデータをmetadataに変換
    for chunk_type, chunk_data in chunkutils.chunk_iter(data):
        if chunk_type == b"vrCd":
            metadata.date = chunk_data.decode("utf-8")
        elif chunk_type == b"vrCp":
            metadata.update_photographer(chunk_data.decode("utf-8"))
        elif chunk_type == b"vrCw":
            metadata.update_world(chunk_data.decode("utf-8"))
        elif chunk_type == b"vrCu":
            metadata.add_user(chunk_data.decode("utf-8"))
        elif chunk_type != b"IEND":
            # vrc_meta_toolで使っていないチャンクはIENDを除いてそのまま保存
            metadata.other_data = metadata.other_data + chunkutils.chunk(
                chunk_type, chunk_data
            )

    metadata.sort_users()
    metadata.print()

    while True:
        mode = input("Add/Update/Delete/Print/Quit [a/u/d/p/q] ")
        if len(mode) == 0:
            continue

        mode_initial = mode[0].lower()
        if mode_initial == "a":
            # ユーザ追加
            vrcname = input("VRCName: ")
            if vrcname == "":
                continue
            twitterid = input('TwitterId: (eg:"@Twitter")(optional): ')
            user_name = vrcname
            if twitterid != "":
                user_name = vrcname + " : " + twitterid
            metadata.add_user(user_name)
            metadata.sort_users()
            chunkutils.write(image_path, metadata)

        elif mode_initial == "u":
            item = input("Date/Photographer/World/VRCName/TwitterID [d/p/w/v/t] ")
            if len(item) == 0:
                continue

            item_initial = item[0].lower()
            if item_initial == "d":
                # 撮影日時変更
                valid = False
                while not valid:
                    date = input('New Date(eg: "2018-05-10 18:52:00": ')
                    valid = metadata.validate_date_format(date)
                    if not valid:
                        print("invalid date format. expected YYYY-MM-DD HH:mm:ss")

                metadata.update_date(date)

                chunkutils.write(image_path, metadata)

            elif item_initial == "p":
                # 撮影者変更
                photographer = input("New Photographer: ")
                metadata.update_photographer(photographer)

                chunkutils.write(image_path, metadata)

            elif item_initial == "w":
                # 撮影ワールド変更
                world = input("New World: ")
                metadata.update_world(world)

                chunkutils.write(image_path, metadata)

            elif item_initial == "v":
                # VRCNameの変更
                metadata.print_users()
                index = input("Select user: ")
                user_name = input("New VRCName: ")
                metadata.update_user(int(index), user_name, "")
                metadata.sort_users

                chunkutils.write(image_path, metadata)

            elif item_initial == "t":
                # TwitterIDの変更
                metadata.print_users()
                index = input("Select user: ")
                twitterid = input('New TwitterID: (eg:"@Twitter"):')
                metadata.update_user(int(index), "", twitterid)

                chunkutils.write(image_path, metadata)

        elif mode_initial == "d":
            # ユーザ削除
            metadata.print_users()
            user_input = input('Select User (eg:"1 2 3", "1-3", "^4"): ')
            # 削除するインデックスの配列
            delete_indexes = parse_number(user_input, len(metadata.users))
            deleted_user = metadata.delete_users(delete_indexes)

            for user in deleted_user:
                print("delete :", user)

            chunkutils.write(image_path, metadata)

        elif mode in {"p", "P", "print", "Print"}:
            metadata.print()

        elif mode in {"q", "Q", "quit", "Quit"}:
            break


if __name__ == "__main__":
    main(sys.argv)
