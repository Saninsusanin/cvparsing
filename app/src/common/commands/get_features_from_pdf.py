from src.settings import GET_FEATURES_FROM_PDF
from src.feature_extraction.feature_extractor import feature_extractor


def do():
    feature_extractor(
        GET_FEATURES_FROM_PDF['SOURCE_PATH'],
        GET_FEATURES_FROM_PDF['DESTINATION_PATH']
    )