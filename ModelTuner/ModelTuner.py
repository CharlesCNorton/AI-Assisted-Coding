import os
from transformers import (
    AutoModelForCausalLM, AutoTokenizer, TextDataset, TrainingArguments, Trainer,
    DataCollatorForLanguageModeling, get_constant_schedule_with_warmup
)
import torch

# Global Default Configurations
CONFIG = {
    "model_path": "path_to_model",
    "train_file_path": "path_to_data",
    "output_dir": "output_directory",
    "num_train_epochs": 1,
    "per_device_train_batch_size": 2,
    "learning_rate": 5e-5,
    "gradient_clipping": 1.0,
    "resume_from_checkpoint": None,
    "use_fp16": False,
    "use_adaptive_lr": False,
    "warmup_steps": 0
}

# Core Logic
def load_model_and_tokenizer(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    return model, tokenizer

def prepare_training_data(train_file_path, tokenizer):
    block_size = min(tokenizer.model_max_length, 512)
    train_data = TextDataset(
        tokenizer=tokenizer,
        file_path=train_file_path,
        block_size=block_size
    )
    return train_data

def configure_training(output_dir, num_train_epochs, per_device_train_batch_size, learning_rate, gradient_clipping, resume_from_checkpoint, use_fp16, use_adaptive_lr, warmup_steps):
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir='./logs',
        learning_rate=learning_rate,
        max_grad_norm=gradient_clipping,
        resume_from_checkpoint=resume_from_checkpoint if resume_from_checkpoint else None,
        fp16=use_fp16
    )
    scheduler = get_constant_schedule_with_warmup(training_args.optimizer, num_warmup_steps=warmup_steps) if use_adaptive_lr else None
    return training_args, scheduler

def perform_training(model, tokenizer, train_data, training_args, scheduler=None):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_data,
        lr_scheduler=scheduler
    )
    trainer.train()
    model.save_pretrained(training_args.output_dir)
    tokenizer.save_pretrained(training_args.output_dir)
    return model, tokenizer

# Configuration Functions
def view_config():
    for key, value in CONFIG.items():
        print(f"{key}: {value}")
    input("\nPress any key to continue...")

def set_config_parameter():
    print("\nChoose parameter to modify:")
    for idx, key in enumerate(CONFIG.keys()):
        print(f"{idx + 1}. {key}")
    choice = int(input("Your choice: ")) - 1
    key = list(CONFIG.keys())[choice]
    if isinstance(CONFIG[key], str):
        CONFIG[key] = input(f"Enter new value for {key}: ")
    elif isinstance(CONFIG[key], int):
        CONFIG[key] = int(input(f"Enter new value for {key}: "))
    elif isinstance(CONFIG[key], float):
        CONFIG[key] = float(input(f"Enter new value for {key}: "))
    elif isinstance(CONFIG[key], bool):
        CONFIG[key] = input(f"Enter new value for {key} (True/False): ").lower() == 'true'
    print(f"{key} updated to {CONFIG[key]}")

def main():
    while True:
        print("\n===== Fine-tuning Menu =====")
        print("1. Fine-tune a model with current configuration")
        print("2. View current configuration")
        print("3. Modify a configuration parameter")
        print("4. Exit")
        choice = input("Your choice: ")

        if choice == '1':
            try:
                model, tokenizer = load_model_and_tokenizer(CONFIG["model_path"])
                train_data = prepare_training_data(CONFIG["train_file_path"], tokenizer)
                training_args, scheduler = configure_training(CONFIG["output_dir"], CONFIG["num_train_epochs"], CONFIG["per_device_train_batch_size"], CONFIG["learning_rate"], CONFIG["gradient_clipping"], CONFIG["resume_from_checkpoint"], CONFIG["use_fp16"], CONFIG["use_adaptive_lr"], CONFIG["warmup_steps"])
                model, tokenizer = perform_training(model, tokenizer, train_data, training_args, scheduler)
                print(f"Fine-tuning completed. Saved to {CONFIG['output_dir']}")
                torch.cuda.empty_cache()

            except FileNotFoundError as e:
                print(e)
            except PermissionError as e:
                print(f"Permission denied: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '2':
            view_config()

        elif choice == '3':
            set_config_parameter()

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
