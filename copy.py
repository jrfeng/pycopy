import json
import sys
import os
import shutil


def read_config(config_file: str):
    if not os.path.exists(config_file):
        print("[error]not find config file.")
        return

    with open(config_file, encoding="utf-8") as config:
        return json.loads(config.read())


def check_config(config: dict):
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
    except KeyError:
        print("[error]config file format error.")
        return False

    return True


def check_or_create_dir(parent_dir: str, child_dir: str):
    if not os.path.exists(parent_dir + "/" + child_dir):
        print("create dir:", child_dir)
        os.mkdir(parent_dir + "/" + child_dir)


def copy_all_files(input_dir: str, output_dir: str):
    count = 0;
    for f in os.scandir(input_dir):
        if os.path.isfile(f):
            print_copy_message(f.name, output_dir)
            shutil.copy(f, output_dir)
            count += 1
    print("    count:", count)


def file_exists(parent_dir: str, file_name: str):
    return os.path.exists(parent_dir + "/" + file_name)


def print_copy_message(file_name: str, output_dir: str):
    message = "    copy: " + file_name

    if file_exists(output_dir, file_name):
        message += " [override]"
    else:
        message += " [new]"

    print(message)


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

    print("input  dir:", input_dir)
    print("output dir:", output_dir)

    for key, value in dir_maps.items():
        check_or_create_dir(output_dir, value)
        print("[", key, " -> ", value, "]", sep="")
        copy_all_files(input_dir + "/" + key, output_dir + "/" + value)


if __name__ == "__main__":
    main()
