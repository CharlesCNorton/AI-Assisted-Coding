========================================
GPTQ Quantizer
========================================

Description:
------------------
GPTQ Quantizer provides an easy-to-use interface to perform GPTQ quantization on local Hugging Face Transformer models. It supports various quantization modes and offers a tkinter-based GUI for an interactive user experience.

Getting Started:
------------------
1. Ensure you have the required dependencies installed:
   - transformers
   - tkinter

2. Run `gptq_quantizer.py` to launch the GPTQ Quantizer.

Usage:
------------------
1. Launch GPTQ Quantizer.
2. Follow the on-screen menu to select the desired quantization mode.
3. Use the tkinter-based GUI to select the model directory and specify an output directory for the quantized model.
4. Upon successful quantization, the quantized model will be saved to the specified output directory.

Supported Quantization Modes:
------------------
1. GPTQ Quantization
2. 8-bit Quantization using bitsandbytes
3. 4-bit Quantization using bitsandbytes
4. Advanced 4-bit using NF4 data type
5. Nested Quantization for memory efficiency

Contribute:
------------------
Feel free to fork, open issues, or send pull requests. We appreciate all contributions and feedback!

License:
------------------
This software is released under the original MIT license.

Acknowledgements:
------------------
Thanks to the Hugging Face team for their transformers library which made this tool possible.