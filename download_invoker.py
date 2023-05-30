import sys
import apk_downloader.apkdownloader as apkdl

def download_apks(file_descriptor):
    app_names = file_descriptor.read().splitlines()
    for name in app_names:
        apkdl.download_apk(name)

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

    download_apks(app_ids_fd)

    app_ids_fd.close()

if __name__ == '__main__':
    main()