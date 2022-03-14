import pdftotree


def pdf_to_html_converter(source_path, destination_path):
    """
    Simple convertation from pdf to html using pdftotree
    :param source_path: path to source file
    :param destination_path: path to destination directory
    :return: None
    """
    pdftotree.parse(source_path, destination_path)
