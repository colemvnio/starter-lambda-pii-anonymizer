from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

_analyzer = None
_anonymizer = None


def get_response(original_text, anonymized_text):
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
    return [result for result in results if result.score >= threshold]


def get_analyzer():
    global _analyzer
    if _analyzer is None:
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
    global _anonymizer
    if _anonymizer is None:
        _anonymizer = AnonymizerEngine()
    return _anonymizer


def analyze(text, entities, user_language):
    analyzer = get_analyzer()
    results = analyzer.analyze(text=text, entities=entities, language=user_language)
    return results


def anonymize(text, analyzer_results):
    anonymizer = get_anonymizer()
    return anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
