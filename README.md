## 使用说明

**功能**：复制指定目录下某些子目录中的子文件到另一个目录中。

**使用说明**：需要在脚本目录下创建一个名为 `'copy_config.json'` 的配置文件。或者在执行脚本时使用一个参数来指定配置文件的路径。

**配置文件格式:**

```json
{
    "input_dir": "<string>",
    "output_dir": "<string>",
    "dir_maps": "<map>"
}
```

**字段说明：**

* **`input_dir`**: 输入目录，字符串类型。
* **`output_dir`**: 输出目录，字符串类型。
* **`dir_maps`**: 目录映射，`map` 类型。每个 `key` 都表示 `input_dir` 的一个子目录，`value` 都表示 `output_dir` 下的一个子目录。`key` 目录下的所有文件都会被复制到其 `value` 值对应的目录下。

**例：**

```json
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
```