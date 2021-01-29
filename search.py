#!python3
import os, sys
import glob
import itertools
import re

def find_matches(filepath, terms):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    finds = {}
    for i in re.finditer("|".join(terms), text):
        match = i.group()
        matched_from, _ = i.span()
        finds.setdefault(match, set()).add(matched_from)

    if finds:
        combos = list(itertools.product(finds.items()))
        for c in combos:
            print(c)
        proximities = [sum(abs(a - b) for (a, b) in itertools.product(p)) for p in combos]
        closest_match = min(proximities)
        return closest_match
    else:
        return None

def main(filepattern, *search_for):
    file_scores = {}
    for filepath in glob.glob(filepattern):
        score = find_matches(filepath, search_for)
        if score is not None:
            file_scores[filepath] = score

    for filepath, score in sorted(file_scores.items(), key=lambda x: x[-1]):
        print(filepath, "=>", score)

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))