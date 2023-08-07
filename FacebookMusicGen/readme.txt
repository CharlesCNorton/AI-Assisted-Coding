# Facebook Music Generator

This Python script uses the Transformers library to generate music using pre-trained models provided by Facebook. The generated music is stored in WAV format.

## Requirements

- Transformers library
- SciPy
- Python 3.x
- Anything else it says you're missing

## Usage

1. Go into the code and change the output paths to correspond with your desired one.
2. Run the script: `python FacebookMusicGenerator.py`
3. Follow the prompts in the script to generate music. **You can select from three different models (1-3), or quit the program by entering 'q'.**

(max_new_tokens is set to 256 (5 seconds) by default, but it can be changed to increase the audio length of the output.)

## Error Handling

The script includes error handling capabilities. In case of an error during the music generation process, the error message will be recorded for further debugging.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

The GNU General Public License v3.0