# Mengimpor semua library yang kita butuhkan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- FUNGSI UTAMA UNTUK MENJALANKAN TES ---
def jalankan_tes_otomasi():
    if not os.path.exists("laporan_tes"):
        os.makedirs("laporan_tes")

    # --- Setup ---
    print("Memulai setup driver Chrome dalam mode headless...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    wait = WebDriverWait(driver, 15)
    laporan = []
    
    try:
        # 1. Test Case Positif: Memastikan Judul Halaman Utama Benar (TETAP SAMA)
        print("\nMenjalankan Test Case 1: Verifikasi Judul Halaman...")
        driver.get("https://indonesiaindicator.com/home")
        wait.until(EC.title_contains("Indonesia Indicator"))
        laporan.append("Test 1 [LULUS]: Judul halaman utama sudah sesuai harapan.")
        driver.save_screenshot("laporan_tes/1_judul_halaman.png")
        print("Test Case 1 Selesai.")

        # 2. Test Case Positif: Menguji Fungsionalitas Navigasi ke Halaman 'Who We Are'
        print("\nMenjalankan Test Case 2: Navigasi ke Halaman 'Who We Are'...")
        driver.get("https://indonesiaindicator.com/home") 
        tombol_who_we_are = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Who We Are")))
        driver.execute_script("arguments[0].click();", tombol_who_we_are)
        wait.until(EC.url_contains("who-we-are"))
        laporan.append("Test 2 [LULUS]: Navigasi ke halaman 'Who We Are' berhasil.")
        driver.save_screenshot("laporan_tes/2_halaman_who_we_are.png")
        print("Test Case 2 Selesai.")

        # 3. Test Case Positif: Menguji Fungsionalitas Tombol 'Learn More'
        print("\nMenjalankan Test Case 3: Fungsionalitas Tombol 'Learn More'...")
        driver.get("https://indonesiaindicator.com/home")
        tombol_learn_more = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Learn More")))
        driver.execute_script("arguments[0].click();", tombol_learn_more)
        wait.until(EC.url_contains("who-we-are"))
        laporan.append("Test 3 [LULUS]: Tombol 'Learn More' berfungsi dan mengarah ke halaman yang benar.")
        driver.save_screenshot("laporan_tes/3_halaman_learn_more.png")
        print("Test Case 3 Selesai.")

        # 4. Test Case Negatif (BARU): Memastikan Teks Tidak Ada di Halaman
        print("\nMenjalankan Test Case 4 (Negatif): Verifikasi Teks Tidak Ada...")
        driver.get("https://indonesiaindicator.com/home")
        
        # PERBAIKAN: Kita cari seluruh isi halaman dan pastikan teks 'mustahil' ini tidak ada.
        page_source = driver.page_source
        non_existent_text = "Selamat Datang di Toko Kue ABCDE"
        assert non_existent_text not in page_source
        
        laporan.append("Test 4 [LULUS - Negatif]: Teks yang tidak seharusnya ada, memang tidak ditemukan di halaman.")
        driver.save_screenshot("laporan_tes/4_teks_tidak_ada.png")
        print("Test Case 4 Selesai.")

    except Exception as e:
        laporan.append(f"SEBUAH TES GAGAL: {e}")
        driver.save_screenshot("laporan_tes/ERROR.png")
        print(f"TERJADI ERROR: {e}")

    finally:
        print("\n--- LAPORAN HASIL PENGUJIAN OTOMATIS ---")
        for baris in laporan:
            print(baris)
        print("------------------------------------------")
        print("Pengujian selesai. Semua screenshot telah disimpan di folder 'laporan_tes'.")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    jalankan_tes_otomasi()
