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

The solution would have:
* tests
* the README how to deploy and evaluate the system
* a benchmark tool to evaluate service performance with different numbers of users and request lengths (any additional measurements are welcome)
* performance analysis under various loads and findings about optimal configurations
You are free to design your own solution.

## Design considerations
**Model** chosen is [`allenai/Llama-3.1-Tulu-3.1-8B`](https://huggingface.co/allenai/Llama-3.1-Tulu-3.1-8B). It was chosen as a model with instruction training able to perform tasks in user query. 
It has shown decent performance on multiple tests; its larger counterpart with 70B size includes latest training approaches including GRPO to improve behavior on tasks where formal assessment can be performed.

In case one has a Huggingface account with access to `meta-llama/Meta-Llama-3.1-8B-Instruct`, it can be set in `instance/parameters.py` to assess the behavior of the original LLaMA-3.1 model.

Model size was chosen to ensure model to fit into a single common GPU with 24 Gb of RAM; for testing purposes, smaller models of the same architecture can be chosen down to 1.5B models.

**Preprocessing** was implemented using blacklists and is present just to display a pipeline with pre- and postprocessing. For any given business-related task preprocessing must be carefully designed with all requirements in mind, including safety, simplicity and interfacing. Thus, for a dialog-based system prompt building is necessary with conversation sequence preservation; for a contextless AI assistant sensitive topics need to be determined.
<...>
**Inference** was optimized for execution with NVidia GPUs and MPS on Apple Mx ARM chips.
<...>
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


## Evaluation results
Notice: the estimations on model load were given using <...> presupposition.
As stated in the task, no internal queue was implemented, thus, with real load actual waiting time might be higher than the pure response time.
Suppositions on user counts can me made given the message throughput rate, but those should be left to project team.
 - NVidia RTX3090 GPU @ 24Gb
 - NVidia H100 GPU @ 80Gb
 - Apple M2 CPU @ 16 Gb RAM
 - Intel Core2Duo CPU @ 16 Gb RAM

## Credits
This project would never appear without M.P., D.T., I.V. and the whole inference team. I am just too lazy without external influence.
