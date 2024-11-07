# YesNo solver

exposes a Yes No parser as a solver plugin

> **NOT** meant to be used within persona framework

this solver only indicates if the user answered "yes" or "no" to a yes/no prompt

> ie, it is indicated to **parse** user responses

## Install

`pip install ovos-solver-yes-no-plugin`

## Usage

Standalone usage

```python
from ovos_yes_no_solver import YesNoSolver

bot = YesNoSolver()
assert bot.spoken_answer("i agree") == "yes"
assert bot.spoken_answer("no way") == "no"
```


more examples from unittests
```python
from ovos_yes_no_solver import YesNoSolver

solver = YesNoSolver()

def test_utt(text, expected):
    res = solver.match_yes_or_no(text, "en-us")
    return res == expected

test_utt("yes", True)
test_utt("no", False)
test_utt("no way", False)
test_utt("don't think so", False)
test_utt("i think not", False)
test_utt("that's affirmative", True)
test_utt("beans", None)
test_utt("no, but actually, yes", True)
test_utt("yes, but actually, no", False)
test_utt("yes, yes, yes, but actually, no", False)
test_utt("please", True)
test_utt("please don't", False)
test_utt("I agree", True)
test_utt("agreed", True)
test_utt("I disagree", False)
test_utt("disagreed", False)

# test "neutral_yes" -> only count as yes word if there isn't a "no" in sentence
test_utt("no! please! I beg you", False)
test_utt("yes, i don't want it for sure", False)
test_utt("please! I beg you", True)
test_utt("i want it for sure", True)
test_utt("obviously", True)
test_utt("indeed", True)
test_utt("no, I obviously hate it", False)

# test "neutral_no" -> only count as no word if there isn't a "yes" in sentence
test_utt("do I hate it when companies sell my data? yes, that's certainly undesirable", True)
test_utt("that's certainly undesirable", False)
test_utt("yes, it's a lie", True)
test_utt("no, it's a lie", False)
test_utt("he is lying", False)
test_utt("correct, he is lying", True)
test_utt("it's a lie", False)
test_utt("you are mistaken", False)
test_utt("that's a mistake", False)
test_utt("wrong answer", False)

# test double negation
test_utt("it's not a lie", True)
test_utt("he is not lying", True)
test_utt("you are not mistaken", True)
test_utt("tou are not wrong", True)
```