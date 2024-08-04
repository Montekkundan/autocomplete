import os

MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 400

NEW_LINE_CHAR = "<N>"

full_paths = []
for dir_path, dir_names, filenames in os.walk("repos"):
    for f in filenames:
        full_path = os.path.join(dir_path, f)
        full_paths.append(full_path)
print(len(full_paths))

with open("python_code.txt", "a") as f:
    for fpath in full_paths:
        try:
            d = open(fpath, "r").read()
            fd = d.replace("\n", NEW_LINE_CHAR)
            if 100 < len(d) <= MAX_CHAR_LENGTH:
                f.write(fd + '\n')
            else:
                sd = fd.split(f"{NEW_LINE_CHAR}{NEW_LINE_CHAR}")
                substring = ""
                for split in sd:
                    substring += split + f"{NEW_LINE_CHAR}{NEW_LINE_CHAR}"
                    if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:
                        f.write(fd + '\n')
                        substring = ""
        except Exception as e:
            print(str(e))
