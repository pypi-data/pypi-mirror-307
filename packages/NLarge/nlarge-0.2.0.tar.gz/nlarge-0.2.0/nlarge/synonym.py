import logging

import nltk
from nltk.corpus import wordnet

loggers = logging.getLogger(__name__)

class WordNet:
    def __init__(self, lang="eng", is_synonym=True):
        self.lang = lang
        self.is_synonym = is_synonym
        self.model = self.read()

    def read(self):
        try:
            wordnet.synsets("testing")
            return wordnet
        except LookupError:
            nltk.download("wordnet")
            nltk.download("omw-1.4")
            return wordnet

    def predict(self, word, pos=None):
        results = []
        for synonym in self.model.synsets(word, pos=pos, lang=self.lang):
            for lemma in synonym.lemmas(lang=self.lang):
                if self.is_synonym:
                    results.append(lemma.name())
                else:
                    for antonym in lemma.antonyms():
                        results.append(antonym.name())
        return results

    @classmethod
    def pos_tag(cls, tokens):
        try:
            results = nltk.pos_tag(tokens)
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
            nltk.download('averaged_perceptron_tagger_eng')
            results = nltk.pos_tag(tokens)

        return results


class PartOfSpeech:
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"

    pos2con = {
        "n": ["NN", "NNS", "NNP", "NNPS"],
        "v": ["VB", "VBD", "VBG", "VBN", "VBZ", "VBP"],
        "a": ["JJ", "JJR", "JJS", "IN"],
        "s": ["JJ", "JJR", "JJS", "IN"],  # Adjective Satellite
        "r": ["RB", "RBR", "RBS"],
    }

    con2pos = {}
    poses = []
    for key, values in pos2con.items():
        poses.extend(values)
        for value in values:
            if value not in con2pos:
                con2pos[value] = []
            con2pos[value].append(key)

    @staticmethod
    def pos2constituent(pos):
        return PartOfSpeech.pos2con.get(pos, [])

    @staticmethod
    def constituent2pos(con):
        return PartOfSpeech.con2pos.get(con, [])

    @staticmethod
    def get_pos():
        return PartOfSpeech.poses


def init_ppdb_model(dict_path, force_reload=False):
    global PPDB_MODEL

    model_name = os.path.basename(dict_path)
    if model_name in PPDB_MODEL and not force_reload:
        return PPDB_MODEL[model_name]

    model = nmw.Ppdb(dict_path)
    PPDB_MODEL[model_name] = model

    return model


import random

from NLarge.utils.words import WordsUtil


class SynonymAugmenter():
    def __init__(self) -> None:
        loggers.info("SynonymAugmenter initialized")

    def __call__(
        self,
        data,
        aug_src="wordnet",
        model_path=None,
        lang="eng",
        aug_min=1,
        aug_max=10,
        aug_p=0.3,
        stopwords=None,
        tokenizer=None,
        reverse_tokenizer=None,
        stopwords_regex=None,
        force_reload=False,
        verbose=0,
    ):
        if not data or not data.strip():
            return data

        model = WordNet(lang=lang) if aug_src == "wordnet" else None
        if model is None:
            raise ValueError("currently, aug_src can only be `wordnet`.")

        change_seq = 0
        tokenizer = tokenizer or str.split
        reverse_tokenizer = reverse_tokenizer or " ".join
        doc = WordsUtil(data, tokenizer(data))

        original_tokens = doc.get_original_tokens()
        pos = model.pos_tag(original_tokens)
        stopwords = stopwords or []

        def skip_aug(token_idxes, tokens):
            results = []
            for token_idx in token_idxes:
                if tokens[token_idx][1] in ["DT"]:
                    continue

                word_poses = PartOfSpeech.constituent2pos(tokens[token_idx][1])
                if aug_src == "ppdb" and not word_poses:
                    continue

                if word_poses and not any(
                    model.predict(tokens[token_idx][0], pos=pos)
                    for pos in word_poses
                ):
                    continue

                results.append(token_idx)

            return results

        def _get_aug_idxes(tokens):
            aug_cnt = (
                min(len(tokens), int(len(tokens) * aug_p)) if aug_p else aug_max
            )
            word_idxes = [i for i in range(len(tokens)) if i not in stopwords]
            word_idxes = skip_aug(word_idxes, tokens)

            return random.sample(word_idxes, aug_cnt) if word_idxes else []

        aug_idxes = _get_aug_idxes(pos)
        if not aug_idxes:
            return data

        for aug_idx in aug_idxes:
            original_token = original_tokens[aug_idx]
            word_poses = PartOfSpeech.constituent2pos(pos[aug_idx][1])
            candidates = sum(
                (
                    model.predict(pos[aug_idx][0], pos=word_pos)
                    for word_pos in word_poses
                ),
                [],
            )

            candidates = [
                c for c in candidates if c.lower() != original_token.lower()
            ]

            if candidates:
                substitute_token = random.choice(candidates).lower()
                if aug_idx == 0:
                    substitute_token = substitute_token.capitalize()

                change_seq += 1
                doc.add_change_log(
                    aug_idx,
                    new_token=substitute_token,
                    action="substitute",
                    change_seq=change_seq,
                )

        return reverse_tokenizer(doc.get_augmented_tokens())
