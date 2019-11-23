import json
import sys
import os
import shutil


def read_config(config_file):
    if not os.path.exists(config_file):
        print("[error]not find config file.")
        return

    with open(config_file, encoding="utf-8") as config:
        return json.loads(config.read())


def check_config(config):
    try:
        if config is None:
            return False

        if not os.path.exists(config["input_dir"]):
            print("[error]input_dir not exists.")
            return False

        if not os.path.exists(config["output_dir"]):
            print("[error]output_dir not exists.")
            return False

        dir_maps = config["dir_maps"]
        if not isinstance(dir_maps, dict):
            print("[error]dir_maps not a json object.")
            return False

        input_dir = config["input_dir"]
        for key, _ in dir_maps.items():
            if not os.path.exists(input_dir + "/" + key):
                print("[error]", key, "not exists.")
                return False
    except json.KeyError as err:
        print("[error]config file format error.")
        return False

    return True


def check_or_create_dir(parent_dir, child_dir):
    if not os.path.exists(parent_dir + "/" + child_dir):
        print("create dir:", child_dir)
        os.mkdir(parent_dir + "/" + child_dir)


def copy_all_files(input_dir, output_dir):
    for f in os.scandir(input_dir):
        if os.path.isfile(f):
            print("    copy:", f.name)
            shutil.copy(f, output_dir)


def main():
    config_file = "copy_config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    config = read_config(config_file)

    if not check_config(config):
        return

    input_dir = config["input_dir"]
    output_dir = config["output_dir"]
    dir_maps = config["dir_maps"]

    for key, value in dir_maps.items():
        check_or_create_dir(output_dir, value)
        print("[", key, " -> ", value, "]", sep="")
        copy_all_files(input_dir + "/" + key, output_dir + "/" + value)


if __name__ == "__main__":
    main()
