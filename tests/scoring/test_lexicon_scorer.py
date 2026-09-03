from scoring.lexicon_scorer import LexiconScorer


def test_positive_text_scores_positive():
    scorer = LexiconScorer()
    assert scorer.score_tone("Revenue increased and growth was strong and record.") == "positive"


def test_uncertain_text_scores_cautious():
    scorer = LexiconScorer()
    assert scorer.score_tone("Results may be volatile and are uncertain and risk-laden.") == "cautious"


def test_neutral_text_scores_neutral():
    scorer = LexiconScorer()
    assert scorer.score_tone("The company operates in three regions.") == "neutral"


def test_uncertainty_score_is_zero_for_no_matches():
    scorer = LexiconScorer()
    assert scorer.uncertainty_score("The sky is blue today.") == 0.0


def test_uncertainty_score_nonzero_for_matches():
    scorer = LexiconScorer()
    assert scorer.uncertainty_score("This may or could depend on conditions.") > 0.0
