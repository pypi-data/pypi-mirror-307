from re import match as re_match
from sys import argv as sys_argv

from warnings import warn
# from KAFY.pipeline import TrajectoryPipeline
from KAFY.mainPipeline import TrajectoryPipeline
from KAFY.modelsLoader import (
    load_model_from_huggingface,
    load_model_from_file,
)
import logging
from os import path as os_path
# Configure the logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def update_project_location(new_location, file_name="assets/projectLocation.txt"):
    """Updates the project location file and sets the environment variable."""
    # Update the project location in the file
    file_path = os_path.join(os_path.dirname(os_path.abspath(__file__)), file_name)
    with open(file_path, "w") as file:
        file.write(new_location)


def get_project_location(
    file_name="assets/projectLocation.txt", default_path="KafyProjectDirectory"
):
    """Reads the project location from a file. Falls back to default if file is not found or empty."""
    try:

        file_path = os_path.join(os_path.dirname(os_path.abspath(__file__)), file_name)
        with open(file_path, "r") as file:
            project_location = file.read().strip()
            if not project_location:
                return default_path
            return project_location
    except FileNotFoundError:
        raise FileNotFoundError(f"Couldn't find project location file '{file_path}'.")


# Project location default path set through environment variable (case-insensitive)
kafy_project_location = get_project_location()
"""
Global variable to define the project's root directory.

Users can update this variable to specify a custom location for their project data, models, and results.

Attributes:
    kafy_project_location (str): The path to the main project directory. Defaults to '/KafyProject/'.

Example:
    To change the project location:
    
    >>> export KAFY_PROJECT_LOCATION=/new/project/location
"""


def start_new_project(location):
    """
    Starts a new project by creating the required directories at the given location.

    Args:
        location (str, optional): The path where the new project should be created. Defaults to kafy_project_location.

    Returns:
        None
    """
    global kafy_project_location
    if location is None:
        location = kafy_project_location
    # User changed the location so we need to also update the environment variable.
    elif location != kafy_project_location:
        kafy_project_location = location
        update_project_location(kafy_project_location)
    # Ensure the provided location exists or create it

    TrajectoryPipeline(
        mode="startNewProject",
        project_path=kafy_project_location,
    )


def add_pretraining_data(data_location: str = "data_location.csv"):
    """
    Adds dataset to Trajectory store, to be used later to pretrain all models.

        Args:
            data_location (str): file path of data.csv file to be tokenized and added to be used for pretraining.

        Returns:
            None
    """
    global kafy_project_location
    pipeline = TrajectoryPipeline(
        mode="addPretrainingData",
        use_tokenization=True,
        project_path=kafy_project_location,
    )
    trajectories_list = pipeline.get_trajectories_from_csv(column_name="trajectory",file_path=data_location)
    # pipeline.set_trajectories(trajectories_list)
    # TODO Youssef: This can be given from the user
    pipeline.set_tokenization_resolution(10)
    pipeline.add_pretraining_data(trajectories_list)


def add_model(model_family, source, config_path, save_as_name):
    # @YOUSSEF DO: I need to use the optut_name to save the transformer_family using this name in the pyramid
    global kafy_project_location
    # If the model is available at HuggingFace then load it
    if source.lower() == "hf":
        model = load_model_from_huggingface(
            model_name=model_family, config_path=config_path
        )
    # or load it from a user-defined class
    else:
        ##This is not implemented for now
        model = load_model_from_file(source, config_path)
    ##Now we need to check if this model exists in the modelsRepo
    pipeline = TrajectoryPipeline(
        mode="addPretrainModel",
        project_path=kafy_project_location,
    )
    training_args_path = os_path.join(
        os_path.dirname(os_path.abspath(__file__)), "assets/training_args.json"
    )
    model.config.training_args_path = training_args_path
    if not getattr(model.config, "training_args_path", None):
        # Raise a warning if training_args_path is not provided
        warn(
            "No 'training_args_path' found in the configuration. "
            "Default TrainingArguments will be used from assets/training_args. "
            "If you want to use your own TrainingArguments, please provide a path to the training_args.json file.",
            UserWarning,
        )
        # You can set up the default TrainingArguments or do additional logic here
    else:
        # Proceed with using the training_args_path from the config
        training_args_path = model.config.training_args_path

    model.config.given_name = save_as_name
    

    """
    # initialize the data collator, randomly masking 20% (default is 15%) of the tokens for the Masked Language
    # Modeling (MLM) task
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=True, mlm_probability=0.2
    )
    training_args = TrainingArguments(
    output_dir=model_path,          # output directory to where save model checkpoint
    evaluation_strategy="steps",    # evaluate each `logging_steps` steps
    overwrite_output_dir=True,
    num_train_epochs=1,            # number of training epochs, feel free to tweak
    per_device_train_batch_size=10, # the training batch size, put it as high as your GPU memory fits
    gradient_accumulation_steps=8,  # accumulating the gradients before updating the weights
    per_device_eval_batch_size=64,  # evaluation batch size
    logging_steps=1000,             # evaluate, log and save model checkpoints every 1000 step
    save_steps=1000,
    # load_best_model_at_end=True,  # whether to load the best model (in terms of loss) at the end of training
    # save_total_limit=3,           # whether you don't have much space so you let only 3 model weights saved in the disk
    )
    # initialize the trainer and pass everything to it
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )
    trainer.train()
    """
    # TODO: For now the model architecure will be added to TransformersPlugin/pretraining
    transformersPluginDirectory = os_path.join(
        kafy_project_location, "transformersPlugin"
    )
    if not os_path.exists(transformersPluginDirectory):
        os.makedirs(transformersPluginDirectory)
    # From HF utilities
    # But do I need to call the trainer before?
    # save the architecture itself as a random weight initialized model
    model.save_pretrained(
        os_path.join(transformersPluginDirectory, "pretraining", save_as_name)
    )
    logging.info("Model architecture inially saved to transformersPlugin")
    pipeline.pretrain_model_on_all_datasets(model)


