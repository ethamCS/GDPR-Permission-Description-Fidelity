import sys
import os
import apk_downloader.apkdownloader as apkdl

filename = sys.argv[1]

def download_apks(file_descriptor):
    try:
        app_names = open(filename, 'r')
    except FileNotFoundError:
        msg = f'Error: "{filename}" could not be found'
        sys.exit(msg)
        
    app_names = file_descriptor.splitlines()
    print(app_names)
    for name in app_names:
        apkdl.download_apk(name)


download_apks(filename)


'''
def main():

    if len(sys.argv) < 2:
        print("Usage: python apk_downloader.py filename")
        sys.exit("Error: no filename provided")

    filename = sys.argv[1]

    try:
        app_ids_fd = open(filename, 'r')
    except FileNotFoundError:
        msg = f'Error: "{filename}" could not be found'
        sys.exit(msg)

    try:
        os.mkdir("./apks")
    except OSError:
        pass 

    download_apks(app_ids_fd)

    app_ids_fd.close()

if __name__ == '__main__':
    main()
'''