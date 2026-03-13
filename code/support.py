from settings import *


def import_image(*path, format="png", alpha=True):
    full_path = join(*path) + f".{format}"
    image = pygame.image.load(full_path)
    return image.convert_alpha() if alpha else image.convert()


def import_folder(*path):
    frames = []

    for folder_path, _, files in walk(join(*path)):
        for file_name in sorted(files, key=lambda name: int(name.split(".")[0])):
            full_path = join(folder_path, file_name)
            frames.append(pygame.image.load(full_path).convert_alpha())

    return frames


def audio_importer(*path):
    audio_dict = {}

    for folder_path, _, files in walk(join(*path)):
        for file_name in files:
            full_path = join(folder_path, file_name)
            audio_dict[file_name.split(".")[0]] = pygame.mixer.Sound(full_path)

    return audio_dict
