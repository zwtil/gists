import os
import toml
import tempfile

meta = toml.load(".github/data/meta.toml")

pathes = os.listdir()

req_list = set()

for k, v in meta.items():
    if isinstance(v, dict) and k in pathes:
        depends = v.get("depends", [])

        for depend in depends:
            req_list.add(depend)

# write req file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
    for req in req_list:
        tmp.write(f"{req}\n")
    tmp_path = tmp.name

os.system(f"pip install -r {tmp_path}")
os.unlink(tmp_path)
