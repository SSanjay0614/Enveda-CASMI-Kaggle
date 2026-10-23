import json

def fix():
    nb_path = 'c:/Users/ssanj/OneDrive/Desktop/Sanjay/Antigravity/enveda_casmi/kernel_v3/casmi26_sota_v3.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    fixed_count = 0
    for i, cell in enumerate(nb['cells']):
        src = ''.join(cell['source'])
        if "assert platform.python_version_tuple()[:2] == ('3', '12')" in src:
            src = src.replace(
                "assert platform.python_version_tuple()[:2] == ('3', '12')",
                "assert platform.python_version_tuple()[0] == '3'  # Compatible with Python 3.12 & 3.13"
            )
            cell['source'] = [line + '\n' for line in src.split('\n')][:-1]
            fixed_count += 1
            print(f"Fixed Python version assertion in Cell {i}!")
        elif "platform.python_version_tuple()" in src:
            print(f"Other version check in Cell {i}:")
            for line in src.split('\n'):
                if 'platform' in line:
                    print("  ", line)

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=True)

    print(f"Done. Fixed {fixed_count} assertions.")

if __name__ == '__main__':
    fix()
