import os
from transformers import AutoModelForCausalLM, AutoTokenizer, TextDataset, TrainingArguments, Trainer
import torch

def fine_tune_model(model_path, train_file_path, output_dir, num_train_epochs, per_device_train_batch_size, block_size=128, save_steps=10_000):
    try:
        # Check if the model directory exists
        if not os.path.exists(model_path):
            print(f"Model directory not found: {model_path}")
            return

        # Check if the training file exists
        if not os.path.exists(train_file_path):
            print(f"Training file not found: {train_file_path}")
            return

        # Load the pre-trained model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)

        # Prepare the new data
        train_data = TextDataset(
            tokenizer=tokenizer,
            file_path=train_file_path,
            block_size=block_size
        )

        # Configure the training
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            save_steps=save_steps,
            save_total_limit=2,
        )

        # Fine-tune the model
        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=lambda data: {'input_ids': torch.stack([f[0] for f in data])},
            train_dataset=train_data,
        )

        trainer.train()

        # Save the fine-tuned model
        model.save_pretrained(output_dir)

        print(f"Fine-tuning completed. The fine-tuned model was saved to {output_dir}")

    except Exception as e:
        print(f"An error occurred during fine-tuning: {e}")

def main():
    while True:
        print("\nMenu:")
        print("1. Fine-tune a model")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            model_path = input("Enter the directory path of the pre-trained model: ")
            train_file_path = input("Enter the path to the training data: ")
            output_dir = input("Enter the directory to save the fine-tuned model: ")
            num_train_epochs = int(input("Enter the number of training epochs: "))
            per_device_train_batch_size = int(input("Enter the per-device train batch size: "))

            fine_tune_model(model_path, train_file_path, output_dir, num_train_epochs, per_device_train_batch_size)

        elif choice == '2':
            break

        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
