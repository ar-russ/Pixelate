from PIL import Image
import configparser

config = configparser.ConfigParser()
config.read("base/config.ini")

default_name = config.get("settings", "default_name")
search_path = config.get("settings", "search_path")
save_path = config.get("settings", "save_path")


def generate_brick_tiles(image_size: tuple, brick_size: int = 16) -> Image:
    '''
    Генерирует картинку с текстурой кубиков конструктора.
        Параметры:
            image_size (tuple) : Размер картинки на выходе (в пикселях)
            brick_size (int) : Размер одного кубика (в пикселях)
    '''
    brick = Image.open("base/brick.png")
    brick = brick.resize((brick_size, brick_size))
    image = Image.new("RGBA", image_size)
    for x in range(0, image_size[0], brick_size):
        for y in range(0, image_size[1], brick_size):
            image.paste(brick, (x, y))
    return image


def pixelate(image: Image, pixel_size: int = 16):
    '''
    Добавляет на картинку image эффект мозайки (пикселизации).
        Параметры:
            image (Image) : Картинка, на которую надо наложить эффект
            pixel_size (int) : Размер одной ячейки мозайки в пикселях
    '''
    image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST)
    image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
    return image.convert("RGBA")


def generate_and_save_image(input_image, input_pixel_size):
    '''
    Генерирует картинку, накладывая на нее эффект пикселизации и текстуру
    кубиков конструктора, после чего сохраняет в корневой папке.
        Параметры:
            input_image (Image) : Картинка, на которую надо наложить эффекты
            input_pixel_size (int) : Размер одной ячейки мозайки для наложения
            эффекта мозайки (пикселизации) изображения.
    '''
    pixelated_image = pixelate(input_image, input_pixel_size)
    brick_texture = generate_brick_tiles(pixelated_image.size, input_pixel_size)
    result = Image.blend(pixelated_image, brick_texture, 0.5)
    result.save(save_path + "result.png")
    return result


def main():
    if not is_config_valid():
        return
    image_name = input("Введите название картинки вместе с её форматом (пример: source.png): ")
    if image_name == "":
        image_name = default_name
    try:
        input_image = Image.open(search_path + image_name)
    except FileNotFoundError:
        print("Картинка не найдена :(")
        return
    input_pixel_size = int(input("Введите размер одного кубика (в пикселях): "))
    if input_pixel_size > min(input_image.size) // 4 or input_pixel_size <= 0:
        print("Размер введен некорректно!")
        return
    print("Пожалуйста, подождите! Программа генерирует картинку...")
    result = generate_and_save_image(input_image, input_pixel_size)
    result.show()


def is_config_valid():
    if search_path != '' and search_path[-1] != "/":
        print("Пожалуйста, поставьте в конце путя search_path в файле base/config.ini символ '/'")
        return False
    if save_path != '' and save_path[-1] != "/":
        print("Пожалуйста, поставьте в конце путя save_path в файле base/config.ini символ '/'")
        return False
    return True


if __name__ == "__main__":
    main()

input() # Чтобы консоль не закрывалась мгновенно после завершения выполнения программы