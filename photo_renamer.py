#!/usr/bin/env python3

import datetime
import os
import pprint
from pathlib import Path

import click

PHOTO_PREFIX = "DSC"

PP = pprint.PrettyPrinter(indent=4)

def print_photos(list_1 : list, list_2 : list, prefix : str = ""):
    

    if prefix != "":
        list_1_w_prefix = [f"{prefix}/{element}" for element in list_1]
    else:
        list_1_w_prefix = list_1

    to_print = [photo_data for photo_data in zip(list_1_w_prefix, list_2)]
    PP.pprint(to_print)

def get_photos(folder : Path) -> list[Path]:
    photos = os.listdir(folder)
    return [photo for photo in photos if photo.startswith(PHOTO_PREFIX)]

def get_photos_modification_time(photos: list[Path], folder : Path):
    return [datetime.datetime.fromtimestamp(os.path.getmtime(folder/photo)) for photo in photos]

def rename_photo(old_name, new_name, folder : Path):
    if os.path.isfile(folder / new_name):
        return (1, folder / new_name)
    else:
        print(f"Renaming {old_name} to {new_name}")
        os.rename(folder/old_name, folder/new_name)
        return (0, None)

def rename_photos(photos : list[Path], m_times: list[datetime.datetime], folder : Path):
    print(f"Renaming photos in {folder}")

    prefixes = [f"{time.year}_{time.month}_{time.day}_{time.hour}_{time.minute}_{time.second}" for time in m_times]
    new_names = [f"{prefix}_{photo}" for prefix, photo in zip(prefixes, photos)]

    res = [rename_photo(old_name, new_name, folder) for old_name, new_name in zip(photos, new_names)]
    res_stat, err = zip(*res)

    if sum(res_stat) != 0:
        print("The following photos could not be renamed because they already exist:")
        err_photos = [err_photo for err_photo in err if err_photo != None]
        PP.pprint(err_photos)
        return 1
    
    return 0

@click.command()
@click.option('--folder', prompt='Select folder', help='Folder that contains photos that you want to rename.')
def main(folder: Path):
    folder = Path(folder)

    photos = get_photos(folder)

    if len(photos) == 0:
        print("No photos selected for renaming.")
        return 0

    m_times = get_photos_modification_time(photos, folder)

    res = rename_photos(photos, m_times, folder)
    print(f"Photo manager ended with result {res}")

if __name__ == "__main__":
    main()
    
    