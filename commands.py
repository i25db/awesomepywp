import utils
from pathlib import Path


def init_config(config_path, extensions):
    """Creates or resets the wallpaper config file"""
    if config_path.exists():
        print("Config file already exists")
        return

    wp_path = Path(str(config_path.parent))

    config = {
        "curr_wp": "",
        "wallpapers": utils.get_wallpapers(wp_path, extensions)
    }

    if len(config["wallpapers"]) > 0:
        config["curr_wp"] = utils.first(config["wallpapers"])

    utils.dump(config, config_path)


def reset_config(config_path, extensions):
    """Resets the wallpaper config file after confirmation"""
    if not config_path.exists():
        init_config(config_path, extensions)
        return

    check = input("Are you sure you want to reset the wallpaper config file? (yes, no):")
    if not any(check.lower() == r for r in ["yes", "y"]):
        return

    config_path.unlink(True)

    init_config(config_path, extensions)


def update_config(config_path):
    print("Not implemented yet")


def get_path(config):
    return config["wallpapers"][config["curr_wp"]]["path"]


def get_curr(config_path):
    return get_path(utils.load_config(config_path))


def cycle_wp(config_path, prev=False):
    config = utils.load_config(config_path)
    wallpapers = list(config["wallpapers"])

    if prev:
        wallpapers = reversed(wallpapers)

    # if the last element is the current wallpaper
    found = False

    for i, wp in enumerate(wallpapers):
        if found:
            config["curr_wp"] = wp
            utils.dump(config, config_path)
            return get_path(config)
        found = wp == config["curr_wp"]

    # if we reach this point the only option is we need to loop
    config["curr_wp"] = wallpapers[0]
    utils.dump(config, config_path)
    return get_path(config)


def get_offset(config):
    offset = config["wallpapers"][config["curr_wp"]]["offset"]
    return str(offset["x"]) + " " + str(offset["y"])


def set_offset(config_path, x=0, y=0):
    config = utils.load_config(config_path)

    config["wallpapers"][config["curr_wp"]]["offset"]["x"] += x
    config["wallpapers"][config["curr_wp"]]["offset"]["y"] += y

    utils.dump(config, config_path)
    return get_offset(config)


def get_fit(config):
    return config["wallpapers"][config["curr_wp"]]["fit"]


def set_fit(config_path, fit=None):
    config = utils.load_config(config_path)

    if not fit:
        return get_fit(config)

    config["wallpapers"][config["curr_wp"]]["fit"] = fit
    utils.dump(config, config_path)
    return fit


def cycle_fit(config_path):
    config = utils.load_config(config_path)
    fit = ""

    if config["wallpapers"][config["curr_wp"]]["fit"] == "fit":
        config["wallpapers"][config["curr_wp"]]["fit"] = "maximized"
        fit = "maximized"
    else:
        config["wallpapers"][config["curr_wp"]]["fit"] = "fit"
        fit = "fit"

    utils.dump(config, config_path)
    return fit
