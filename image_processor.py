import cv2
import numpy as np

def hex_to_hsv(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    bgr = (rgb[2], rgb[1], rgb[0])
    color_bgr = np.uint8([[list(bgr)]])
    hsv_color = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)[0][0]
    return hsv_color

def process_image(image_path, hex_colors):
    img = cv2.imread(image_path)
    # konversi ke hsv untuk proses filter warna
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # toleransi dibuat agak ketat, agar tidak ada elemen lain yg "ikut terdeteksi by warna"
    hue_tolerance = 5
    sat_tolerance = 10
    val_tolerance = 10

    final_filter = np.zeros(hsv.shape[:2], dtype="uint8")
    color_count = []

    for hex_color in hex_colors:
        hsv_color = hex_to_hsv(hex_color)

        # set toleransi pergeseran warna, karena tidak selalu akurat satu hexa warna
        lower_bound = np.array([
            max(0, hsv_color[0] - hue_tolerance), 
            max(0, hsv_color[1] - sat_tolerance), 
            max(0, hsv_color[2] - val_tolerance)
        ])
        upper_bound = np.array([
            min(180, hsv_color[0] + hue_tolerance), 
            min(255, hsv_color[1] + sat_tolerance), 
            min(255, hsv_color[2] + val_tolerance)
        ])

        # cari where filter
        filter = cv2.inRange(hsv, lower_bound, upper_bound)
        final_filter = final_filter | filter

        # jumlah piksel utk simbol warna (tidak dihitung)
        warna_simbol = 200
        # hitung jumlah piksel tiap2 warna
        color_count.append(cv2.countNonZero(filter) - warna_simbol)

    # pertahankan bagian gambar sesuai filter
    color_only = cv2.bitwise_and(img, img, mask=final_filter)
    # create gambar hitam-putih
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_3channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    # merge gambar hitam-putih dan berwarna
    result = np.where(color_only != 0, img, gray_3channel)
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # terkadang ada yg color count nya mines setelah dikurangi warna simbol
    color_count = [max(0, x) for x in color_count]
    print("Jumlah piksel tiap warna:")
    for count in color_count:
        print(f"{count} piksel")

    r = {
        "color_count" : color_count,
        "img" : result_rgb
    }
    return r
