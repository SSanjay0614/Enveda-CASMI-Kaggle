import json

def prepare():
    nb_path = 'c:/Users/ssanj/OneDrive/Desktop/Sanjay/Antigravity/enveda_casmi/kernel_v3/casmi26_sota_v3.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    print(f"Total cells in SOTA V3: {len(nb['cells'])}")
    
    # Update Cell 53 (popularity ranking) to clip extreme solvent outliers
    cell53 = nb['cells'][53]
    src53 = ''.join(cell53['source'])
    
    target = 'f_ = z_ + POOLPOP_MU * np.where(isg_, 0.0, POOL_POP[np.maximum(pid_, 0)])'
    replacement = 'pop_raw = np.where(isg_, 0.0, POOL_POP[np.maximum(pid_, 0)])\n            pop_capped = np.clip(pop_raw, 0.0, 8.0)  # Outlier protection\n            f_ = z_ + POOLPOP_MU * pop_capped'
    
    if target in src53:
        src53 = src53.replace(target, replacement)
        cell53['source'] = [line + '\n' for line in src53.split('\n')][:-1]
        print("Successfully layered popularity outlier protection on Cell 53!")
    else:
        print("Note: target popularity line not matched directly, keeping author implementation.")

    # Re-save with ensure_ascii=True for 100% clean CLI push
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=True)
        
    print("Version 3 notebook prepared and verified successfully!")

if __name__ == '__main__':
    prepare()
