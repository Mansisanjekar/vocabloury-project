"""
Dictionary API integration for VocabLoury application
"""

import requests
from typing import Dict, List, Optional
from config.settings import DICTIONARY_API_BASE_URL, DATAMUSE_API_BASE_URL


class DictionaryAPI:
    """Free Dictionary API integration"""
    
    @staticmethod
    def get_word_definition(word: str) -> Optional[Dict]:
        """Get word definition from Free Dictionary API"""
        try:
            response = requests.get(f"{DICTIONARY_API_BASE_URL}/{word.lower()}")
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0]
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    @staticmethod
    def get_word_synonyms(word: str) -> List[str]:
        """Get synonyms using Datamuse API"""
        try:
            response = requests.get(f"{DATAMUSE_API_BASE_URL}?rel_syn={word}")
            if response.status_code == 200:
                data = response.json()
                return [item['word'] for item in data[:10]]  # Top 10 synonyms
            return []
        except Exception as e:
            print(f"Synonyms API Error: {e}")
            return []
    
    @staticmethod
    def get_word_antonyms(word: str) -> List[str]:
        """Get antonyms using Datamuse API"""
        try:
            response = requests.get(f"{DATAMUSE_API_BASE_URL}?rel_ant={word}")
            if response.status_code == 200:
                data = response.json()
                return [item['word'] for item in data[:10]]  # Top 10 antonyms
            return []
        except Exception as e:
            print(f"Antonyms API Error: {e}")
            return []
    
    @staticmethod
    def get_words_by_topic(topic: str, max_words: int = 100) -> List[str]:
        """Get words related to a specific topic"""
        try:
            response = requests.get(f"{DATAMUSE_API_BASE_URL}?topics={topic}&max={max_words}")
            if response.status_code == 200:
                data = response.json()
                return [item['word'] for item in data if len(item['word']) > 2]
            return []
        except Exception as e:
            print(f"Topic API Error: {e}")
            return []
    
    @staticmethod
    def get_words_by_alphabet(letter: str, max_words: int = 50) -> List[str]:
        """Get words starting with a specific letter"""
        try:
            response = requests.get(f"{DATAMUSE_API_BASE_URL}?sp={letter}*&max={max_words}")
            if response.status_code == 200:
                data = response.json()
                return [item['word'] for item in data if len(item['word']) > 2]
            return []
        except Exception as e:
            print(f"Alphabet API Error: {e}")
            return []
