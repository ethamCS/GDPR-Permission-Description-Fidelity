import sys
import os
import apk_downloader.apkdownloader as apkdl

# def download_apks(file_descriptor):
#     app_names = file_descriptor.readlines()
#     for name in app_names:
#         apkdl.download_apk(name)
#         print(name)


# file = open("./app_qualified_names2.txt", 'r')

# download_apks(file)
apkdl.down("homeworkout.homeworkouts.noequipment")