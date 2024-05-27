# Alex Assistant

![Alex Assistant Logo](logo.png)

A simple tutorial showing how to capture the screen, recognize speech, add context, and query Anthropic API

*Disclaimer: This assistant is not meant to be used for real proposal development, but is simply a fun demo that combines many inputs (voice, image, text) and shows how to weave these into an application with Anthropic Claude.*

## Features

- Captures the current screen as an input to the LLM.
- Uses speech recognition to convert spoken commands to text.
- Shows a simple strategy to inject context from a text file into the prompt
- Queries the Anthropic API with both text and image inputs.
- Provides responses in Markdown format.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/blaiszik/alex-assistant
   cd alex-assistant
   ```

2. Create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
Install the package:
```

```bash
pip install .
```

## Setting the Environment Variable

To use the Anthropic API, you need to set the ANTHROPIC_API_KEY environment variable. Here’s how to do it:

On Mac
1. Open your terminal.

2. Add the following line to your shell profile file (e.g., ~/.bash_profile, ~/.zshrc, or ~/.profile):

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

3. Apply the changes. e.g., `source ~/.bash_profile` `source ~/.zshrc` 



## Usage

1. Ensure the ANTHROPIC_API_KEY environment variable is set.

2. Run the main script:

```bash
python anthropic_screen_capturer
```

Speak your command when prompted. The tool will capture the screen and query the Anthropic API with the captured image and spoken command.

The default model is set to Claude 3 Haiku (the cheapest available model). For better responses, you can try the other models.

Other models "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
Newer models may be available, see: https://docs.anthropic.com/en/docs/models-overview

