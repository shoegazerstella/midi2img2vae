import os, sys
from tqdm import tqdm

from midi2img import midi2image


def preprocess(DATA_DIR, SAVE_DIR):
    for (dirpath, dirnames, filenames) in os.walk(DATA_DIR):
        for filename in tqdm(filenames):
            if filename.endswith('.mid'):
                midi_filepath = os.path.join(dirpath, filename)
                midi2image(midi_filepath, SAVE_DIR)

def augmentation_by_mirroring(DATA_DIR, SAVE_DIR, save_as_image=False, mirror=True):
    """Data augmentation by mirroring the image."""
    for (dirpath, dirnames, filenames) in os.walk(DATA_DIR):
        for filename in tqdm(filenames):
            if filename.endswith('.mid'):
                midi_filepath = os.path.join(dirpath, filename)
                midi2image(midi_filepath, SAVE_DIR, save_as_image=save_as_image, mirror=mirror)


if __name__ == '__main__':

    DATA_DIR = os.path.join('dataset', 'groove')

    SAVE_DIR = os.path.join('dataset', 'groove2img_npy')
    preprocess(DATA_DIR, SAVE_DIR)

    #SAVE_DIR = os.path.join('dataset', 'groove2img_augmented_npy')
    #augmentation_by_mirroring(DATA_DIR, SAVE_DIR)
