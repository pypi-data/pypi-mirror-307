import unittest
import os
import json

from subdeloc_tools.modules import honorific_utils

class TestHonorificUtils(unittest.TestCase):
    def setUp(self):
        self.basic_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "That's Naruto",
                            "original": "That's Naruto",
                            "nl": 1
                        }
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "それ和ナルトくんです",
                            "original": "それ和ナルトくんです",
                            "nl": 1
                        }
                    ],
                },
                "result": "That's Naruto-kun"
            }
        self.question_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Is that Naruto?",
                            "original": "Is that Naruto?",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "それはナルトくんですか？",
                            "original": "それはナルトくんですか？",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Is that Naruto-kun?"
            }
        self.double_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Those are Naruto and Sakura",
                            "original": "Those are Naruto and Sakura",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "あれはナルトくんとサクラちゃんす",
                            "original": "あれはナルトくんとサクラちゃんす",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Those are Naruto-kun and Sakura-chan"
            }
        self.double_question_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Are those Naruto and Sakura?",
                            "original": "Are those Naruto and Sakura?",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "あれはナルトくんとサクラちゃんすか？",
                            "original": "あれはナルトくんとサクラちゃんすか？",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Are those Naruto-kun and Sakura-chan?"
            }
        self.single_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Ms. Hinata",
                            "original": "Ms. Hinata",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "ヒナタさん",
                            "original": "ヒナタさん",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Hinata-san"
            }
        self.contained_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Big sis Hinata",
                            "original": "Big sis Hinata",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "ヒナタお姉さん",
                            "original": "ヒナタお姉さん",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Hinata-oneesan"
            }
        self.single_and_contained_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Ms. Ino and sis Hinata",
                            "original": "Ms. Ino and sis Hinata",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "いのさんとヒナタお姉さん",
                            "original": "いのさんとヒナタお姉さん",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Ino-san and Hinata-oneesan"
            }

        self.basic_token_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Hello Naruto",
                            "original": "Hello Naruto",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Hola Naruto-kun",
                            "original": "Hola Naruto-kun",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Hello Naruto-kun"
            }
        self.question_token_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Are you Naruto?",
                            "original": "Are you Naruto?",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "¿Eres Naruto-kun?",
                            "original": "¿Eres Naruto-kun?",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Are you Naruto-kun?"
            }
        self.double_token_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Glad you're both together, Naruto and Ino",
                            "original": "Glad you're both together, Naruto and Ino",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Gusto que esten juntos, Naruto-kun e Ino-chan",
                            "original": "Gusto que esten juntos, Naruto-kun e Ino-chan",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Glad you're both together, Naruto-kun and Ino-chan"
            }
        self.double_question_token_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Are you together, Naruto and Ino?",
                            "original": "Are you together, Naruto and Ino?",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Estan juntos, Naruto-kun e Ino-chan?",
                            "original": "Estan juntos, Naruto-kun e Ino-chan?",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Are you together, Naruto-kun and Ino-chan?"
            }
        self.single_token_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Ino",
                            "original": "Ino",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Ino-san",
                            "original": "Ino-san",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Ino-san"
            }
        self.contained_token_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Hinata",
                            "original": "Hinata",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Hinata-oneesan",
                            "original": "Hinata-oneesan",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Hinata-oneesan"
            }
        self.single_and_contained_token_pair = {
                "pair": {
                    "start": 0,
                    "end": 1000,
                    "original": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Ino and Hinata",
                            "original": "Ino and Hinata",
                            "nl": 1,
                        },
                    ],
                    "reference": [
                        {
                            "start": 0,
                            "end": 1000,
                            "text": "Ino-san y Hinata-oneesan",
                            "original": "Ino-san y Hinata-oneesan",
                            "nl": 1,
                        },
                    ],
                },
                "result": "Ino-san and Hinata-oneesan"
            }

        with open("."+os.sep+"subdeloc_tools"+os.sep+"samples"+os.sep+"honorifics.json", encoding='utf-8') as f:
            self.honorifics_json = json.load(f)
        with open("."+os.sep+"tests"+os.sep+"files"+os.sep+"test_names.json", encoding='utf-8') as f:
            self.names_json = json.load(f)

    def test_check_basic(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.basic_pair["pair"])
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.basic_pair["result"])

    def test_check_question(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.question_pair["pair"])
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.question_pair["result"])

    def test_check_double(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.double_pair["pair"])
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.double_pair["result"])

    def test_check_double_question(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.double_question_pair["pair"])
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.double_question_pair["result"])

    def test_check_single(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.single_pair["pair"])
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.single_pair["result"])

    def test_check_contained(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.contained_pair["pair"])
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.contained_pair["result"])

    def test_check_single_and_contained(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.single_and_contained_pair["pair"])
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.single_and_contained_pair["result"])

    # --------------------------------------------------------------------------------------------------------------------

    def test_check_basic_token(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.basic_token_pair["pair"], tokens=True)
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.basic_token_pair["result"])

    def test_check_question_token(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.question_token_pair["pair"], tokens=True)
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.question_token_pair["result"])

    def test_check_double_token(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.double_token_pair["pair"], tokens=True)
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.double_token_pair["result"])

    def test_check_double_question_token(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.double_question_token_pair["pair"], tokens=True)
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.double_question_token_pair["result"])

    def test_check_single_token(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.single_token_pair["pair"], tokens=True)
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.single_token_pair["result"])

    def test_check_contained_token(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.contained_token_pair["pair"], tokens=True)
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.contained_token_pair["result"])

    def test_check_single_and_contained_token(self):
        fixer = honorific_utils.Fixer(self.honorifics_json, self.names_json, self.single_and_contained_token_pair["pair"], tokens=True)
        result = fixer.fix()
        self.assertEqual(result["original"][0]["original"], self.single_and_contained_token_pair["result"])

if __name__ == "__main__":
    unittest.main()