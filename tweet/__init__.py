import check50
import uva.check50.py
import check50.internal
import re
import os
import sys

check50.internal.register.before_every(lambda : sys.path.append(os.getcwd()))
check50.internal.register.after_every(lambda : sys.path.pop())

@check50.check()
def exists():
    """tweet.py exists."""
    check50.include("helpers.py", "negative_words.txt", "positive_words.txt", "trump.txt")
    check50.exists("tweet.py")


@check50.check(exists)
def compiles():
    """tweet.py compiles."""
    uva.check50.py.compile("tweet.py")
    module = uva.check50.py.run("tweet.py").module

    for attr in ["classify", "positive_word", "bad_days"]:
        if not hasattr(module, attr):
            raise check50.Failure(f"Expected tweet.py to have a function called {attr} !")


@check50.check(compiles)
def correct_positive():
    """correct number of positive tweets."""
    check_classify("positive", 417)


@check50.check(compiles)
def correct_negative():
    """correct number of negative tweets."""
    check_classify("negative", 130)


@check50.check(compiles)
def correct_neutral():
    """correct number of neutral tweets."""
    check_classify("neutral", 450)


@check50.check(compiles)
def best_words():
    """correct top five positive words"""
    positive_word = uva.check50.py.run("tweet.py").module.positive_word

    import helpers
    dates, tweets = helpers.read_tweets("trump.txt")
    positives = helpers.read_words("positive_words.txt")

    with uva.check50.py.capture_stdout() as stdout:
        positive_word(tweets, positives)

    out = stdout.getvalue()
    top5 = ["great", "trump", "thank", "good", "honor"]

    for word in top5:
        if word not in out:
            raise check50.Mismatch(f"{word}", out)

    for word in set(positives) - set(top5) - {"positive", "top"}:
        if word and word in out:
            raise check50.Failure(f"Did not expect {word} in top 5!")

    return out


@check50.check(best_words)
def occurance_words(out):
    """correct occurance of top five positive words"""
    for word, occ in [("great", 245), ("trump", 88), ("thank", 82), ("good", 55), ("honor", 39)]:
        match = re.search(f"{word}[^\n^\d]*(\d+)", out)
        if not match.groups() or not int(match.groups()[0]) == occ:
            raise check50.Mismatch(f"{word} {occ}", out)


def check_classify(type, n):
    classify = uva.check50.py.run("tweet.py").module.classify

    import helpers
    dates, tweets = helpers.read_tweets("trump.txt")

    positives = helpers.read_words("positive_words.txt")
    negatives = helpers.read_words("negative_words.txt")

    with uva.check50.py.capture_stdout() as stdout:
        classify(tweets, positives, negatives)

    out = stdout.getvalue()
    match = re.search(fr"{type}[^\n^\d]*(\d+)", out)

    if not match or int(match.groups()[0]) != n:
        raise check50.Mismatch(f"{type}: {n}", out)