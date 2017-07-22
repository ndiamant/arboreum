import imageio
import os
import re


FPS = 240

p = re.compile('\d+')

def get_key(fname):
    return int(p.findall(fname)[0])


def write_gif_from_dir(path='images'):
    filenames = sorted((path +'/' + fn for fn in os.listdir('images') if fn.endswith('.png')), key=get_key)

    with imageio.get_writer('test.gif', mode='I', fps=FPS) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)


def write_gif_from_arrays(arrays, name='trees.gif'):
    """arrays is a list of numpy arrays"""
    with imageio.get_writer(name, mode='I', fps=FPS) as writer:
        for array in arrays:
            writer.append_data(array)
