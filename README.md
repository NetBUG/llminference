# Question answering bot
This is a part of a task designed to exemplify development process of a simple LLM inference.

## Task
Goal: to design and develop a service that is capable of answering user questions using an LLM.
There is no need to train the model as part of this assignment.
The core of the service should be the inference engine for serving the LLM.

Also, preprocessing and postprocessing steps should be implemented to check for prohibited/offensive words in user's request and model responses.
You can use some opensource ML model or rules library for this task (it is assumed that this may be a lengthy operation).
In the end, you should have a 3-step pipeline that solves the given task.
The service should have an HTTP API and be wrapped in Docker to run it on an Nvidia GPU or CPU (you can choose the hardware).

The solution should have:
 - [x] tests
 - [x] the README how to deploy and evaluate the system
 - [ ] a benchmark tool to evaluate service performance with different numbers of users and request lengths (any additional measurements are welcome)
 - [ ] performance analysis under various loads and findings about optimal configurations

## Design considerations
**Model** chosen is [`allenai/Llama-3.1-Tulu-3.1-8B`](https://huggingface.co/allenai/Llama-3.1-Tulu-3.1-8B). It was chosen as a model with instruction training able to perform tasks in user query. 
It has shown decent performance on multiple tests; its larger counterpart with 70B size includes latest training approaches including GRPO to improve behavior on tasks where formal assessment can be performed.

In case one has a Huggingface account with access to `meta-llama/Meta-Llama-3.1-8B-Instruct`, it can be set in `instance/parameters.py` to assess the behavior of the original LLaMA-3.1 model.

Model size was chosen to ensure model to fit into a single common GPU with 24 Gb of RAM; for testing purposes, smaller models of the same architecture can be chosen down to 1.5B models.

**Preprocessing** was implemented using blacklists and is present just to display a pipeline with pre- and postprocessing. For any given business-related task preprocessing must be carefully designed with all requirements in mind, including safety, simplicity and interfacing. Thus, for a dialog-based system prompt building is necessary with conversation sequence preservation; for a contextless AI assistant sensitive topics need to be determined.

**Inference** was optimized for execution with NVidia GPUs and MPS on Apple Mx ARM chips.
To speed up inference, vllm was used instead of vanilla transformers.
Interface of `ModelGenerator` has been made exactly the same as for transformers inference. Parameters set does not fully intersect, however, certain effort has been made to maximize matches between response distribution for initial (small) question set in evaluation.

**Postprocessing** is implemented using a RoBERTa-based toxicity classifier. Two checks are performed:
 - Single model response
 - Model response following user's query 
This is done to model a situation when two individually safe phrases form an unwanted intention supported by a model (e.g. "My computer is dead! Shall I die as well? - Yes sure")
For any business-oriented task, custom trained model is required to handle potentially risky contexts.

Two-step **build** with plain Docker was chosen, as no limitations have been set in task requirements, and there is no known infrastructure to target for building a more lightweight image.


## Deployment
Run `run_inference.sh` to execute the chain, or build and run manually the image from `ai.core.reply` subfolder.
It is supposed that we have a __containerd__ installed with `docker-cli` interface. For other setups (including __nerdctl__, usage of buildx) please adjust shell scripts accordingly.

## Usage
The simplest client could be a cURL request executed from a command line:
```sh
   curl --location 'http://localhost:8000/generate' --header 'Content-Type: application/json' --data '{ "text": "How much is 2 + 3?" }'
```
The API is designed to be integrated as a service into a larger system, please check [API documentation](/doc) to do so.

### API Documentation
The API was documented according to [APIDoc](https://apidocjs.com/) standards.

#### Prerequisites
Install `apidoc`:
```sh
    npm install -g apidoc
```

#### Generate (updated) documentation
```sh
    cd ai.core.reply && apidoc -i instance
```

## Running tests
Run `run_tests.sh`

## Evaluation
Evaluation was aimed on assessing query execution time. Each query is processed using the same pipeline, while query set, inference parameters and hardware were varied.
Assessment shows exerpts from a grid search using 
 - short queries / full set
 - absent/present system prompt
 - different hardware (see below)
 - three different models

Target variables: RPM, tokens/sec.

<...>

vLLM does not seem to have significant influence on small queries, speeding up from circa 0.6 to 0.42s per query on an A6000 GPU. However, that's around 30% increase, that, despite the advantage slightly reducing with large context size (1000 tokens and more benefit ~22-25% from vLLM) will affect user experience even more

**Response assessment** was not considered a part of the task.

An adversarial system like [that](https://github.com/NetBUG/llmplayground/blob/master/llm_assessment/openai_tests.py) can be suggested for that purpose, however, designing that system and the questions for it lies far beyond a sample task with no training: assessment system and prompts are designed to complement the training dataset for the main model. [Model memory](https://github.com/NetBUG/llmplayground/blob/master/llm_assessment/memory_tests.py), [context preservation](https://github.com/NetBUG/llmplayground/blob/master/llm_assessment/misgender_test.py), [user reference](https://github.com/NetBUG/llmplayground/blob/master/llm_assessment/empathy_tests.py) etc can also be handled with similar methods.

**Notice**: As stated in the task, no internal queue was implemented, thus, with real workload actual waiting time might be higher than the pure response time shown in tables.
Suppositions on user counts can me made given the message throughput rate, but those should be left to infrastructure design process; the service requested, designed and implemented does not deal with users, only with individual requests.

## Evaluation results
 - NVidia RTX3090 GPU @ 24Gb
 - NVidia A6000 GPU @ 48Gb
 - NVidia H100 GPU @ 80Gb
 - Apple M2 CPU @ 16 Gb RAM
 - Intel Core2Duo CPU @ 16 Gb RAM

## Credits
This project would never appear without M.P., D.T., I.V. and the whole inference team. I am just too lazy without external influence.
