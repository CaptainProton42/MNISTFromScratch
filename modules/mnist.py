import os
import struct
import numpy as np

# Based on https://gist.github.com/akesling/5358964 which is in return
# loosely inspired by http://abel.ee.ucla.edu/cvxopt/_downloads/mnist.py
# which is GPL licensed.

def read(dataset = "training", path = "."):
    # Python function for importing the MNIST data set.  It returns an iterator
    # of 2-tuplesq2f s with the first element being the label and the second element
    # being a numpy.uint8 2D array of pixel data for the given image.

    if dataset is "training":
        fname_img = os.path.join(path, 'train-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)
        img = np.divide(img, 255)

    l = list()
    for i in range(len(lbl)):
        img_vec = img[i].flatten()
        lbl_vec = np.zeros(10)
        lbl_vec[lbl[i]] = 1
        l.append([list(img_vec), list(lbl_vec)])

    return l

def show(image):
    # Render a given numpy.uint8 2D array of pixel data.
    image = np.array(image).reshape(28, 28)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    imgplot = ax.imshow(image, cmap='Greys')
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    plt.show()