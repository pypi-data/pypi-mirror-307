import re

from subdeloc_tools.common.types.types import MatchesVar
from subdeloc_tools.common.decorators.decorators import decremental

class Fixer:
	def __init__(self, honorifics_json: dict, names: dict, pair: MatchesVar=None, tokens: bool=False):
		self.honorifics_json = honorifics_json["honorifics"]
		self.honorifics = self.prepare_honorifics()
		self.names = names
		self.pair = pair
		self.tokens = tokens

		self.honor_list = self.get_kanji_honor_list()
		self.names_list = self.get_name_list()

	def update_pair(self, pair: MatchesVar):
		self.pair = pair

	def prepare_honorifics(self) -> dict:
		return {i:self.honorifics_json[i]["kanjis"] for i in self.honorifics_json}

	@decremental
	def get_kanji_honor_list(self) -> list:
		return list(self.honorifics.keys())

	@decremental
	def get_name_list(self) -> list:
		return list(self.names.keys())

	def find_exact_name_in_string(self, name: str, string: str) -> bool:
		pattern = r"\b" + re.escape(name) + r"\b"
		return bool(re.search(pattern, string, flags=re.I))

	def find_prefix_honor(self, prefix: str, string: str) -> bool:
		pattern = r"\b" + re.escape(prefix) + r"\s"
		return bool(re.search(pattern, string, flags=re.I))

	def check_names(self, sentence: str) -> str:
		for n in self.names_list:
			if self.find_exact_name_in_string(n, sentence):
				yield n

	def replace_word(self, k: str, v: str, text: str) -> str:
		return re.sub(k, v, text, flags=re.I)

	def replace_english_honorifics(self, sentence: str, honorific: str) -> str:
		for alternative in self.honorifics_json[honorific]["alternatives"]:
			if self.find_prefix_honor(alternative, sentence):
				sentence = re.sub(alternative+" ", "", sentence, flags=re.I)
				break

		return sentence

	def fix_sentence(self, sentence: str, name: str, new_word: str, honorific: str) -> str:
		sentence = self.replace_word(name, new_word, sentence)
		sentence = self.replace_english_honorifics(sentence, honorific)
		sentence = sentence.strip()

		return sentence

	# -------------------------- Honor ----------------------------

	def search_honor(self, sentence: str, name: str) -> str:
		for honor in self.honor_list:
			for h in self.honorifics[honor]:
				if name+h in sentence:
					yield honor

	# -------------------- Tokens ---------------------------------
	def search_tokens(self, sentence: str, name: str):
		for honor in self.honor_list:
			if name+"-"+honor in sentence:
				yield honor
	# -------------------------------------------------------------

	def flow_honor(self, pair: MatchesVar) -> MatchesVar:
		for orig in pair["original"]:
			sentence = orig["text"]
			original = orig["original"]
			for name in self.check_names(sentence):
				for ref in pair["reference"]:
					honor = next(self.search_honor(ref["text"], self.names[name]), None)
					if honor:
						original = self.fix_sentence(original, name, f"{name}-{honor}", honor)
						break

			orig["original"] = original
		return pair

	def flow_tokens(self, pair: MatchesVar) -> MatchesVar:
		for orig in pair["original"]:
			sentence = orig["text"]
			original = orig["original"]
			for name in self.check_names(sentence):
				for ref in pair["reference"]:
					honor = next(self.search_tokens(ref["text"], name), None)
					if honor:
						original = self.fix_sentence(original, name, f"{name}-{honor}", honor)
						break

			orig["original"] = original
		return pair

	def fix(self) -> MatchesVar:
		if self.tokens:
			return self.flow_tokens(self.pair)
		else:
			return self.flow_honor(self.pair)