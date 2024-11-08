import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
from dataclasses import dataclass
from PIL import Image

@dataclass
class RamanImage:
    img: Image # PIL Image used for matplotlib imshow
    extent: np.array # extent for matplotlib imshow

def parse_image_txt(filename):
    """Parses the gray-scale image saved in .txt format as saved from the "Video" tab in LabSpec6

    Parameters
    ----------
    filename
        Path to txt file containing gray-scale image data and X/Y positions of pixels

    Returns
    -------
    x
        Numpy array (M) of x pixel positions
    y
        Numpy array (M) of y pixel positions
    intensity
        Numpy array (MxN) of gray-scale intensity values
    """

    with open(filename, encoding="latin-1") as f:
        x = None
        y = []
        vals = []
        for line in f:
            if line.startswith("#"):
                continue
            if line.startswith("\t"):
                x = [float(x) for x in line.split()]
            else:
                split = line.split()
                y.append(float(split[0]))
                vals.append([float(x) for x in split[1:]])
                


    return np.flip(np.array(x)), np.flip(np.array(y)), np.flip(np.array(vals))


def parse_image_comb(bmp_filename, txt_filename):
    """Returns PIL Image object with corresponding extends from .txt version of the image

    Parameters
    ----------
    bmp_filename
        Filename of the .bmp file taken from the LabSpec6 video feed
    txt_filename
        Filename of the .txt file taken from the LabSpec6 video feed

    Returns
    -------
    raman_image : RamanImage
    """

    x, y, gray = parse_image_txt(txt_filename)

    extent = (x[0], x[-1], y[-1], y[0])
    
    img = Image.open(bmp_filename)

    return RamanImage(img, np.array(extent))

@dataclass
class RamanMapData:
    """Holds spectral data with positions, rotations, and extent"""
    shift: np.array # 1D array of Raman shift values
    pos: np.array # 2 column array of x and y positions
    counts: np.array # 2D array where each row is the counts for a given spectra
    dim: np.array # (rows,columns) of map dimension
    center: np.array # (x,y) of center of map
    rotation: float # rotation in degrees
    extent: np.array # extents used for matplotlib imshow


def parse_l6m_txt(filename):
    """Parse the txt version of the l6m file and return a RamanMapData object

    Parameters
    ----------
    filename
        Filename of the txt version of the l6m file

    Returns
    -------
    map_data: RamanMapData
    """

    with open(filename, encoding="latin-1") as f:
        start_x = None
        start_y = None
        shift = None
        pos = []
        counts = []

        for line in f:
            if line.startswith("#"):
                if line.startswith("#X (µm)"):
                    split = line.split()
                    start_x = float(split[-1])
                elif line.startswith("#Y (µm)"):
                    split = line.split()
                    start_y = float(split[-1])
            elif line.startswith("\t"):
                shift = np.array([float(x) for x in line.split()])
            else:
                split = line.split()
                pos.append(np.array([float(split[1]), float(split[0])]))

                counts.append(np.array([float(x) for x in split[2:]]))

        if start_x == None:
            start_x = pos[0][0]
            start_y = pos[0][1]

        pos = np.array(pos)

        dim = determine_dim_from_pos(pos)

        start_pos = np.array([start_x, start_y])
        center = (pos[0] + pos[-1]) / 2

        start_pos_off = start_pos - center
        grid_pos_off = pos[0] - center


        dot = np.dot(start_pos_off, grid_pos_off)
        theta = np.arccos(dot / (np.linalg.norm(start_pos_off) * np.linalg.norm(grid_pos_off)))

        dx = np.abs(pos[0][0] - pos[1][0])
        dy = np.abs(pos[0][1] - pos[dim[1]][1])

        left = pos[0][0] - dx /  2
        right = pos[-1][0] + dx / 2
        bottom = pos[-1][1] + dy / 2
        top = pos[0][1] - dy / 2 



        return RamanMapData(shift, pos, counts, dim, center, np.degrees(theta), np.array((left, right, bottom, top)))


def determine_dim_from_pos(pos):
    """Use map positions to calculate rows and columns

    Parameters
    ----------
    pos : list[np.array]
        List of positions (x,y) for collected spectra

    Returns
    -------
    dimensions : np.array
        Dimensions (row, col) of the map
    """
    n_cols = 0
    cur_y = pos[0][1]
    for p in pos:
        if p[1] != cur_y:
            break

        n_cols += 1

    return np.array([len(pos) // n_cols, n_cols])

def extract_maxes_from_range(shift, counts, shift_min, shift_max, normalize=False):
    """Returns all maxes for a given Raman shift range. Wrapper function for extract_max_from_range
    
    Parameters
    ----------
    shift
        Raman shift array
    counts
        2D array of count data for map spectra
    shift_min
        Lower bound for Raman shift
    shift_max
        Upper bound for Raman shift
    normalize
        Optional argument to normalize extracted max value to the maximum of the spectrum

    Returns
    -------
    maxes
        Array of extracted maximums"""

    maxes = []
    for c in counts:
        start = np.argmax(shift > shift_min)
        end = np.argmax(shift > shift_max)
        m = np.max(c[start:end])
        if normalize:
            maxes.append(m / np.max(c))
        else:
            maxes.append(m)


    return np.array(maxes)

def quickplot_map(l6m_txt, img_bmp, img_txt, shift_min, shift_max, 
                  normalize=False, alpha=0.5):
    """Generate a quick representation of map data

    Parameters
    ----------
    l6m_txt : str
        Filename for txt version of the l6m file 
    img_bmp : str
        Filename for bmp version of camera view
    img_txt : str
        Filename for txt version of camera view
    shift_min : float
        Left bound for maximum value search
    shift_max : float
        Right bound for maximum value search
    normalize : bool
        Normalize extracted maximum value for spectra by maximum of spectra
    alpha : float
        Alpha value for imshow opacity of map overlay"""

    out = parse_l6m_txt(l6m_txt)
    out_img = parse_image_comb(img_bmp, img_txt)

    maxes = np.reshape(extract_maxes_from_range(out.shift, out.counts, shift_min, shift_max),
                       out.dim)
    plt.figure(figsize=(9, 4))
    plt.subplot(121)

    tr = transforms.Affine2D().rotate_deg(-out.rotation)
    plt.imshow(out_img.img, extent=out_img.extent)
    plt.imshow(maxes, extent=out.extent,
               transform=tr+plt.gca().transData, interpolation="none", alpha=0.6)

    plt.xlim(out_img.extent[0], out_img.extent[1])
    plt.ylim(out_img.extent[2], out_img.extent[3])
    plt.xlabel(r"X [$\mu$m]", fontsize=16)
    plt.ylabel(r"Y [$\mu$m]", fontsize=16)

    plt.subplot(122)
    for c in out.counts:
        plt.plot(out.shift, c, lw=0.5)
    plt.xlabel(r"Raman shift [cm$^{-1}$]", fontsize=16)
    plt.ylabel(r"Intensity [counts]", fontsize=16)
    plt.tight_layout()
    plt.show()


#quickplot_map("offgrid_3.txt", "offgrid.bmp", "offgrid.txt", 600, 800, normalize=True)
