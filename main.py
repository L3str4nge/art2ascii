from PIL import Image
from progress.bar import Bar
from datetime import datetime


class Pixel:
    def __init__(self, point: tuple, red: int, green: int, blue: int, alpha: int):
        self.point = point
        self.red = red
        self.green = green
        self.blue = blue

    def greyscale(self) -> float:
        """
        Calculating RGB grayscale value by following pattern:
        Y = 0.2126*RED + 0.587*GREEN + 0.114*BLUE
        :return: float
        """
        return 0.2126 * self.red + 0.587 * self.green + 0.114 * self.blue

    def to_ascii(self):
        greyscale = self.greyscale()
        return GreyscaleAscii.get_ascii(greyscale)


class GreyscaleAscii:
    """
    Greyscale value | ascii character
    0 - 100         |      #
    100 - 200       |      "
    200 - 232       |     ' '
    """

    @staticmethod
    def get_ascii(greyscale_value: float) -> str:
        if 0 <= greyscale_value < 100:
            return "#"
        elif 100 <= greyscale_value < 200:
            return '"'
        elif 200 <= greyscale_value < 233:
            return ' '


image_path = "C:\\Users\zwsmzzki\\Documents\\art2ascii\\DonaldDuck.png"


def load_image(image_path):
    image: Image = Image.open(image_path)
    pixels = image.load()
    image_size = image.size
    pixels_to_process = []

    with Bar('Processing', max=image_size[0] * image_size[1], fill='#', suffix='%(percent)d%%') as progress_bar:
        for x in range(image_size[1]):
            pixels_line = []
            for y in range(image_size[0]):
                progress_bar.next()
                pixels_line.append(Pixel((y, x), *pixels[y, x]))

            pixels_to_process.append(pixels_line)

    return pixels_to_process


def write_image_ascii(pixels, output_filename):
    filename = f"{output_filename}_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(filename, 'w') as txt_image:
        for pixel_line in pixels:
            for pixel in pixel_line:
                txt_image.write(pixel.to_ascii())
            txt_image.write('\n')


if __name__ == '__main__':
    # TODO: dorobic parametry
    pixels = load_image(image_path)
    write_image_ascii(pixels, 'test')
