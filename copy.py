'''
功能: 复制指定目录下某些子目录中的子文件到另一个目录中。

使用说明: 需要在脚本目录下创建一个名为 'copy_config.json' 的配置文件。或者在执行脚本时使用
一个参数来指定配置文件的路径。

'config.json' 配置文件格式:

{
    "input_dir": <string>,
    "output_dir": <string>,
    "dir_maps": <map>
}

字段说明：

* input_dir: 输入目录，字符串类型。这个目录通常是 Illustrator 的导出目录。
* output_dir: 输出目录，字符串类型。这个目录通常是 Android 项目的 res 目录。
* dir_maps: 目录映射，map 类型。每个 key 都表示 input_dir 的一个子目录，value 都表示 
            output_dir 下的一个子目录。key 目录下的所有文件都会被复制到其 value 值对
            应的目录下。

例：

{
    "input_dir": "C:/test/input_dir",
    "output_dit": "C:/my_android/app/src/main/res",
    "dir_maps": {
        "0.5x": "mipmap-mdpi",
        "0.75x": "mipmap-hdpi",
        "1x": "mipmap-xhdpi",
        "1.75x": "mipmap-xxhdpi",
        "2x": "mipmap-xxxhdpi"
    }
}

'''

import json
import sys
import os
import shutil


def read_config(config_file):
    if not os.path.exists(config_file):
        print("config file not exists.")
        return

    with open(config_file, encoding="utf-8") as config:
        return json.loads(config.read())


def check_config(config):
    try:
        if config is None:
            return False

        if not os.path.exists(config["input_dir"]):
            print("input_dir not exists.")
            return False

        if not os.path.exists(config["output_dir"]):
            print("output_dir not exists.")
            return False

        dir_maps = config["dir_maps"]
        input_dir = config["input_dir"]
        for key, _ in dir_maps.items():
            if not os.path.exists(input_dir + "/" + key):
                print(key, "not exists.")
                return False
    except json.KeyError as err:
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
        print("\n")
        check_or_create_dir(output_dir, value)
        print("[", key, " -> ", value, "]", sep="")
        copy_all_files(input_dir + "/" + key, output_dir + "/" + value)


if __name__ == "__main__":
    main()
