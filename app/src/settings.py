import os


GENERAL = {
    'MULTIPROCESSING': False
}

PDF_TO_HTML = {
    'SOURCE_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/pdfs/Aastha Bist_CV.pdf'),
    'DESTINATION_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/htmls/Aastha Bist_CV.html'),
}

HMTL_TO_ORDERED_SENT = {
    'SOURCE_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/htmls/Aastha Bist_CV.html'),
    'DESTINATION_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/texts/Aastha Bist_CV.txt'),
}

PDF_TO_TEXT_BATCH = {
    'PDF_DIR_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/pdfs/'),
    'HTML_DIR_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/htmls/'),
    'TEXT_DIR_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/texts/'),
}

GET_FEATURES_FROM_PDF = {
    'SOURCE_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..',
                                'data/pdfs/Aastha Bist_CV.pdf'),
    'DESTINATION_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..',
                                     'data/features/Aastha Bist_CV.json'),
}

GET_FEATURES_FROM_PDF_BATCH = {
    'SOURCE_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/pdfs/'),
    'DESTINATION_PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data/features/'),
}

MGMT_COMMANDS_ALIASES = {
    'html_to_ordered_sentences': 'src.common.commands.html_to_ordered_sentences',
    'pdf_to_html': 'src.common.commands.pdf_to_html',
    'pdf_to_text_batch': 'src.common.commands.pdf_to_text_batch',
    'get_features_from_pdf': 'src.common.commands.get_features_from_pdf',
    'get_features_from_pdf_batch': 'src.common.commands.get_features_from_pdf_batch',
    'plot_words_by_point_grid': 'src.common.commands.plot_words_by_point_grid',
}