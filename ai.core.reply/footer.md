## Design considerations
**Model** chosen is [`allenai/Llama-3.1-Tulu-3.1-8B`](https://huggingface.co/allenai/Llama-3.1-Tulu-3.1-8B). It was chosen as a model with instruction training able to perform tasks in user query. 
It has shown decent performance on multiple tests; its larger counterpart with 70B size includes latest training approaches including GRPO to improve behavior on tasks where formal assessment can be performed.

In case one has a Huggingface account with access to `meta-llama/Meta-Llama-3.1-8B-Instruct`, it can be set in `instance/parameters.py` to assess the behavior of the original LLaMA-3.1 model.

Model size was chosen to ensure model to fit into a single common GPU with 24 Gb of RAM; for testing purposes, smaller models of the same architecture can be chosen down to 1.5B models.

**Preprocessing** was implemented using blacklists and is present just to display a pipeline with pre- and postprocessing. For any given business-related task preprocessing must be carefully designed with all requirements in mind, including safety, simplicity and interfacing. Thus, for a dialog-based system prompt building is necessary with conversation sequence preservation; for a contextless AI assistant sensitive topics need to be determined.

**Inference** was optimized for execution with NVidia GPUs and MPS on Apple Mx ARM chips.

**Postprocessing** is implemented using a RoBERTa-based toxicity classifier. Two checks are performed:
 * Single model response
 * Model response following user's query 
This is done to model a situation when two individually safe phrases form an unwanted intention supported by a model (e.g. "My computer is dead! Shall I die as well? - Yes sure")
For any business-oriented task, custom trained model is required to handle potentially risky contexts.

Two-step **build** with plain Docker was chosen, as no limitations have been set in task requirements, and there is no known infrastructure to target for building a more lightweight image.


## Deployment
Run `run_inference.sh` to execute the chain, or build and run manually the image from `ai.core.reply` subfolder.

## Usage
The simplest client could be a cURL request executed from a command line:
```sh
   curl --location 'http://localhost:8000/generate' --header 'Content-Type: application/json' --data '{ "text": "How much is 2 + 3?" }'
```
The API is designed to be integrated as a service into a larger system, current documentation reflects that.