def finetune_model(task, pretrained_model_path, config_path, output_name):
    # Initialize and run your fine-tuning pipeline here
    pipeline = TrajectoryPipeline(
        mode="finetuning",
        operation_type=task,
        # other relevant configurations
    )
    # Fine-tuning logic
    logging.info(f"Fine-tuned model saved as {output_name}")


def summarize_data(data_path, model_path):
    # Initialize and run your summarization pipeline here
    pipeline = TrajectoryPipeline(
        mode="operation",
        operation_type="summarization",
        # other relevant configurations
    )
    # Summarization logic
    logging.info("Summarization complete")


def parse_command(command=None):
    if command is None:
        command = " ".join(
            sys_argv[1:]
        )  # Join command-line arguments into a single string
    start_new_project_match = re_match(
        r"(?i)start\s+new\s+project\s*(.*)",  # (?i) makes "start", "new", "project" case-insensitive
        command,
    )
    add_pretraining_data_command_match = re_match(
        r"(?i)add\s+pretraining\s+data\s+from\s+(\S+)\s*",  # (?i) makes "add", "pretraining", "data", and "from" case-insensitive
        command,
    )
    # Captures HF or a model file and a config file
    add_model_match = re_match(
        r"(?i)add\s+model\s+(\w+)\s+from\s+(hf|(\S+))\s+using\s+(\S+)\s+as\s+(\S+)",
        command,
    )
    # finetune_match = re_match(
    #     r"FINETUNE\s+(\w+)\s+FOR\s+(\w+)\s+USING\s+(\S+)\s+WITH\s+(\S+)\s+AS\s+(\S+)",
    #     command,
    #     re_IGNORECASE,
    # )
    # summarize_match = re_match(
    #     r"SUMMARIZE\s+FROM\s+(\S+)\s+USING\s+(\S+)", command, re_IGNORECASE
    # )
    if start_new_project_match:
        location = start_new_project_match.group(1).strip()
        if location == "":
            location = None  # If no location provided, set to None so it defaults to kafy_project_location
        start_new_project(location)
    elif add_pretraining_data_command_match:
        data_location = add_pretraining_data_command_match.group(1)
        add_pretraining_data(data_location)
    elif add_model_match:
        model_name = add_model_match.group(1)  # xBERT or model name
        source = add_model_match.group(2)  # "hf" or path to model.py
        config_path = add_model_match.group(4)  # Path to config.json
        save_as_name = add_model_match.group(5)  # Path to config.json
        add_model(model_name, source, config_path, save_as_name)
        logging.info(
            "New Model was pretrained successfully on all available datasets and saved to the modelsRepo."
        )
    # elif finetune_match:
    #     model, task, pretrained_model, config, output_name = finetune_match.groups()
    #     finetune_model(task, pretrained_model, config, output_name)
    # elif summarize_match:
    #     data, model = summarize_match.groups()
    #     summarize_data(data, model)
    else:
        raise ValueError("Command Not Supported (Erroneous Command)")
