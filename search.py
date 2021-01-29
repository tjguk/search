#!python3
import os, sys
import glob
import itertools
import re

def term_as_regex(term):
    term = term.replace("*", r"[\w\.]*")
    term = term.replace("?", r"[\w\.]")
    return term

def find_matches(filepath, terms):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    finder = re.compile("|".join(terms), flags=re.IGNORECASE)
    found = set(finder.findall(text))
    found_terms = set(t for t in terms if any(re.match(t, f, flags=re.IGNORECASE) for f in found))
    score = len(found_terms & terms)

    return score

def main(filepattern, *search_for):
    search_terms = set(term_as_regex(t) for t in search_for)
    print(search_terms)

    file_scores = {}
    for filepath in glob.glob(filepattern):
        score = find_matches(filepath, search_terms)
        if score:
            file_scores[filepath] = score

    for filepath, score in sorted(file_scores.items(), key=lambda x: x[-1], reverse=True):
        print(filepath, "=>", score)

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))