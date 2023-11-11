# Your Personal Terminal Assistant

[![Pylint](https://github.com/webmaster-exit-1/terminal-assistant/actions/workflows/pylint.yml/badge.svg)](https://github.com/webmaster-exit-1/terminal-assistant/actions/workflows/pylint.yml)

> Dev Note: I'm just one guy, making code. If you follow or fork this, don't rely on my updated versions to work. Or even be the same code. So, if I were you and you see something I did and like it, grab it and run with it because I'm not a professional. This is just for fun. And I can and will make breaking changes, stupid ideas, and sometimes, just delete repo's and code I'm done with. Learn 2 Code. Have fun. Happy Hacking

## Features

* Google Search </br>
* Google Voice Recognition </br>
* Google TTS (Speech playback -- Assistants Voice) </br>
* OpenAI API Base

## How to Use

1. Clone the repository to your local machine. </br>
2. Install the required dependencies:
3. https://lmstudio.ai/ -> Click Linux link to join discord -> Give Yourself Linux Beta Role -> Check Pinned Messages in Linux Beta Channel to get the link to the appimage.

```bash
git clone https://github.com/webmaster-exit-1/terminal-assistant
cd terminal-assistant
pip install -r requirements.txt
```

### Customization

1. Open the terminal-assistant.py file in your preferred text editor. </br>
2. Make any modifications you desire.

### Google Search

To enable the custom Google search feature, you need to obtain a Google API key and a custom search engine ID. Follow these steps to set it up: </br>

1. Sign up for a Google API key at the [Google Developers Console](https://console.developers.google.com/). </br>
2. Create a new project and enable the "Custom Search JSON API" for the project. </br>
3. Generate an API key for the project. </br>
4. Get your Google Search Engine ID here: [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/all) </br>
5. Add your `GOOGLE_API_KEY` when prompted by the script. </br>
6. Add your `SEARCH_ENGINE_ID` when prompted by the script..

#### Language Model

By default, it only uses openai's api base. This updated version now uses LM-Studios as the server backend. You can use whatever compatible LLM you want!

#### Usage

Run `LM-Studio Beta Linux appimage` (From the "How to use" #3 section) <br>
- download model, open the server section via left side tab, load model and start server. <br>
- The server will be waiting for terminal_assistant to be started. <br>

Run the `terminal-assistant.py` file using the python command. </br>
`"Enter"` To respond with text </br>
`"Shift+Enter"` To respond by voice </br>
Type `!search` to use Google search,example: `!search cats` </br>
To exit the chatbot, type `quit`.

##### Disclaimer

Terminal Assistant is a personal A.I. assistant and is not intended to replace human interaction or professional advice. Use it at your own risk.
