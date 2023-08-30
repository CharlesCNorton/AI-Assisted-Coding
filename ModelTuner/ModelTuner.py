import os
from transformers import (
    AutoModelForCausalLM, AutoTokenizer, TextDataset, TrainingArguments, Trainer,
    DataCollatorForLanguageModeling, get_constant_schedule_with_warmup
)
import torch
from collections import namedtuple
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Configuration namedtuple for better organization
Config = namedtuple('Config', [
    "model_path",
    "train_file_path",
    "output_dir",
    "num_train_epochs",
    "per_device_train_batch_size",
    "learning_rate",
    "gradient_clipping",
    "resume_from_checkpoint",
    "use_fp16",
    "use_adaptive_lr",
    "warmup_steps"
])

# Default Configurations
DEFAULT_CONFIG = Config(
    model_path="gpt2-medium",
    train_file_path="path_to_data",
    output_dir="output_directory",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    learning_rate=5e-5,
    gradient_clipping=1.0,
    resume_from_checkpoint=None,
    use_fp16=False,
    use_adaptive_lr=False,
    warmup_steps=0
)

# Tooltips for each configuration parameter
TOOLTIPS = {
    "model_path": "Path to the pre-trained model or model identifier from huggingface.co/models.",
    "train_file_path": "Path to the training data.",
    "output_dir": "Path to save the fine-tuned model.",
    "num_train_epochs": "Number of training epochs. Suggested range: 1-10, depending on data size.",
    "per_device_train_batch_size": "Batch size per device during training. Suggested range: 2-32, based on GPU memory.",
    "learning_rate": "Training learning rate. Suggested range: 1e-6 to 1e-3. Smaller datasets might require smaller LR.",
    "gradient_clipping": "Maximum norm of the gradients. Suggested range: 0.1-5.0. Prevents exploding gradients.",
    "resume_from_checkpoint": "Path to resume training from a checkpoint.",
    "use_fp16": "Use 16-bit (mixed) precision training instead of 32-bit. Can speed up training on supported GPUs.",
    "use_adaptive_lr": "Use adaptive learning rate with warmup steps. Adapts learning rate during training.",
    "warmup_steps": "Number of warmup steps for adaptive learning rate. Suggested range: 0-5000. Helps in stabilizing training in the beginning."
}

from transformers import DataCollatorForLanguageModeling

def load_model_and_tokenizer(model_path):
    """Load a pre-trained model and tokenizer from Hugging Face's model hub."""
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer

def prepare_training_data(train_file_path, tokenizer):
    """Prepare the training data by tokenizing the text."""
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_file_path,
        block_size=128
    )
    return train_dataset

def configure_training(config):
    """Set up the training configuration."""
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        overwrite_output_dir=True,
        num_train_epochs=config.num_train_epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        learning_rate=config.learning_rate,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        save_steps=10,
        save_total_limit=2,
        fp16=config.use_fp16,
        gradient_accumulation_steps=1,
        gradient_clipping=config.gradient_clipping,
        evaluation_strategy="steps",
        eval_steps=10,
        warmup_steps=config.warmup_steps,
        logging_first_step=True
    )

    scheduler = get_constant_schedule_with_warmup if config.use_adaptive_lr else None
    return training_args, scheduler

def perform_training(model, tokenizer, train_data, training_args, scheduler):
    """Perform the actual fine-tuning."""
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_data
    )

    trainer.train()
    trainer.save_model()

    return model, tokenizer

def view_config(config):
    """Display the current configuration."""
    for field in config._fields:
        print(f"{field}: {getattr(config, field)}")


def set_config_parameter(config):
    """Modify a configuration parameter."""
    fields = config._fields
    print(Fore.BLUE + "\nChoose parameter to modify:")
    for idx, field in enumerate(fields):
        print(Fore.GREEN + f"{idx + 1}. {field} (Current: {getattr(config, field)})")
        print(Fore.WHITE + f"   - {TOOLTIPS[field]}")

    choice = int(input(Fore.YELLOW + "Your choice: ")) - 1
    key = fields[choice]
    current_value = getattr(config, key)

    # For boolean values, provide a toggle option
    if isinstance(current_value, bool):
        new_value = input(f"Do you want to enable {key}? (yes/no, Current: {current_value}): ").lower() == 'yes'
    else:
        new_value = input(f"Enter new value for {key} (Press Enter to keep current value: {current_value}): ")
        if not new_value:
            new_value = current_value
        else:
            # Convert the input to the appropriate type
            if isinstance(current_value, int):
                new_value = int(new_value)
            elif isinstance(current_value, float):
                new_value = float(new_value)

    updated_config = config._replace(**{key: new_value})
    print(Fore.CYAN + f"{key} updated to {getattr(updated_config, key)}")
    return updated_config

def main():
    config = DEFAULT_CONFIG

    while True:
        print(Fore.BLUE + "\n===== Fine-tuning Menu =====")
        print(Fore.GREEN + "1. Fine-tune a model with current configuration")
        print(Fore.GREEN + "2. View current configuration")
        print(Fore.GREEN + "3. Modify a configuration parameter")
        print(Fore.GREEN + "4. Exit")
        choice = input(Fore.YELLOW + "Your choice: ")

        if choice == '1':
            try:
                model, tokenizer = load_model_and_tokenizer(config.model_path)
                train_data = prepare_training_data(config.train_file_path, tokenizer)
                training_args, scheduler = configure_training(config)
                model, tokenizer = perform_training(model, tokenizer, train_data, training_args, scheduler)
                print(Fore.CYAN + f"Fine-tuning completed. Saved to {config.output_dir}")

                # Clear GPU memory if available
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

            except FileNotFoundError as e:
                print(Fore.RED + str(e))
            except PermissionError as e:
                print(Fore.RED + f"Permission denied: {e}")
            except Exception as e:
                print(Fore.RED + f"An error occurred: {e}")

        elif choice == '2':
            view_config(config)

        elif choice == '3':
            config = set_config_parameter(config)

        elif choice == '4':
            break

        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
