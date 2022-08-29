import json
import sys
from collections import OrderedDict


def dump(config, config_path):
    """Shortcut to pretty print json to a file"""
    with config_path.open('w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def load_config(config_path):
    """Loads the json at the given path. Does not error check"""
    if not config_path.exists():
        print("Config file does not exist")
        sys.exit(1)

    with config_path.open() as f:
        return json.load(f)


def first(map):
    """Returns the first element or key of the collection"""
    return next(iter(map))


def check_extension(path, extensions):
    """Check if path has an extension contained in extensions"""
    for ext in extensions:
        if path.suffix == ext:
            return True
    return False


def make_unique_names(files, file_names):
    """Merges directory hierarchy into file names that are duplicates"""
    result = OrderedDict()

    index = 0
    for file in files:
        if len(file_names[file.stem]) == 1:
            result[file.stem] = file.absolute()
        else:
            file_names[file.stem].remove(index)
            new_name = file.parent.name + "_" + file.stem
            result[new_name] = file.absolute()
        index += 1
    return result


def get_files(wp_path, extensions, files=[], file_names=OrderedDict()):
    """Recursively get all files from a starting directory"""
    print("Looking at", wp_path.absolute())
    dirs = []

    index = len(files)
    for entry in wp_path.iterdir():
        if entry.is_dir():
            dirs.append(entry)
        elif entry.is_file():
            if not check_extension(entry, extensions):
                continue
            files.append(entry)
            if entry.stem in file_names.keys():
                file_names[entry.stem].append(index)
                # indicates that this name will always have duplicate names
                file_names[entry.stem].append(True)
            else:
                file_names[entry.stem] = [index]
            index += 1

    for dir in dirs:
        res = get_files(dir.absolute(), extensions, files, file_names)
        files = res[0]
        file_names = res[1]

    return (files, file_names)


def get_wallpapers(wp_path, extensions):
    wallpapers = OrderedDict()
    files = get_files(wp_path, extensions)
    names = make_unique_names(files[0], files[1])
    for name, path in names.items():
        wallpapers[name] = {
            "path": str(path),
            "fit": "maximized",
            "offset": {
                "x": 0,
                "y": 0
            }
        }

    return wallpapers
