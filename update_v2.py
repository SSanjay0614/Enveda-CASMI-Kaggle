import json
import re

def update_notebook():
    nb_path = 'c:/Users/ssanj/OneDrive/Desktop/Sanjay/Antigravity/enveda_casmi/kernel_v2/casmi26-multimodal-v2-bioprior.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # 1. Update Cell 13: Popularity prior saturation & POOLPOP_MU tuning
    cell13 = nb['cells'][13]
    src13 = ''.join(cell13['source'])
    
    # Replace POOLPOP_MU = 0.25 with 0.20
    src13 = src13.replace('POOLPOP_MU = 0.25', 'POOLPOP_MU = 0.20  # Calibrated for natural product fidelity')
    
    # Clip extreme popularity values to prevent industrial solvent dominance
    target_f = 'f_ = z_ + POOLPOP_MU * np.where(isg_, 0.0, POOL_POP[np.maximum(pid_, 0)])'
    replacement_f = 'pop_raw = np.where(isg_, 0.0, POOL_POP[np.maximum(pid_, 0)])\n            pop_capped = np.clip(pop_raw, 0.0, 8.0)  # Prevents synthetic/solvent outliers from overriding spectral match\n            f_ = z_ + POOLPOP_MU * pop_capped'
    
    if target_f in src13:
        src13 = src13.replace(target_f, replacement_f)
        print("Updated Cell 13: Popularity prior saturation applied.")
    else:
        print("Warning: target_f not found in Cell 13")
        
    cell13['source'] = [line + '\n' for line in src13.split('\n')][:-1]

    # 2. Update Cell 19: RRF weights & Multi-tier PPM DreaMS tail injection
    cell19 = nb['cells'][19]
    src19 = ''.join(cell19['source'])
    
    # Replace ALPHA_BASE, KRR = 0.60, 3.0 with 0.65, 2.5
    src19 = src19.replace('ALPHA_BASE, KRR = 0.60, 3.0', 'ALPHA_BASE, KRR = 0.65, 2.5  # Tuned RRF balance for CASMI 2026')
    src19 = src19.replace('alpha=0.60', 'alpha=0.65')
    
    # Replace single 10 ppm window in DreaMS with multi-tier adaptive ppm window
    old_dreams = """                delta_m = target_neutral * 10e-6
                mass_mask = (dreams_np_mass >= target_neutral - delta_m) & (dreams_np_mass <= target_neutral + delta_m)
                matching_indices = np.where(mass_mask)[0]

                if len(matching_indices) > 0:
                    for idx in matching_indices:
                        smi = dreams_np_smiles[idx]
                        k = chem.score_key(smi) or smi
                        if k not in seen_keys:
                            seen_keys.add(k)
                            raw_smis.append(smi)
                            if len(raw_smis) >= 25:
                                break
                    n_injected += 1"""
                    
    new_dreams = """                # Multi-tier adaptive tolerance (10 ppm -> 25 ppm -> 50 ppm)
                for ppm_tier in [10.0, 25.0, 50.0]:
                    delta_m = target_neutral * (ppm_tier * 1e-6)
                    mass_mask = (dreams_np_mass >= target_neutral - delta_m) & (dreams_np_mass <= target_neutral + delta_m)
                    matching_indices = np.where(mass_mask)[0]
                    if len(matching_indices) > 0:
                        for idx in matching_indices:
                            smi = dreams_np_smiles[idx]
                            k = chem.score_key(smi) or smi
                            if k not in seen_keys:
                                seen_keys.add(k)
                                raw_smis.append(smi)
                                if len(raw_smis) >= 25:
                                    break
                        n_injected += 1
                        if len(raw_smis) >= 25:
                            break"""

    if old_dreams in src19:
        src19 = src19.replace(old_dreams, new_dreams)
        print("Updated Cell 19: Multi-tier adaptive DreaMS injection applied.")
    else:
        print("Warning: old_dreams not found in Cell 19")

    cell19['source'] = [line + '\n' for line in src19.split('\n')][:-1]

    # Save notebook
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=True)
    print("Version 2 notebook successfully updated and saved with ensure_ascii=True!")

if __name__ == '__main__':
    update_notebook()
