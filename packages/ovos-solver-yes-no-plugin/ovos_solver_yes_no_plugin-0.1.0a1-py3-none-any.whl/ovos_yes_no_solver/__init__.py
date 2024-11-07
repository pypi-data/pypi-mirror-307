import json
import os.path
import re
import string
from ovos_plugin_manager.templates.solvers import QuestionSolver
from langcodes import closest_match


class YesNoSolver(QuestionSolver):
    """not meant to be used within persona framework
    this solver only indicates if the user answered "yes" or "no"
    to a yes/no prompt"""
    enable_tx = False  # TODO - dynamic depending on lang
    priority = 100

    def __init__(self, config=None):
        config = config or {}
        self.resources = {}
        super().__init__(config)

    @staticmethod
    def normalize(text: str, lang: str):

        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Converting to Lowercase
        text = document.lower()

        if lang.startswith("en"):
            text = text.replace("don't", "do not")

        return text

    def match_yes_or_no(self, text: str, lang: str):
        _langs = os.listdir(f"{os.path.dirname(__file__)}/res")
        lang2, score = closest_match(lang, _langs)
        if score < 10:
            raise ValueError(f"unsupported lang: {lang}")
        lang = lang2

        if lang not in self.resources:
            resource_file = f"{os.path.dirname(__file__)}/res/{lang}/yesno.json"

            with open(resource_file) as f:
                words = json.load(f)
                self.resources[lang] = {k: [_.lower() for _ in v] for k, v in words.items()}

        text = self.normalize(text, lang)
        toks = [w.strip(string.punctuation) for w in text.split()]

        # if user says yes but later says no, he changed his mind mid-sentence
        # the highest index is the last yesno word
        res = None
        best = -1
        # check if user said yes
        for w in self.resources[lang]["yes"]:
            if w not in toks:
                continue
            idx = text.index(w)
            if idx >= best:
                best = idx
                res = True

        # check if user said no
        for w in self.resources[lang]["no"]:
            if w not in toks:
                continue

            idx = text.index(w)
            if idx >= best:
                best = idx

                # handle double negatives, eg "its not a lie"
                double_negs = [f"{w} {neg}" for neg in self.resources[lang].get("neutral_no", [])]
                for n in double_negs:
                    if n in text and text.index(n) <= idx:
                        res = True
                        break
                else:
                    res = False

        # check if user said no, but only if there isn't a previous yes
        # handles cases such as "yes/no, that's a lie" vs "it's a lie" -> no
        if res is None:
            for w in self.resources[lang].get("neutral_no", []):
                if w not in toks:
                    continue
                idx = text.index(w)
                if idx >= best:
                    best = idx
                    res = False

        # check if user said yes, but only if there isn't a previous no
        # handles cases such as "no! please! I beg you"
        if res is None:
            for w in self.resources[lang].get("neutral_yes", []):
                if w not in toks:
                    continue
                idx = text.index(w)
                if idx >= best:
                    best = idx
                    res = True

        # None - neutral
        # True - yes
        # False - no
        return res

    # abstract Solver methods
    def get_data(self, query, context=None):
        return {"answer": self.get_spoken_answer(query, context)}

    def get_spoken_answer(self, query, context=None):
        context = context or {}
        lang = context.get("lang", "en-us")
        res = self.match_yes_or_no(query, lang)
        if res is None:
            return None
        return "yes" if res else "no"


if __name__ == "__main__":
    cfg = {}
    bot = YesNoSolver(config=cfg)
    print(bot.get_spoken_answer("disagree"))
