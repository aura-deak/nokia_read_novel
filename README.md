# 诺基亚浏览器快照文件转换器

## 简介

这是一个用于将标准HTML或纯文本文件转换为诺基亚浏览器快照文件格式的Python脚本。通过逆向分析诺基亚浏览器的快照文件格式，实现了对这种专有格式的支持。

## 测试设备

本程序的文件提取、逆向分析和所有功能测试均在以下设备上进行：

- **设备型号**: Nokia 215 4G
- **型号代码**: TA-1278
- **浏览器**: 诺基亚内置浏览器

## 功能特性

- 支持HTML文件转换
- 支持纯文本文件自动包装为HTML
- 支持自定义伪装URL地址
- 神秘字段可配置长度（包括设置为0以最小化文件大小）
- 命令行界面，易于使用

## 安装

无需额外安装，只需Python 3环境即可运行。

## 使用方法

### 基本用法

```bash
# 转换HTML文件
python3 nokia_snapshot_converter.py input.html output.html --url "http://example.com"

# 转换纯文本文件
python3 nokia_snapshot_converter.py input.txt output.html --url "http://example.com" --type text

# 设置神秘字段长度为0（最小化文件）
python3 nokia_snapshot_converter.py input.html output.html --url "http://example.com" --mystery 0
```

### 参数说明

- `input`: 输入文件路径（必需）
- `output`: 输出文件路径（必需）
- `--url, -u`: 伪装的URL地址（默认: http://example.com）
- `--type, -t`: 输入文件类型，可选 `html` 或 `text`（默认: html）
- `--mystery, -m`: 神秘字段长度（默认: 14，可以是任意值包括0）

### 示例

```bash
# 转换一个小说HTML文件，伪装为小说网站
python3 nokia_snapshot_converter.py novel.html novel_snapshot.html --url "http://www.novel-site.com"

# 转换一个文本文件，设置为最小文件大小
python3 nokia_snapshot_converter.py readme.txt readme_snapshot.html --type text --mystery 0
```

## 文件格式说明

诺基亚浏览器快照文件格式由以下部分组成：

```
[头部 24字节]
├─ [0-3]    头部总长度 (小端序)
├─ [4-7]    版本号 (小端序，当前为1)
├─ [8-11]   保留字段 (总是0)
├─ [12-15]  URL长度 (小端序)
├─ [16-19]  神秘字段长度 (小端序)
└─ [20-23]  URL开始标志 (总是 "http" = 0x68747470)

[URL数据]
└─ [24-24+URL长度-1]  URL内容（UTF-8编码）

[神秘字段]
└─ [24+URL长度-24+URL长度+神秘字段长度-1]  神秘字段（可填充任意数据，建议全0）

[HTML内容]
└─ [24+URL长度+神秘字段长度-...]  标准HTML内容
```

## 神秘字段说明

通过实验验证，神秘字段：
- 不是必须的（可设为0长度）
- 内容可以是任意值（建议使用全0）
- 可能是浏览器内部用于跟踪或缓存管理
- 不影响快照文件的正常显示

## 注意事项

- 输出文件建议使用 `.html` 扩展名
- 纯文本文件会自动转换为HTML格式，包含基本的样式
- 伪装URL不会影响实际显示的内容，仅用于浏览器内部标识

## 技术细节

详细的文件格式分析和推理过程请参考 `CHAT.md` 文件。
