#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import os
import shutil
from concurrent.futures import ThreadPoolExecutor


def copy_markdown_file(src_file, dst_file):
    if not os.path.exists(dst_file):
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy2(src_file, dst_file)
        print(f"Copied {src_file} to {dst_file}")
    else:
        print(f"Skipped {dst_file} (already exists)")


def copy_markdown_files(src_folder, dst_folder):
    tasks = []

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".md"):
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, src_folder)
                dst_file = os.path.join(dst_folder, rel_path)
                tasks.append((src_file, dst_file))

    with ThreadPoolExecutor() as executor:
        executor.map(lambda args: copy_markdown_file(*args), tasks)


def update_markdown_content(content):
    # Update relative paths (../) to absolute paths without /docs/ prefix
    content = content.replace('../specification/', '/specification/')
    return content


def copy_guide_files():
    guide_src = "../../docs/guide/"
    guide_dst = "../../docs/docs/guide/"
    
    # Copy all files from guide to docs/guide
    if os.path.exists(guide_src):
        os.makedirs(guide_dst, exist_ok=True)
        for item in os.listdir(guide_src):
            src_path = os.path.join(guide_src, item)
            dst_path = os.path.join(guide_dst, item)
            if os.path.isfile(src_path):
                # If it's a markdown file, update the content
                if src_path.endswith('.md'):
                    with open(src_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Update the paths in content
                    updated_content = update_markdown_content(content)
                    # Write the updated content to destination
                    with open(dst_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Copied and updated paths in {src_path} to {dst_path}")
                else:
                    # For non-markdown files, just copy as is
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied {src_path} to {dst_path}")
        print(f"Finished copying guide files")


def execute():
    # First copy guide files
    copy_guide_files()
    
    base_src_folder = "../../docs/"
    zh_cn_docs_dst = "../../i18n/zh-CN/docusaurus-plugin-content-docs/current/"
    en_us_docs_dst = "../../i18n/eu-US/docusaurus-plugin-content-docs/current/"

    base_blog_folder = "../../blog/"
    zh_cn_blog_dst = "../../i18n/zh-CN/docusaurus-plugin-content-blog/"
    en_us_blog_dst = "../../i18n/eu-US/docusaurus-plugin-content-blog/"

    copy_markdown_files(base_src_folder, zh_cn_docs_dst)
    copy_markdown_files(base_src_folder, en_us_docs_dst)

    copy_markdown_files(base_blog_folder, zh_cn_blog_dst)
    copy_markdown_files(base_blog_folder, en_us_blog_dst)


if __name__ == "__main__":
    print("Copying markdown files...")
    execute()
