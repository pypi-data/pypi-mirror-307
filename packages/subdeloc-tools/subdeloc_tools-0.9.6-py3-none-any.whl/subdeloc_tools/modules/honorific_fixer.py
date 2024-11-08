import pysubs2
from typing import Dict, Union, List
from subdeloc_tools.common.types.types import MatchesVar

def load_ass(file_path:str) -> pysubs2.SSAFile:
	"""
	Load subtitle file to pysubs2.
	"""
	try:
		subs = pysubs2.load(file_path)
		return subs
	except Exception as e:
		print(f"Error loading file '{file_path}': {e}")
		return None

def prepare_edit_dict(dt: dict) -> Dict[str, str]:
	"""
	Create a dict of every line by the line number.
	"""
	result = {}
	for i in dt:
		for j in i["original"]:
			result[str(j["nl"])] = j["original"]

	return result

def fix_original(file: str, fixed: List[MatchesVar], new_name="edited.ass") -> str:
	"""
	Edit the subtitle file replacing the lines for the new ones.
	"""
	try:
		subs = load_ass(file)
		res = prepare_edit_dict(fixed)

		ks = res.keys()

		for nl,line in enumerate(subs):
			if str(nl) in ks:
				line.text = res[str(nl)]

		subs.save(new_name)
		return new_name
	except Exception as e:
		print(e)
		return ''
