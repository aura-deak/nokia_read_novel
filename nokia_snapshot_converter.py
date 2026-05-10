#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诺基亚浏览器快照文件生成器
将标准HTML或纯文本转换为诺基亚浏览器可识别的快照文件格式
"""

import struct
import argparse
import sys
from pathlib import Path


def create_nokia_snapshot(html_content, url="http://example.com", mystery_length=14):
    """
    创建诺基亚浏览器快照文件
    
    Args:
        html_content: HTML内容（字节串）
        url: 伪装的URL地址
        mystery_length: 神秘字段长度（默认14，可以是任意值包括0）
    
    Returns:
        bytes: 完整的快照文件内容
    """
    url_bytes = url.encode('utf-8')
    url_len = len(url_bytes)
    
    # 构建头部
    header_len = 24 + url_len + mystery_length
    version = 1
    reserved1 = 0
    url_start = 0x68747470  # "http" 的十六进制值
    
    # 构建头部字节（小端序）
    header = struct.pack(
        '<IIIIII',  # 6个无符号整数，小端序
        header_len,      # [0-3] 头部总长度
        version,         # [4-7] 版本号
        reserved1,       # [8-11] 保留字段
        url_len,         # [12-15] URL长度
        mystery_length,  # [16-19] 神秘字段长度
        url_start        # [20-23] URL开始标志
    )
    
    # 构建神秘字段（全0）
    mystery_field = b'\x00' * mystery_length
    
    # 组合所有部分
    snapshot = header + url_bytes + mystery_field + html_content
    
    return snapshot


def read_file_content(filepath, content_type='html'):
    """
    读取文件内容
    
    Args:
        filepath: 文件路径
        content_type: 内容类型 ('html' 或 'text')
    
    Returns:
        bytes: 文件内容
    """
    path = Path(filepath)
    
    if not path.exists():
        print(f"错误: 文件 '{filepath}' 不存在")
        sys.exit(1)
    
    try:
        with open(path, 'rb') as f:
            content = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 '{filepath}': {e}")
        sys.exit(1)
    
    # 如果是纯文本，转换为HTML格式
    if content_type == 'text':
        # 将纯文本包装为简单的HTML
        text_content = content.decode('utf-8', errors='ignore')
        html_content = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text File</title>
    <style>
        body {{ font-family: monospace; padding: 20px; line-height: 1.6; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
    </style>
</head>
<body>
    <pre>{text_content}</pre>
</body>
</html>"""
        content = html_content.encode('utf-8')
    
    return content


def main():
    parser = argparse.ArgumentParser(
        description='将HTML或纯文本文件转换为诺基亚浏览器快照文件格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换HTML文件
  %(prog)s input.html output.html --url http://example.com
  
  # 转换纯文本文件
  %(prog)s input.txt output.html --url http://example.com --type text
  
  # 设置神秘字段长度为0
  %(prog)s input.html output.html --url http://example.com --mystery 0
        """
    )
    
    parser.add_argument('input', help='输入文件路径（HTML或纯文本）')
    parser.add_argument('output', help='输出文件路径')
    parser.add_argument('--url', '-u', default='http://example.com',
                        help='伪装的URL地址（默认: http://example.com）')
    parser.add_argument('--type', '-t', choices=['html', 'text'], default='html',
                        help='输入文件类型（默认: html）')
    parser.add_argument('--mystery', '-m', type=int, default=14,
                        help='神秘字段长度（默认: 14，可以是任意值包括0）')
    
    args = parser.parse_args()
    
    # 读取输入文件
    print(f"读取输入文件: {args.input}")
    html_content = read_file_content(args.input, args.type)
    print(f"  内容长度: {len(html_content)} 字节")
    
    # 创建快照文件
    print(f"创建诺基亚快照文件...")
    print(f"  伪装URL: {args.url}")
    print(f"  神秘字段长度: {args.mystery}")
    
    snapshot = create_nokia_snapshot(html_content, args.url, args.mystery)
    
    # 保存输出文件
    try:
        output_path = Path(args.output)
        with open(output_path, 'wb') as f:
            f.write(snapshot)
        print(f"  输出文件: {args.output}")
        print(f"  文件大小: {len(snapshot)} 字节")
        print("\n转换成功！")
    except Exception as e:
        print(f"错误: 无法写入输出文件 '{args.output}': {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()