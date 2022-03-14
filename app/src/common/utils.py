import os
from functools import partial
from multiprocessing import Pool, cpu_count

from src.settings import GENERAL


def _handler(paths, processor):
    processor(*paths)


def transform(source_directory, destination_directory, processor, paths_generator):
    """
    extract files from :source_directory using :paths_generator, transform using :processor and put into :destination_directory
    :param source_directory: path to source directory
    :param destination_directory: path to destination directory
    :param processor: transform-function
    :param paths_generator: get filenames from directory
    :return: None
    """
    source_paths, destination_paths = paths_generator(source_directory, destination_directory)

    if GENERAL['MULTIPROCESSING']:
        processor = partial(_handler, processor=processor)
        with Pool(min(len(source_paths), cpu_count())) as p:
            p.map(processor, zip(source_paths, destination_paths))
    else:
        for src, dst in zip(source_paths, destination_paths):
            processor(src, dst)


def general_paths_generator(source_directory, destination_directory, from_extension, to_extension):
    """
    Walk over files into :source_directory, filter :from_extension extension and generate destination path with :to_extension extension
    :param source_directory: path to source directory
    :param destination_directory: path to destination directory
    :param from_extension:
    :param to_extension:
    :return: source and destination file paths
    """
    source_paths = []
    destination_paths = []

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith(from_extension):
                source_paths.append(os.path.join(root, file))
                destination_paths.append(os.path.join(destination_directory, file.split('.')[0] + to_extension))

    return source_paths, destination_paths


pdf_to_html_paths = partial(general_paths_generator, from_extension='.pdf', to_extension='.html')
html_to_text_paths = partial(general_paths_generator, from_extension='.html', to_extension='.text')
pdf_to_json_paths = partial(general_paths_generator, from_extension='.pdf', to_extension='.json')
