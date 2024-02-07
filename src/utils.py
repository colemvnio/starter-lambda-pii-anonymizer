"""Imported modules"""
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

from presidio_anonymizer import AnonymizerEngine

_ANALYZER = None
_ANONYMIZER = None


def get_response(original_text, anonymized_text):
    """Returns a formatted response."""
    data = {
        "anonymized": False,
    }
    if anonymized_text and len(anonymized_text.items):
        data = {
            "anonymized": True,
            "anonymized_items": anonymized_text.items,
            "anonymized_text": anonymized_text.text,
            "original_text": original_text
        }

    return data


def filter_high_confidence_results(results, threshold=0.7):
    """Retains high confidence results to anonymize"""
    return [result for result in results if result.score >= threshold]


def get_analyzer():
    """Returns the configured Presidio Analyzer Engine"""
    global _ANALYZER
    if _ANALYZER is None:
        supported_languages = ["en"]
        # "fr_core_news_sm", "en_core_web_sm"
        nlp_config = {
            "nlp_engine_name": "spacy",
            "models": [
                {"lang_code": "en", "model_name": "en_core_web_sm"},
            ],
        }

        provider = NlpEngineProvider(nlp_configuration=nlp_config)
        nlp_engine = provider.create_engine()
        return AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=supported_languages)


def get_anonymizer():
    """Returns the configured Presidio Anonymizer Engine"""
    global _ANONYMIZER
    if _ANONYMIZER is None:
        _ANONYMIZER = AnonymizerEngine()
    return _ANONYMIZER


def analyze(text, entities, user_language):
    """Generates score results based on the text parameter for desired entities and user language"""
    analyzer = get_analyzer()
    results = analyzer.analyze(text=text, entities=entities, language=user_language)
    return results


def anonymize(text, analyzer_results):
    """Following the analysis, anonymizes the data"""
    anonymizer = get_anonymizer()
    return anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
