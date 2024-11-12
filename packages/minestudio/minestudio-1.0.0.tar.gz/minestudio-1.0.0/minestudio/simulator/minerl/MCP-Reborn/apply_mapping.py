# 简陋的实现，不知道会不会有问题....

from pathlib import Path
import os
import glob
import csv
from tqdm import tqdm

mapping_file = Path("/home/zhangbowei/.gradle/caches/forge_gradle/mcp_repo/net/minecraft/server/1.16.5-20210115.111550/server-1.16.5-20210115.111550-srg.jar")
tmp_dir = Path("/tmp/mcp_mappings/")
field_csv = tmp_dir / "fields.csv"
method_csv = tmp_dir / "methods.csv"

os.system(f"unzip -o {mapping_file} -d {tmp_dir}")


def parse_mappings(file_path):
    mappings = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            searge, name, _, _ = row
            mappings[searge] = name
    return mappings

field_mappings = parse_mappings(field_csv)
method_mappings = parse_mappings(method_csv)
java_files = [f for f in glob.glob("**/*.java", recursive=True)]

def apply_mapping(file_path, mappings):
    with open(file_path, 'r') as file:
        filedata = file.read()
    for searge, name in mappings.items():
        filedata = filedata.replace(searge, name)
    with open(file_path, 'w') as file:
        file.write(filedata)

for java_file_path in tqdm(java_files):
    apply_mapping(java_file_path, field_mappings)
    apply_mapping(java_file_path, method_mappings)