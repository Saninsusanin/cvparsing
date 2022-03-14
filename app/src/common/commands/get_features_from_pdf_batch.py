from src.settings import GET_FEATURES_FROM_PDF_BATCH
from src.common.utils import transform, pdf_to_json_paths
from src.feature_extraction.feature_extractor import feature_extractor


def do():
    transform(
        GET_FEATURES_FROM_PDF_BATCH['SOURCE_PATH'],
        GET_FEATURES_FROM_PDF_BATCH['DESTINATION_PATH'],
        feature_extractor,
        pdf_to_json_paths
    )