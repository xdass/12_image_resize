from PIL import Image
import argparse
import os
from math import floor


def open_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        return None


def save_image(image, default_path=None):
    image.save(default_path)


def generate_path_to_image(image_path, new_image):
    orig_filename, orig_file_ext = os.path.splitext(image_path)
    new_filename = '{}__{}x{}{}'.format(orig_filename, new_image.width, new_image.height, orig_file_ext)
    return new_filename


def resize_image(image_to_resize, width, height, scale):
    result_image = None
    original_width, original_height = image_to_resize.size
    if scale and (height or width):
        raise ValueError('You can`t use --scale option with width and height arguments!')
    elif scale:
        result_image = image_to_resize.resize((int(original_width * scale), int(original_height * scale)))
    elif width is None:
        resize_width = original_width / (original_height / height)
        result_image = image_to_resize.resize((floor(resize_width), height))
    elif height is None:
        resize_height = original_height / (original_width / width)
        result_image = image_to_resize.resize((width, floor(resize_height)))
    elif width and height:
        result_image = image_to_resize.resize((width, height))
    return result_image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image Resizer')
    parser.add_argument('orig_image_path', help='path to original image')
    parser.add_argument('--width',
                        type=int,
                        help='Image resize width. You cant use --scale with this option')
    parser.add_argument('--height',
                        type=int,
                        help='Image resize height. You cant use --scale with this option')
    parser.add_argument('--scale',
                        type=float,
                        help='Zoom ratio. If you use this option you cant use --width and --height')
    parser.add_argument('--output',
                        help='Resized file destination. If this option not used, the file saved near the original file')
    args = parser.parse_args()

    original_image = open_image(args.orig_image_path)
    if original_image is not None:
        resized_image = resize_image(original_image, args.width, args.height, args.scale)
        if args.output is None:
            new_image_path = generate_path_to_image(args.orig_image_path, resized_image)
        else:
            new_image_path = args.output
        save_image(resized_image, new_image_path)
    else:
        print('File {} not found'.format(args.orig_image_path))
