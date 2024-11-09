from .lib.misp import Mispao

import os
import configparser
import argparse
from pathlib import Path

KEY_PATH = os.path.join(os.path.expanduser("~"), '.mispao.ini')

def save_data(key:str, url:str):
    config = configparser.ConfigParser()
    config['API'] = {'key': key, 'url': url}
    with open(KEY_PATH, 'w') as configfile:
        config.write(configfile)

def main():
    # Start with date arguments
    parser = argparse.ArgumentParser(description='Viriback C2 data to MISP events')

    r_init = True
    if Path(KEY_PATH).exists():
        r_init = False

    parser.add_argument('-i', '--init', action='store_true', dest='init', required=r_init, help="First step. Pass your API key and URL.")
    parser.add_argument('-u', '--update', action='store_true', dest='update', help="Update MISP events.")
    parser.add_argument('-d', '--distribution', choices=[0,1,2,3,4], dest='distribution', default=0, help="""The common distribution levels in MISP are as follows:
        0: Your organization only - Default;
        1: This community only;
        2: Connected communities;
        3: All communities;
        4: Sharing group.""")

    args = parser.parse_args()
    if not args:
        exit()
    else:
        if args.init:
            key = input('Enter your key:')
            url = input('Enter your MISP url:')
            save_data(key, url)
            print(f"Saved data")
        elif args.update:
            config = configparser.ConfigParser()
            try:
                config.read(KEY_PATH)
                key = config['API']['key']
                url = config['API']['url']
                Mispao(url, key, args.distribution)
            except Exception as err:
                print("Run init command first - API key and URL were not found or is not correct")
                exit()

if __name__ == "__main__":
    main()