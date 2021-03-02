from urllib import request
from zipfile import ZipFile
from io import BytesIO
from os import makedirs
import re
import argparse
from pathlib import Path

BASE_URL = "https://github.com/numediart/MBROLA-voices/raw/master/data/%s/%s"
MBROLA_FOLDER = Path("/usr/share/mbrola/")

LANG_FILES = {
    'cn': [1],
    'ir': [1],
    'hu': [1],
    'ar': [2, 1],
    'ca': [1, 2],
    'cz': [2, 1],
    'pt': [1],
    'it': [3, 1, 2, 4],
    'nl': [3, 1, 2],
    'fr': [7, 2, 1, 3, 4, 6, 5],
    'cr': [1],
    'mx': [1, 2],
    'ee': [1],
    'en': [1],
    'lt': [2, 1],
    'es': [2, 1, 4, 3],
    'de': [1, 3, 5, 8, 4, 7, 2, 6],
    'us': [1, 3, 2],
    'jp': [2, 3, 1],
    'bz': [1],
    'br': [1, 2, 3, 4],
    'tr': [2, 1],
    'ma': [1],
    'ro': [1],
    'hn': [1],
    'hb': [1, 2],
    'tl': [1],
    'vz': [1],
    'af': [1],
    'id': [1],
    'sw': [2, 1],
    'in': [1, 2],
    'la': [1],
    'gr': [1, 2],
    'nz': [1],
    'ic': [1],
    'pl': [1]
}


def create_folder_and_extract(voice_name, zfile):
    try:
        makedirs(MBROLA_FOLDER + voice_name + "/")
    except FileExistsError:
        pass
    zfile.extract(voice_name, MBROLA_FOLDER + voice_name + "/")


def install_voices(lang="fr"):
    """Automatically downloads and extracts all the voices for one language in the /usr/share/mbrola folder"""
    for voice_id in LANG_FILES[lang]:
        voice_name = lang + str(voice_id)
        print("Downloading MBROLA language file for voice %s" % voice_name)
        voice_data = request.urlopen(BASE_URL %
                                     (voice_name, voice_name)).read()
        # creating folder for the language file
        print("Writing data for language %s" % voice_name)
        voice_folder = MBROLA_FOLDER / Path(voice_name)
        voice_folder.mkdir(parents=True, exist_ok=True)
        lang_path = voice_folder / Path(voice_name)
        with open(str(lang_path), "wb") as lang_file:
            lang_file.write(voice_data)


argparser = argparse.ArgumentParser()
argparser.add_argument("languages",
                       nargs="+",
                       choices=list(LANG_FILES.keys()),
                       type=str,
                       help="Languages to install")
argparser.add_argument("--all",
                       action="store_true",
                       help="Download all language files")

if __name__ == "__main__":
    args = argparser.parse_args()
    if args.all:
        languages = list(LANG_FILES.keys())
    else:
        languages = args.languages
    for lang in languages:
        print("Installing voices for languages %s" % lang)
        install_voices(lang)
