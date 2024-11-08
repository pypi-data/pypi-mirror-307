from horiba_raman_ccoverstreet import mapping
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms

# Load data
raman_map = mapping.parse_l6m_txt("offgrid_3.txt")
raman_img = mapping.parse_image_comb("offgrid.bmp", "offgrid.txt")

# Extract peak intensities corresponding to Gd2O3
maxes = np.reshape(mapping.extract_maxes_from_range(raman_map.shift, raman_map.counts, 600, 800,
                                         normalize=True), raman_map.dim)


# Move map to center and then rotate
# Use negative rotation since imshow rotate is stage was flipped in this measurement
rotation = transforms.Affine2D().translate(*-raman_map.center).rotate_deg(-raman_map.rotation).translate(*raman_map.center)
plt.imshow(raman_img.img, extent=raman_img.extent)
plt.imshow(maxes, extent=raman_map.extent, transform=rotation+plt.gca().transData,
           interpolation="bilinear", alpha=0.5)
plt.xlim(raman_img.extent[0], raman_img.extent[1])
plt.ylim(raman_img.extent[2], raman_img.extent[3])
plt.savefig("rotated.png")
plt.show()
