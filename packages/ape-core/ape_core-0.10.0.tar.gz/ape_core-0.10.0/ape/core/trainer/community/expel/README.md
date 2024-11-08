# ExpelTrainer

**ExpelTrainer** is inspired by the paper [Expel](https://arxiv.org/abs/2308.10144), but implemented as a prompt optimization algorithm.

## Description

The original **Expel** method is an improvement over [Reflexion](https://arxiv.org/abs/2303.11366), drawing inspiration from the human learning process. It extracts insights from three types of groups: the successful group, the unsuccessful group, and the comparison group.

- **Successful Group**: A group of examples where the model succeeds, designed to extract insights on general success strategies.
- **Unsuccessful Group**: A group of examples where the model fails, aimed at identifying recurring failure patterns.
- **Comparison Group**: A group that compares successful and failed outcomes for the same example, helping to determine the reasons behind success or failure.

Compared to Reflexion, Expel extracts a wider range of insights. In this implementation, Expel is combined with [TextGrad](https://arxiv.org/abs/2406.07496). We extract insights from successful and unsuccessful groups and use these insights to iteratively optimize the prompt.

## Motivation for Developing this Method

Expel is one of the most data-driven prompt optimization methods, learning significantly more from the training dataset compared to other methods—even more than TextGrad. Team Weavel tested Expel using the Python programming benchmark `humaneval` in 2023.09, and found that Expel improved performance by 7-9%.
Though originally a variation of Reflexion, Expel can also be implemented as a variation of **TextGrad** and applied to further improve new prompt generation and optimization tasks.

## Key Differences

### Instruction Improvement Only

The original Expel paper includes few-shot examples that are saved from the training dataset and dynamically retrieved at test time. While this dynamic retrieval technique is well-known and effective, as seen in papers like [MedPrompt](https://arxiv.org/abs/2311.16452), we chose to implement only the instruction improvement part for ExpelTrainer. This decision aligns with Ape’s focus as a hub for prompt optimization methods, keeping it streamlined for prompt improvement.

## Benchmark Performance

For benchmark performance, visit [link](../../../../../../../experiments/trainer/community/expel/RESULT.md).
