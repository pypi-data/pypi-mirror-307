from horiba_raman_ccoverstreet import mapping
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


raman_map = mapping.parse_l6m_txt("Gd2O3_AlN_map_data.txt")
raman_img = mapping.parse_image_comb("Gd2O3_AlN_map.bmp", "Gd2O3_AlN_map.txt")

# Create an array and reshape based on rectangular mesh
# of peak maxes corresponding to Gd2O3
maxes = mapping.extract_maxes_from_range(raman_map.shift, raman_map.counts, 300, 500)
maxes = np.reshape(np.array(maxes), raman_map.dim)

# Throw everything into a plot to taste
plt.figure(figsize=(10, 4))
plt.subplot(121)
plt.title(r"Overlay of Gd$_2$O$_3$ Raman peak", fontsize=16)
plt.imshow(raman_img.img, extent=raman_img.extent)
plt.imshow(maxes, extent=raman_map.extent, alpha=0.4, interpolation="bilinear")
plt.annotate("AlN", (-280, 0), fontsize=16, ha="center")
plt.annotate(r"Gd$_2$O$_3$", (295, 0), fontsize=16, ha="center")
plt.xlim(raman_img.extent[0], raman_img.extent[1])
plt.ylim(raman_img.extent[2], raman_img.extent[3])
plt.xlabel(r"X [$\mu$m]", fontsize=16)
plt.ylabel(r"Y [$\mu$m]", fontsize=16)

plt.subplot(122)
plt.imshow(raman_img.img, extent=raman_img.extent, cmap=plt.get_cmap("gist_grey"))
plt.imshow(maxes, extent=raman_map.extent, alpha=0.4, cmap=plt.get_cmap("gist_heat"))
plt.xlim(raman_img.extent[0], raman_img.extent[1])
plt.ylim(raman_img.extent[2], raman_img.extent[3])

plt.xlabel(r"X [$\mu$m]", fontsize=16)
plt.ylabel(r"Y [$\mu$m]", fontsize=16)

plt.tight_layout()

plt.savefig("Raman_mapping_postprocessing_demo.png")
plt.show()


