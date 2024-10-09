import matplotlib.pyplot as plt
import image_processor

hex_colors = [
    '#11d68f',  # Hijau (cepat)
    '#ffcf43',  # Kuning (padat)
    '#f24e42',  # Merah bata (lambat)
    '#a92727',  # Merah marun (sangat lambat)
]
process = image_processor.process_image("ss3.png", hex_colors)
color = max(process["color_count"])
index_color = process["color_count"].index(color)
lalu_lintas = "lancar"
if index_color == 1:
    lalu_lintas = "padat"
elif index_color == 2:
    lalu_lintas = "lambat"
elif index_color == 3:
    lalu_lintas = "sangat lambat"

plt.figure(figsize=(16, 9))
plt.imshow(process["img"])
plt.axis('off')
plt.title(lalu_lintas)
plt.show()