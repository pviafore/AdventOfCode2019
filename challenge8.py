from typing import Iterable, List

IMAGE_SIZE = 25*6

def chunk(data: str, count: int) -> List[str]:
    return [data[i*count:count*(i+1)] for i in range(len(data) // count)]

def get_image_data() -> List[str]:
    with open("input/input8.txt") as input_file:
        return chunk(input_file.read(), IMAGE_SIZE)

def get_product_of_1s_and_2s_in_target_layer(image_data: List[str]) -> int:
    target_layer = min(image_data, key=lambda chunk: chunk.count("0"))
    return target_layer.count("1") * target_layer.count("2")

def print_image(image_data: List[str]):
    image_string = "".join(get_visible_pixel(pixels) for pixels in zip(*image_data))
    print("\n".join(chunk(image_string, 25)))

def get_visible_pixel(pixels: Iterable[str]) -> str:
    pixel = next(p for p in pixels if p != '2')
    return ' ' if pixel == '0' else '█'

IMAGE_DATA = get_image_data()
if __name__ == "__main__":
    print(get_product_of_1s_and_2s_in_target_layer(IMAGE_DATA))
    print_image(IMAGE_DATA)
