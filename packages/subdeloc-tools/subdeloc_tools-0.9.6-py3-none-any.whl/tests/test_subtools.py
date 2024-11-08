import unittest
from subdeloc_tools import subtools as st
from tests.constants.subtools import *
from tests.constants.pairsubs import RESULT
import os
import json

class TestSubTools(unittest.TestCase):

    def test_init(self):
        ST = st.SubTools(
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"eng.ass", 
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"jap.ass", 
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"names.json", 
            "."+os.sep+"subdeloc_tools"+os.sep+"samples"+os.sep+"honorifics.json", 
            "output.ass"
        )
        self.assertEqual(ST.main_sub, "."+os.sep+"tests"+os.sep+"files"+os.sep+"eng.ass")
        self.assertEqual(ST.ref_sub, "."+os.sep+"tests"+os.sep+"files"+os.sep+"jap.ass")
        self.assertEqual(ST.honorifics["honorifics"]["san"]["kanjis"][0], "さん")
        self.assertEqual(ST.names["Hello"], "こんにちは")

    def test_search_honorifics(self):
        ST = st.SubTools(
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"eng.ass", 
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"jap.ass", 
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"names.json", 
            "."+os.sep+"subdeloc_tools"+os.sep+"samples"+os.sep+"honorifics.json", 
            "output.ass"
        )
        s = ST.search_honorifics(RESULT)
        self.assertEqual(s[1]['original'][0]['original'], "World-dono")

    def test_search_tokens(self):
        ST = st.SubTools(
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"eng.ass", 
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"esp.ass", 
            "."+os.sep+"tests"+os.sep+"files"+os.sep+"names.json", 
            "."+os.sep+"subdeloc_tools"+os.sep+"samples"+os.sep+"honorifics.json", 
            "output.ass", 
            jap_ref=False
        )
        s = ST.search_honorifics(RESULT)
        self.assertEqual(s[1]['original'][0]['original'], "World-dono")

    def test_default_honorifics_file(self):
        hfile = st.SubTools.get_default_honorifics_file()
        with open("."+os.sep+"subdeloc_tools"+os.sep+"samples"+os.sep+"honorifics.json", encoding='utf-8') as f:
            local_file = json.load(f)

        self.assertEqual(hfile, local_file)

if __name__ == "__main__":
    unittest.main()