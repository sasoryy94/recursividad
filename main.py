from PIL import Image, ImageDraw

class Bloc:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.color = None
        self.subblocks = []

    def is_uniform(self):
        return len(self.subblocks) == 0

    def calculate_average_color(self, image):
        if self.color:
            return tuple(self.color)  # If color is already available, return it as a tuple
        else:
        # Initialize counters for RGB values
            total_red = total_green = total_blue = 0
            total_pixels = 0

        # Iterate through each pixel in the block
            for y in range(self.top_left[1], self.bottom_right[1]):
                for x in range(self.top_left[0], self.bottom_right[0]):
                    pixel_color = image.getpixel((x, y))
                    total_red += pixel_color[0]
                    total_green += pixel_color[1]
                    total_blue += pixel_color[2]
                    total_pixels += 1

        # Calculate the average RGB value
            average_red = total_red // total_pixels
            average_green = total_green // total_pixels
            average_blue = total_blue // total_pixels

        return (average_red, average_green, average_blue)  # Return the average color as a tuple

    def divide_into_subblocks(self):
        # Diviser le bloc en quatre sous-blocs
        mid_x = (self.top_left[0] + self.bottom_right[0]) // 2
        mid_y = (self.top_left[1] + self.bottom_right[1]) // 2

        subblock_top_lefts = [(self.top_left[0], self.top_left[1]), (mid_x, self.top_left[1]),
                              (self.top_left[0], mid_y), (mid_x, mid_y)]
        subblock_bottom_rights = [(mid_x, mid_y), (self.bottom_right[0], mid_y),
                                  (mid_x, self.bottom_right[1]), (self.bottom_right[0], self.bottom_right[1])]

        for tl, br in zip(subblock_top_lefts, subblock_bottom_rights):
            subblock = Bloc(tl, br)
            self.subblocks.append(subblock)


class ImageProcessor:
    @staticmethod
    def create_blocks(image, order):
        top_left = (0, 0)
        bottom_right = image.size
        root_block = Bloc(top_left, bottom_right)
        ImageProcessor._divide_image(image, root_block, order)
        return root_block

    @staticmethod
    def _divide_image(image, block, order):
        if order == 0:
            return
        block.divide_into_subblocks()
        for subblock in block.subblocks:
            ImageProcessor._divide_image(image, subblock, order - 1)


# Charger une image avec PIL
image = Image.open('images/galets.png')

# Convertir l'image en mode RGB pour obtenir des pixels sous forme de triplets
image_rgb = image.convert('RGB')

# Créer des blocs à partir de l'image
order = 6
root_block = ImageProcessor.create_blocks(image_rgb, order)

# Enregistrer l'image avec les blocs
draw = ImageDraw.Draw(image_rgb)

# Fonction récursive pour dessiner les blocs
def draw_blocks(block):
    if block.is_uniform():
        average_color = block.calculate_average_color(image_rgb)
        draw.rectangle([block.top_left, block.bottom_right], fill=average_color)
    else:
        for subblock in block.subblocks:
            draw_blocks(subblock)

# Dessiner les blocs sur l'image
draw_blocks(root_block)

# Enregistrer l'image avec les blocs dessinés
image_rgb.save("image_with_blocks6.png", "PNG")