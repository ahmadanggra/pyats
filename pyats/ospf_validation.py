import sys
import os
import json
from genie.utils.diff import Diff
from pathlib import Path

# Exclude list untuk field yang tidak relevan dalam perbandingan
exclude_list = [
    "updated", 
    "age",
    "uptime",
    "last_change",
    "cksum",
    "seq",
    "dead_timer",
    "hello_timer",
    "checksum",
    "seq_num",
    "statistics",
    "lsas",
    "last_state_change",
    "bdr_ip_addr",
    "dr_ip_addr",
    "state",
    "bdr_router_id",
    "dr_router_id",
    "area_scope_lsa_cksum_sum"
]

def validate_ospf(pre_dir, post_dir):
    try:    
        # Gunakan nama variabel yang jelas untuk PATH FOLDER agar tidak tertimpa
        pre_folder_path = Path('/tmp/semaphore/pyats/' + pre_dir)
        post_folder_path = Path('/tmp/semaphore/pyats/' + post_dir)

        # Ambil daftar file JSON dari folder pre_snapshot (menggunakan filter .txt sesuai kode Anda)
        files_to_compare = [f for f in os.listdir(pre_folder_path) if f.endswith('.txt')]

        for file_name in files_to_compare:
            path_pre = os.path.join(pre_folder_path, file_name)
            path_post = os.path.join(post_folder_path, file_name)

            # Pastikan file yang sama juga ada di folder post_snapshot
            if not os.path.exists(path_post):
                print(f"⚠️  [LEWATKAN] File {file_name} tidak ditemukan di folder post.")
                continue
                
            print(f"--- Membandingkan File: {file_name} ---")
            
            # Gunakan nama variabel baru untuk MENAMPUNG ISI DICTIONARY agar tidak menimpa path folder
            with open(path_pre, 'r', encoding='utf-8') as f:
                pre_json_content = json.load(f)  
                
            with open(path_post, 'r', encoding='utf-8') as f:
                post_json_content = json.load(f) 
                
            # Masukkan variabel isi JSON baru ke dalam Genie Diff
            my_diff = Diff(pre_json_content, post_json_content, exclude=exclude_list)
            my_diff.findDiff()
            
            # Cetak hasil analisis jika ada perbedaan riil
            if str(my_diff).strip():
                print(my_diff)
            else:
                print("✅ Identik (Tidak ada perbedaan di luar field waktu yang diabaikan).\n")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

def main():
    validate_ospf(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()