# import modul
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# initiate driver
print("initiate driver")
driver = webdriver.Firefox(executable_path=r'C:\python\warnawarni\geckodriver.exe')
driver.maximize_window()

# Buka google maps
print("Buka google maps")
driver.get("https://www.google.com/maps")
time.sleep(3)

# search jalan
print("search jalan")
search = "jalan jenderal sudirman semarang"
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(search + Keys.RETURN)
time.sleep(2)

# Arahkan mouse ke tombol "Lapisan"
print('Arahkan mouse ke tombol "Lapisan"')
layers_button = driver.find_element(By.XPATH, "//*[text()='Lapisan']")
ActionChains(driver).move_to_element(layers_button).perform()
time.sleep(2)

# Klik opsi "Lalu Lintas" (Traffic)
print('Klik opsi "Lalu Lintas" (Traffic)')
traffic_option = driver.find_element(By.XPATH, "//*[text()='Lalu Lintas']")
traffic_option.click()
time.sleep(2)

# Klik div dg class "gYkzb" untuk menutup side panel
print('Klik div dg class "gYkzb" untuk menutup side panel')
collapse_button = driver.find_element(By.CSS_SELECTOR, "div.gYkzb")
collapse_button.click()
time.sleep(2)

# Klik dulu untuk trigger select2
print('Klik dulu untuk trigger select2')
typical_traffic_option1 = driver.find_element(By.XPATH, "//*[text()='Lalu lintas langsung']")
typical_traffic_option1.click()
time.sleep(2)

# pilih (klik) "lalu lintas biasanya"
print('pilih (klik) "lalu lintas biasanya"')
typical_traffic_option2 = driver.find_element(By.XPATH, "//*[text()='Lalu lintas biasanya']")
typical_traffic_option2.click()
time.sleep(2)

# Cari elemen slider jam (span dg role="slider")
print('Cari elemen slider jam (span dg role="slider")')
time_slider = driver.find_element(By.XPATH, "//span[@role='slider']")
time.sleep(2)

days = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
for day in days:
    print("---------------------------------------------------------------------")
    print(day)
    # Klik tombol dg aria-label sesuai hari
    print('Klik tombol dg aria-label sesuai hari ' + day)
    sunday_button = driver.find_element(By.XPATH, "//*[@aria-label='"+day+"']")
    sunday_button.click()

    jam_default = 9
    jam_min = 6
    jam_max = 22
    jam_available = jam_max - jam_min
    position_per_jam = 12

    # set to first one (06.00)
    print('set to first one (06.00)')
    time_slider.click()
    for _ in range(jam_available * position_per_jam):
        time_slider.send_keys(Keys.ARROW_LEFT)
    time.sleep(1)

    for _ in range(jam_available * position_per_jam):
        # Ekstrak teks dari elemen dg class "Jga6Nb"
        traffic_info_div = driver.find_element(By.CLASS_NAME, "Jga6Nb")
        traffic_info_text = traffic_info_div.text
        waktu_hasil = traffic_info_text.split(",")
        print("waktu_hasil", waktu_hasil)
        # save screenshot
        driver.save_screenshot(f'data/traffic_{search}_{day}-{waktu_hasil[1]}.png')
        if waktu_hasil[1] == "22.00":
            print("reach 22.00, complete for " + day)
            break
        time_slider.send_keys(Keys.ARROW_RIGHT)
        time.sleep(1)

print("DONE")
driver.quit()
