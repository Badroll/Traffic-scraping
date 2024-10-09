# import modul
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import time
import csv
import image_processor

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
search = "tugu muda semarang"
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(search + Keys.RETURN)
time.sleep(3)

# zoom in
canvas = driver.find_element(By.CLASS_NAME, "widget-scene-canvas")
for _ in range(2):
    ActionChains(driver).move_to_element(canvas).click(canvas).send_keys('+').perform()
    time.sleep(1)

# shift + kanan
ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ARROW_RIGHT).key_up(Keys.SHIFT).perform()
time.sleep(1)

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

csv_data = [
    ["no.", "lokasi", "hari", "jam", "lalu lintas", "skor cepat", "skor padat", "skor lambat", "skor sangat lambat", "file"]
]
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

    for i in range(jam_available * position_per_jam):
        # Ekstrak teks dari elemen dg class "Jga6Nb"
        traffic_info_div = driver.find_element(By.CLASS_NAME, "Jga6Nb")
        traffic_info_text = traffic_info_div.text
        waktu_hasil = traffic_info_text.split(",")
        print("waktu_hasil", waktu_hasil)
        # save data
        filename = f'data/traffic_{search}_{day}-{waktu_hasil[1]}.png'
        # simpan ss
        print("simpan ss")
        driver.save_screenshot(filename)
        # proses ss
        print("proses ss")
        hex_colors = [
            '#11d68f',  # Hijau (cepat)
            '#ffcf43',  # Kuning (padat)
            '#f24e42',  # Merah bata (lambat)
            '#a92727',  # Merah marun (sangat lambat)
        ]
        process = image_processor.process_image(filename, hex_colors)
        color_count = process["color_count"]
        max_color = max(color_count)
        index_color = color_count.index(max_color)
        lalu_lintas = "lancar"
        if index_color == 1:
            lalu_lintas = "padat"
        elif index_color == 2:
            lalu_lintas = "lambat"
        elif index_color == 3:
            lalu_lintas = "sangat lambat"
        # just for normalisasi
        faktor_pembagi = 10
        csv_data.append([(i+1), search, day, waktu_hasil[1], lalu_lintas, color_count[0]/faktor_pembagi, color_count[1]/faktor_pembagi, color_count[2]/faktor_pembagi, color_count[3]/faktor_pembagi, filename])

        if waktu_hasil[1] == "22.00":
            print("reach 22.00, complete for " + day)
            break
        time_slider.send_keys(Keys.ARROW_RIGHT)
        time.sleep(1)

print("scraping done")

# dump ke csv
with open('typical_traffic.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(csv_data)

driver.quit()
