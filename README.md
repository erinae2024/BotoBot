# BotoBot

BotoBot is a simple Streamlit chatbot for Philippine election and voting information. It uses pattern matching with NLTK to answer questions about the 2022 presidential candidates, voter registration, election rules, and related laws.

## What You Need

- Windows 10/11
- Python 3.10 or newer
- Internet access for the first package install

## Project Files

- [BotoBot_V1.py](BotoBot_V1.py) - main app
- [BotoBotWideLogo.png](BotoBotWideLogo.png) - app banner image
- [UserMascot.png](UserMascot.png) - user avatar
- [BotoBotMascot.png](BotoBotMascot.png) - bot avatar

## Install and Run

Follow these steps in PowerShell from the project folder.

### 1. Open the project folder

```powershell
cd path\to\BotoBot
```

If you already opened the project folder in PowerShell or VS Code, you can skip this step.

### 2. Create a virtual environment

```powershell
py -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this once first:

```powershell
Set-ExecutionPolicy -Scope Process RemoteSigned
```

### 4. Install the dependencies

```powershell
python -m pip install --upgrade pip
pip install streamlit nltk
```

### 5. Start the app

```powershell
streamlit run BotoBot_V1.py
```

Streamlit will open the app in your browser, usually at `http://localhost:8501`.

## How to Test It

Try these prompts in the chat box:

- `Show me the 2022 presidential candidates`
- `Tell me about Leni Robredo`
- `How do I register to vote?`
- `What are my rights?`
- `What can you do?`

If the bot is working, it should either show a candidate list, display a profile card, or answer with a short election-related response.

## Troubleshooting

- If you see `ModuleNotFoundError`, run the install command again inside the activated virtual environment.
- If the app cannot find an image file, make sure the PNG files are still in the same folder as [BotoBot_V1.py](BotoBot_V1.py).
- If PowerShell refuses to activate `.venv`, rerun the activation command after setting the execution policy for the current process.

## Notes

- This chatbot uses fixed matching rules, so it works best when you ask questions in a similar style to the example prompts above.
- The candidate data in the script is focused on the 2022 Philippine presidential election.
