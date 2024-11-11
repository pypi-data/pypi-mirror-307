# md_replace.py

import os
import re
import sys

def replace_file_paths_in_md(md_file_path, suffix):
    # .mdファイルを読み込む
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.read()

    # {{}} で囲まれた文字列が存在するか確認
    if not re.search(r'\{\{.+?\}\}', content):
        return  # 存在しない場合は処理をスキップ

    # 空白を含むファイルパスにも対応
    pattern = r'\{\{(\s*.+?\s*)\}\}'
    matches = re.findall(pattern, content)

    for match in matches:
        file_path = match.strip()  # 空白文字を除去
        # 相対パスを絶対パスに変換
        file_path_abs = os.path.abspath(os.path.join(os.path.dirname(md_file_path), file_path))
        if os.path.isfile(file_path_abs):
            # ファイルの内容を読み込む
            with open(file_path_abs, 'r', encoding='utf-8') as f:
                file_content = f.read()
            # 置換
            content = content.replace(f'{{{{{file_path}}}}}', file_content)
        else:
            print(f"Warning: File not found: {file_path_abs}")

    # 新しいファイル名を作成
    base, ext = os.path.splitext(md_file_path)
    new_md_file_path = f"{base}{suffix}{ext}"

    # 新しい内容を保存
    with open(new_md_file_path, 'w', encoding='utf-8') as new_md_file:
        new_md_file.write(content)

def main():
    if len(sys.argv) != 2:
        print("Usage: md_replace <suffix>")
        sys.exit(1)

    suffix = sys.argv[1]

    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.md'):
                # サフィックスが付与されたファイルを除外
                base_name, ext = os.path.splitext(filename)
                if base_name.endswith(suffix):
                    # サフィックスが付いている場合はスキップ
                    continue
                md_file_path = os.path.join(dirpath, filename)
                replace_file_paths_in_md(md_file_path, suffix)

if __name__ == '__main__':
    main()
