"""Imported modules"""
import logging
import os
from pprint import pprint

from utils import analyze, filter_high_confidence_results, anonymize, get_response

environment = os.environ.get('ENVIRONMENT', 'local')
if environment == 'production':
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, _context):
    """Handles the lambda request"""
    logger.info("Processing event: %event", event.get('name', None))

    try:
        entities = event.get('entities', ["PERSON", "PHONE_NUMBER", "CREDIT_CARD"])
        user_language = event.get('user_language', 'fr')
        text = event.get('text', '')

        results = analyze(text, entities, user_language)
        filtered_results = filter_high_confidence_results(results)
        if filtered_results:
            anonymized_text = anonymize(text, filtered_results)
        else:
            anonymized_text = text

        response = get_response(text, anonymized_text)
        pprint(response)
        return response
    except Exception as e:
        logger.error("Error processing event: %event", e)
        return e
