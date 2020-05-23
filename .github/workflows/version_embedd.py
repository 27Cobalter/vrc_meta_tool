import os
import re

version = os.environ.get("GITHUB_SHA")
version_number = []
pattern = re.compile('.*v([0-9]+)\.([0-9]+).([0-9]+).')
version_number = re.match(pattern, os.environ.get("GITHUB_REF")).groups()
version_number_str = "{}.{}.{}".format(version_number[0], version_number[1], version_number[2])

print(f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=({version_number[0]}, {version_number[1]}, {version_number[2]}),
    prodvers=({version_number[0]}, {version_number[1]}, {version_number[2]}),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x17,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904b0',
        [StringStruct(u'CompanyName', u'None'),
        StringStruct(u'FileDescription', u'vrc_meta_tool'),
        StringStruct(u'FileVersion', u'{version_number_str}'),
        StringStruct(u'InternalName', u'vrc_meta_tool'),
        StringStruct(u'LegalCopyright', u'Copyright 2020 vrc_meta_tool. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'vrc_meta_tool'),
        StringStruct(u'ProductName', u'vrc_meta_tool'),
        StringStruct(u'ProductVersion', u'{version_number_str}'),
        StringStruct(u'CompanyShortName', u'None'),
        StringStruct(u'ProductShortName', u'vrc_meta_tool'),
        StringStruct(u'LastChange', u'{version}'),
        StringStruct(u'Official Build', u'1')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)''')
