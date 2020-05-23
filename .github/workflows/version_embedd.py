import os

version = os.environ.get("GITHUB_SHA")

print(f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    # filevers=({version}),
    # prodvers=({version}),
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
        StringStruct(u'FileVersion', u'{version}'),
        StringStruct(u'InternalName', u'vrc_meta_tool'),
        StringStruct(u'LegalCopyright', u'Copyright 2020 vrc_meta_tool. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'vrc_meta_tool'),
        StringStruct(u'ProductName', u'vrc_meta_tool'),
        StringStruct(u'ProductVersion', u'{version}'),
        StringStruct(u'CompanyShortName', u'None'),
        StringStruct(u'ProductShortName', u'vrc_meta_tool'),
        StringStruct(u'LastChange', u'{version}'),
        StringStruct(u'Official Build', u'1')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)''')
