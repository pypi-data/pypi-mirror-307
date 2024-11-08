import pysubs2
import json
import re
import os
import logging

from typing import Dict, Union, List, Tuple
from subdeloc_tools.common.types.types import IntervalVar, MatchesVar, SubtitleSetVar

MARGIN = int(os.getenv("PAIR_MARGIN", 1000))

#logger = logging.getLogger(__name__)
#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

def load_ass(file_path: str) -> pysubs2.SSAFile:
    try:
        subs = pysubs2.load(file_path)
        return subs
    except Exception as e:
        print(f"Error loading file '{file_path}': {e}")
        return None

def sanitize_string(string: str) -> str:
    # Match substrings enclosed in {}
    pattern = r"\{([^{}]*)\}"

    # Replace all occurrences of the pattern using the replace function
    result = re.sub(pattern, "", string)
    result = re.sub(r"\s\\.", "", result)
    result = re.sub(r"\\.", " ", result)
    return result

# Intersect functions
def check_interval_conditions(interval: IntervalVar, other_interval: IntervalVar) -> Tuple[bool, bool]:
    # Check for full containment
    fully_contained = (
        (interval['start'] >= other_interval['start'] and interval['end'] <= other_interval['end']) or
        (other_interval['start'] >= interval['start'] and other_interval['end'] <= interval['end'])
    )

    # Check if both start and end times are within the ±2 seconds margin
    within_margin = (
        abs(interval['start'] - other_interval['start']) <= MARGIN or 
        abs(interval['end'] - other_interval['end']) <= MARGIN
    )

    return fully_contained, within_margin

def find_matches(interval: IntervalVar, other_set: List[IntervalVar]) -> List[IntervalVar]:
    matches = []
    for idx, other_interval in enumerate(other_set):
        
        fully_contained, within_margin = check_interval_conditions(interval, other_interval)

        if fully_contained or within_margin:
            matches.append(other_interval)

        # Break happens when next interval is after the end of current, and not within the margin
        if other_interval["start"] >= interval["end"] and not within_margin:
            break

    return matches

def process_interval(interval: IntervalVar, other_set: IntervalVar, key_1: str='original') -> Tuple[MatchesVar, int]:
    matches = find_matches(interval, other_set)

    key_2 = 'reference' if key_1 == 'original' else 'original'

    if matches:
        group_start = min([interval['start']] + [b['start'] for b in matches])
        group_end = max([interval['end']] + [b['end'] for b in matches])

        return {
            'start': group_start,
            'end': group_end,
            key_1: [interval],
            key_2: matches
        }, len(matches)

def update_matches(matches: MatchesVar, interval: IntervalVar, original:bool) -> bool:
    if matches:
        if original:
            fully_contained, within_margin = check_interval_conditions(interval, matches["reference"][-1])
            if fully_contained or within_margin:
                matches["original"].append(interval)
        else:
            fully_contained, within_margin = check_interval_conditions(interval, matches["original"][-1])
            if fully_contained or within_margin:
                matches["reference"].append(interval)
    return True

def find_intersections(set_a: SubtitleSetVar, set_b: SubtitleSetVar) -> List[MatchesVar]:
    intersections = []

    # Pointers for iterating through set A and set B
    i, j = 0, 0

    while i < len(set_a) and j < len(set_b):
        # Get the current intervals from both sets
        interval_a = set_a[i]
        interval_b = set_b[j]

        # Check interval conditions
        fully_contained, within_margin = check_interval_conditions(interval_a, interval_b)

        if fully_contained or within_margin:
            sza = interval_a["end"] - interval_a["start"]
            szb = interval_b["end"] - interval_b["start"]

            if sza >= szb:
                matches, carry = process_interval(interval_a, set_b[j:], 'original')
                j += carry
                i += 1
            else:
                matches, carry = process_interval(interval_b, set_a[i:], 'reference')
                i += carry
                j += 1
            if matches:
                intersections.append(matches)
        else:
            if interval_a["start"] <= interval_b["start"]:
                update_matches((intersections or [None])[-1], interval_a, True)
                i += 1
            else:
                update_matches((intersections or [None])[-1], interval_b, False)
                j += 1

    # Do missing step for subs at the end.
    if i < len(set_a):
        while i < len(set_a):
            interval_a = set_a[i]
            update_matches((intersections or [None])[-1], interval_a, True)
            i += 1
    else:
        while j < len(set_b):
            interval_b = set_b[j]
            update_matches((intersections or [None])[-1], interval_b, False)
            j += 1

    return intersections

# Main methods
def group_lines_by_time(sub1: pysubs2.SSAFile, sub2: pysubs2.SSAFile) -> List[MatchesVar]:
    intervals = []
    sub_pivot = sub2
    current = 0
    set_a = []
    set_b = []

    for nl,line in enumerate(sub1):
        if line.type == "Dialogue":
            set_a.append({"start": line.start, "end": line.end, "text":sanitize_string(line.text), "original":line.text, "nl": nl})
    for nl,line in enumerate(sub2):
        if line.type == "Dialogue":
            set_b.append({"start": line.start, "end": line.end, "text":sanitize_string(line.text), "original":line.text, "nl": nl})

    set_a.sort(key=lambda d: d["start"])
    set_b.sort(key=lambda d: d["start"])

    return find_intersections(set_a, set_b)

def pair_files(s1: str, s2: str) -> List[MatchesVar]:
    sub1 = load_ass(s1)
    sub2 = load_ass(s2)

    res = group_lines_by_time(sub1, sub2)

    return res