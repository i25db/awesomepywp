import os

import commands
import argparse

from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tracks all wallpaper files in a directory and its subdirectories",
        exit_on_error=False
    )

    parser.add_argument('-D', type=Path, default=os.getcwd(), dest="wp_dir", help="the root wallpaper directory (default: .)")
    parser.add_argument('-C', default="wp.json", dest="config_name", help="the name of the config file (default: wp.json)")

    sub_parsers = parser.add_subparsers(dest="command")

    init_parser = sub_parsers.add_parser("init", help="initiate a new config file")
    init_parser.add_argument('-e', nargs='+', default=[".jpg", ".jpeg", ".png"], dest="extensions", help="list of extensions to accept")

    reset_parser = sub_parsers.add_parser("reset", help="reset the current config file")
    reset_parser.add_argument('-e', nargs='+', default=[".jpg", ".jpeg", ".png"], dest="extensions", help="list of extensions to accept")

    next_parser = sub_parsers.add_parser("next", help="get the path of the next wallpaper")
    curr_parser = sub_parsers.add_parser("curr", help="get the path of the current wallpaper")
    prev_parser = sub_parsers.add_parser("prev", help="get the path of the previous wallpaper")

    offset_parser = sub_parsers.add_parser("offset", help="get or set the offset of the current wallpaper")
    offset_parser.add_argument('-x', type=int, default=0, dest="off_x", help="the x offset increment")
    offset_parser.add_argument('-y', type=int, default=0, dest="off_y", help="the y offset increment")

    fit_parser = sub_parsers.add_parser("fit", help="get or set the fit mode of the current wallpaper")
    fit_parser.add_argument("-f", choices=["maximized", "fit"], default=None, dest="fit_choice")
    fit_parser.add_argument("-c", dest="fit_cycle", help="cycle fit for the current wallpaper")

    settings = parser.parse_args()
    config_path = settings.wp_dir/settings.config_name

    if not settings.command:
        parser.print_help()
    elif settings.command == "init":
        commands.init_config(config_path, settings.extensions)
    elif settings.command == "reset":
        commands.reset_config(config_path, settings.extensions)
    elif settings.command == "next":
        print(commands.cycle_wp(config_path))
    elif settings.command == "curr":
        print(commands.get_curr(config_path))
    elif settings.command == "prev":
        print(commands.cycle_wp(config_path, True))
    elif settings.command == "offset":
        print(commands.set_offset(config_path, settings.off_x, settings.off_y))
    elif settings.command == "fit":
        if settings.fit_cycle:
            print(commands.cycle_fit(config_path))
        else:
            print(commands.set_fit(config_path, settings.fit_choice))
