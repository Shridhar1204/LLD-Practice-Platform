# Research Note

## Learner problem

LLD practice is abundant, but evaluation is the difficult part. Community question banks provide many prompts, while structured courses often provide walkthroughs and reference designs. The learner still has to judge whether their own design has sensible responsibilities, relationships and extension points.

## What I reviewed

- **Educative — Grokking the Low-Level Design Interview:** uses a repeatable OOD workflow around requirements, UML, SOLID, patterns and real-world problems, and includes mock interview practice. This validates that learners benefit from a structured process rather than isolated questions. [Source](https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles)
- **LeetCode Discuss — LLD primer / question banks:** community resources provide broad lists of classic problems such as Parking Lot, Elevator, Cache and Splitwise, but are primarily content/discussion repositories rather than a focused submit → evaluate → retry loop. [Primer discussion](https://leetcode.com/discuss/post/1223599/contribute-to-the-low-level-design-primer/) [Question bank](https://leetcode.com/discuss/post/6673561/)
- **LLDCanvas:** combines practice questions with a UML editor, runnable code and interview mode. It demonstrates demand for hands-on design tooling, but also shows how quickly an LLD platform can become a large product. [LLDCanvas](https://www.lldcanvas.in/)
- **LLD Arena:** an open-source practice project combines Java execution, hidden tests, UML and an AI design grader. This is a useful example of a broader implementation-heavy direction. [GitHub](https://github.com/mightbeanshuu/lld-arena)

## Gap / product direction

The MVP deliberately focuses on the smallest useful loop: a learner exposes their design reasoning in a structured submission, receives evidence-based rubric feedback, and can review attempts. It does not try to become an LMS, IDE, diagram editor or full interview simulator.

## Product hypothesis

A good LLD feedback system should not ask “is this design good?” It should evaluate explicit dimensions and cite evidence from the submission. This makes feedback more explainable and leaves room for multiple valid designs.
