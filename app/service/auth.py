import os
import json
import time
from app.client.engsel import get_new_token, get_profile
# from app.util import ensure_api_key # Hapus import ini karena sudah tidak perlu

class Auth:
    _instance_ = None
    _initialized_ = False

    # 1. API_KEY SEKARANG HANYA DIAMBIL DARI OS.ENVIRON
    # JANGAN PERNAH MENGAMBILNYA DARI INPUT()
    api_key = os.environ.get("API_KEY") 

    refresh_tokens = []
    # Format of refresh_tokens: [{"number": int, "refresh_token": str}]

    active_user = None
    # {
    #     "number": int,
    #     "subscriber_id": str,
    #     "subscription_type": str,
    #     "tokens": {
    #         "refresh_token": str,
    #         "access_token": str,
    #         "id_token": str
	#     }
    # }
    
    last_refresh_time = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance_:
            cls._instance_ = super().__new__(cls)
        return cls._instance_
    
    def __init__(self):
        if not self._initialized_:
            
            # --- BAGIAN PERUBAHAN KRITIS DIMULAI DI SINI ---
            
            # 2. HILANGKAN panggilan ke ensure_api_key() yang memicu input().
            # Kita menggunakan nilai yang sudah diambil dari os.environ.get("API_KEY")
            # pada baris ke-11. Kita hanya perlu memvalidasinya.
            
            if not self.api_key:
                # Jika dijalankan di Actions, ini seharusnya TIDAK terjadi.
                # Tapi kita tambahkan cek keamanan.
                raise ValueError("API_KEY environment variable is not set. Cannot continue without key.")
            
            # --- BAGIAN PERUBAHAN KRITIS SELESAI ---
            
            if os.path.exists("refresh-tokens.json"):
                self.load_tokens()
            else:
                # Create empty file
                with open("refresh-tokens.json", "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)

            # Select active user from file if available
            self.load_active_number()
            self.last_refresh_time = int(time.time())

            self._initialized_ = True
            
    # Sisa kode tetap sama...
    
    # ... (Semua fungsi lain tetap tidak berubah)

    def write_active_number(self):
        if self.active_user:
            with open("active.number", "w", encoding="utf-8") as f:
                f.write(str(self.active_user["number"]))
        else:
            if os.path.exists("active.number"):
                os.remove("active.number")
    
    def load_active_number(self):
        if os.path.exists("active.number"):
            with open("active.number", "r", encoding="utf-8") as f:
                number_str = f.read().strip()
                if number_str.isdigit():
                    number = int(number_str)
                    self.set_active_user(number)

AuthInstance = Auth()
