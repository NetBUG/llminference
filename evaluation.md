# Evaluation

## Approach
Evaluation was aimed on assessing query execution time. Each query is processed using the same pipeline, while query set, inference parameters and hardware were varied.
Assessment shows exerpts from a grid search using 
 - short queries / full set
 - absent/present system prompt
 - different hardware (see below)
 - three different models

Target variables were RPM based on a query dataset and optionally performance in tokens/sec (in/out).

**Response assessment** was not considered a part of the task.

An adversarial system like [that](https://github.com/NetBUG/llmplayground/blob/master/llm_assessment/openai_tests.py) can be suggested for that purpose, however, designing that system and the questions for it lies far beyond a sample task with no training: assessment system and prompts are designed to complement the training dataset for the main model. [Model memory](https://github.com/NetBUG/llmplayground/blob/master/llm_assessment/memory_tests.py), [context preservation](https://github.com/NetBUG/llmplayground/blob/master/llm_assessment/misgender_test.py), [user reference](https://github.com/NetBUG/llmplayground/blob/master/llm_assessment/empathy_tests.py) etc can also be handled with similar methods.

**Notice**: As stated in the task, no internal queue was implemented, thus, with real workload actual waiting time might be higher than the pure response time shown in tables.
Suppositions on user counts can me made given the message throughput rate, but those should be left to infrastructure design process; the service requested, designed and implemented does not deal with users, only with individual requests.

## Dataset
Since the task is not about real models, a toy dataset was created with two parts.
 - Short questions (10 in total) contain no more than 12 tokens (7 in average)
 - Long questions (6 in total) contain over 20 tokens

## Code
Please refer to [evaluation/evaluate.py](ai.core.reply/evaluation/evaluate.py)

There are three phases of testing, including 100 iterations of each:
 - short questions (answers are guaranteed to be generated but may be filtered by postprocessing filter)
 - long questions only
 - mixture of short and long questions with probability proportional to subset sizes

## Running
Run `run_evaluation.sh` to perform a single pass of evaluation locally (given current hardware).
You will get an output like that:
```
CID: PIPELINE	Loading model: allenai/Llama-3.1-Tulu-3.1-8B to device: cuda:0
CID: EVAL	Evaluating on cuda:0 -- NVIDIA RTX A6000 - VLLM mode
CID: EVAL	Short questions evaluated: 40.089s, average 149.666 RPM
CID: EVAL	Long questions evaluated: 42.711s, average 140.478 RPM
CID: EVAL	Long questions evaluated: 41.108s, average 145.957 RPM
```

## Evaluation results
As evaluation showed, VLLM affects significantly the performance of inference. Initial hypothesis that it isn't crucial for achieving high performance failed and had to be removed from current text.

As said above, it's hard to assess user load on the service, but if the number of users can be converted into number of requests, a single instance can load the peak loads from a table below.

For vLLM, intrinsic evaluation of input/output token cost was done. It shows that a single input token costs 3 times less than an output one, thus, if a custom model is trained, it's more favorable to favor long user's input and short and concise model outputs.

Running vLLM on backends other than GPU seemed complicated and not worth the time, so some cells in the table are omitted.

A spontaneous test was performed on H100 machine using three different builds with different Python versions.
vLLM does not support 3.13, so only transformers-based generation was used; 3.10 ran into run-time issues so it was also excluded although it should technically work. 

Python 3.11 showed slight although statistically insignificant increase in generation speed, which aligns with author's personal experience.

NVidia drivers version 550.127.08 were used on all GPU-enabled machines.

A table is shown below to reflect outcomes achieved:

| Platform                        | RPM vLLM Avg | RPM trl | in tok/s<br>(VLLM) | out tok/s<br>(VLLM) |
| ------------------------------- | ------------ | ------- | ------------------ | ------------------- |
| RTX A6000 @ 48Gb                | 146          | 44.1    | 102                | 39.1                |
| NVidia RTX3090 GPU @ 24Gb       | 168          | 50.8    | 107                | 45.4                |
| NVidia H100 GPU @ 80Gb @ py3.13 | N/A          | 69.5    | N/A                | N/A                 |
| NVidia H100 GPU @ 80Gb @ py3.12 | 324          | 68.9    | 204                | 87.6                |
| NVidia H100 GPU @ 80Gb @ py3.11 | 325          | 70.4    | 202                | 88.1                |
| Apple M2 CPU @ 16 Gb RAM        | N/A          | 29.3    | N/A                | N/A                 |
| AMD EPYC 9124 CPU               | N/A          | 0.1057  | N/A                | N/A                 |
| i5-10700 CPU                    | N/A          | 0.043   | N/A                | N/A                 |
| Intel Core2Duo T7500 CPU        | N/A          | 0.012   | N/A                | N/A                 |