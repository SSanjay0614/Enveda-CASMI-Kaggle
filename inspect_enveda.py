import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi

def main():
    api = KaggleApi()
    api.authenticate()
    
    comp_id = 'enveda-CASMI26-molecule-id-mass-spectra'
    print(f"=== Inspecting Competition: {comp_id} ===")
    
    # 1. Check Files
    try:
        file_list = api.competition_list_files(comp_id)
        print("\n[Files in Competition]")
        for f in file_list.files:
            size_mb = f.totalBytes / (1024 * 1024) if hasattr(f, 'totalBytes') and f.totalBytes else 0
            print(f"  - {f.name} ({size_mb:.2f} MB)")
    except Exception as e:
        print(f"Error listing files (have you clicked 'Join Competition'?): {e}")

    # 2. Check Top Public Notebooks / Kernels by Votes
    print("\n[Top Notebooks by Votes]")
    try:
        kernels_vote = api.kernels_list(competition=comp_id, sort_by='voteCount', page_size=10)
        for k in kernels_vote:
            print(f"  - Ref: {k.ref}")
            print(f"    Title: {getattr(k, 'title', '')}")
            print(f"    Votes: {getattr(k, 'totalVotes', 0)}")
    except Exception as e:
        print(f"Error fetching kernels by vote: {e}")

    # 3. Check Top Public Notebooks by Score / Best Performing
    print("\n[Top Notebooks by Score / Hotness]")
    try:
        kernels_score = api.kernels_list(competition=comp_id, sort_by='scoreDescending', page_size=10)
        for k in kernels_score:
            print(f"  - Ref: {k.ref}")
            print(f"    Title: {getattr(k, 'title', '')}")
            print(f"    Score/Votes: {getattr(k, 'totalVotes', 0)}")
    except Exception as e:
        print(f"Error fetching kernels by score: {e}")

if __name__ == '__main__':
    main()
