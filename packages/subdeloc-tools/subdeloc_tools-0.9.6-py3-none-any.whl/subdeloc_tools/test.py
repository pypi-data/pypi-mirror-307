"""
That's Naruto-kun						それ和ナルトくんです
Is that Naruto-kun?						それはナルトくんですか？
Those are Naruto-kun and Sakura-chan	あれはナルトくんとサクラちゃんす
Are those Naruto-kun and Sakura-chan?	あれはナルトくんとサクラちゃんすか？

Hinata-san 							ヒナタさん
Hinata-oneesan 						ヒナタお姉さん
Ino-san and Hinata-oneesan 			いのさんとヒナタお姉さん

Is it Naruto-kun or Naruto-san?			xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
---------------------------------------------
姫			hime
ヒナタ		Hinata
ナルト		Naruto
サクラ		Sakura
いの			Ino

それ 和 ナルト です
それはナ ルト君 ですか？

あれは ナルト君 と サクラちゃん す
あれは ナルト君 と サクラちゃん すか？
"""

import re

class Fixer:
	def __init__(self):
		pass

names = {
	"Naruto": "ナルト",
	"Sakura": "サクラ",
	"Ino": "いの	",
	"Hinata": "ヒナタ"
}

honorifics = {
	"san": "さん",
	"oneesan": "お姉さん",
	"kun": "くん",
	"chan": "ちゃん"
}

pair = {
	"orig": "That's Naruto",
	"ref": "それ和ナルトくんです"
}

def get_kanji_honor_list():
	return sorted(list(honorifics.values()), key=len, reverse=True)

def get_name_list():
	return sorted(list(names.values()), key=len, reverse=True)

def find_exact_name_in_string(name, string):
	pattern = r"\b" + re.escape(name) + r"\b"
	return bool(re.search(pattern, string, flags=re.I))

def check_names(sentence):
	for n in sorted(list(names.keys()), key=len, reverse=True):
		if find_exact_name_in_string(n, sentence):
			yield n

def search_honor(sentence, name):
	for honor in honorifics:
		if name+honorifics[honor] in sentence:
			yield honor

def replace_word(sentence, name, honorific):
	sentence = re.sub(name, f"{name}-{honorific}", sentence, flags=re.I)
						
	# for alternative in self.honorifics["honorifics"][honorific]["alternatives"]:
	# 	sentence = re.sub(alternative, "", sentence, flags=re.I)

	sentence = sentence.strip()

	return sentence

def flow(pair):
	sentence = ""
	for name in check_names(pair["orig"]):
		print("Found:", name)
		for honor in search_honor(pair["ref"], names[name]):
			print("Found:", honor)
			sentence = replace_word(pair["orig"], name, honor)
	return sentence

def main():
	pair = {
		"orig": "That's Naruto",
		"ref": "それ和ナルトくんです"
	}
	print(flow(pair))

if __name__ == '__main__':
	main()