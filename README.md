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

## Deployment

## Running tests

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
