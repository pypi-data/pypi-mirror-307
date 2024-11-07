"""Evaluators to optimize task: example-tweet.

THIS IS A TEMPLATE FOR YOU TO CHANGE!

Evaluators compute scores for prompts run over the configured dataset:
https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/datasets/db688c10-764b-42ec-acce-4d62419600ed
"""
from langchain_core.messages import AIMessage
from langsmith.schemas import Run, Example

# Modify these evaluators to measure the requested criteria.
# For most prompt optimization tasks, run.outputs["output"] will contain an AIMessage
# (Advanced usage) If you are defining a custom system to optimize, then the outputs will contain the object returned by your system


def example_evaluator(run: Run, example: Example) -> dict:
    """An example evaluator. Larger numbers are better."""
    predicted: AIMessage = run.outputs["output"]

    result = str(predicted.content)
    score = int("#" not in result)
    return {
        "key": "tweet_omits_hashtags",
        "score": score,
        "comment": "Pass: tweet omits hashtags"
        if score == 1
        else "Fail: omit all hashtags from generated tweets",
    }


evaluators = [example_evaluator]
