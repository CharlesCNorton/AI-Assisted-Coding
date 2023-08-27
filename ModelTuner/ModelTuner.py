import os
from transformers import (AutoModelForCausalLM, AutoTokenizer, TextDataset,
                          TrainingArguments, Trainer, DataCollatorForLanguageModeling)
import torch

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

def configure_training(output_dir, num_train_epochs, per_device_train_batch_size, learning_rate, gradient_clipping, resume_from_checkpoint, use_fp16):
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
    return training_args

def perform_training(model, tokenizer, train_data, training_args):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_data,
    )
    trainer.train()
    model.save_pretrained(training_args.output_dir)
    tokenizer.save_pretrained(training_args.output_dir)
    return model, tokenizer

# I/O functions
def get_user_input():
    model_path = input("Enter the directory path of the pre-trained model: ")
    train_file_path = input("Enter the path to the training data: ")
    output_dir = input("Enter the directory to save the fine-tuned model: ")
    num_train_epochs = int(input("Enter the number of training epochs: "))
    per_device_train_batch_size = int(input("Enter the per-device train batch size: "))
    learning_rate = float(input("Enter the learning rate (e.g., 5e-5): "))
    gradient_clipping = float(input("Enter the gradient clipping value (set to 0 to disable): "))
    resume = input("Do you want to continue training from the last checkpoint? (y/n): ")
    resume_from_checkpoint = output_dir if resume.lower() == 'y' else None
    use_fp16 = input("Do you want to use 16-bit mixed precision training? (y/n): ").lower() == 'y'
    return model_path, train_file_path, output_dir, num_train_epochs, per_device_train_batch_size, learning_rate, gradient_clipping, resume_from_checkpoint, use_fp16

def main():
    while True:
        print("\nMenu:")
        print("1. Fine-tune a model")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            model_path, train_file_path, output_dir, num_train_epochs, per_device_train_batch_size, learning_rate, gradient_clipping, resume_from_checkpoint, use_fp16 = get_user_input()

            try:
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Model directory not found: {model_path}")
                if not os.path.exists(train_file_path):
                    raise FileNotFoundError(f"Training file not found: {train_file_path}")

                model, tokenizer = load_model_and_tokenizer(model_path)
                train_data = prepare_training_data(train_file_path, tokenizer)
                training_args = configure_training(output_dir, num_train_epochs, per_device_train_batch_size, learning_rate, gradient_clipping, resume_from_checkpoint, use_fp16)
                model, tokenizer = perform_training(model, tokenizer, train_data, training_args)

                print(f"Fine-tuning completed. The fine-tuned model was saved to {output_dir}")
                torch.cuda.empty_cache()

            except FileNotFoundError as e:
                print(e)
            except PermissionError as e:
                print(f"Permission denied: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '2':
            break

        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
