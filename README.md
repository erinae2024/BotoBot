# BotoBot

BotoBot is a research chatbot for historical Philippine electoral information, including the 2022 presidential candidates, selected election laws, and general voting and registration procedures.

[Open the research demo](https://botobot.streamlit.app/)

## Run locally

Use Python 3.11 or newer. From the repository root on Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

To run the automated regression tests:

```cmd
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Architecture

The application uses Streamlit, NLTK Naive Bayes intent classification, regular-expression rules, fuzzy entity matching, and a curated JSON dataset. English–Tagalog translation is best-effort; common procedural answers have offline wording. Post-study engineering changes address routing and presentation defects and have not been evaluated using the original study protocol.

## Try it

- Who is Leni Robredo?
- What are her projects?
- What is RA 9006?
- Paano bumoto?
- Paano magparehistro?

## Research and limitations

*LLM Benchmarking of BotoBot: Evaluating an NLTK and Regex-Based Virtual Assistant for Philippine Electoral Information and Voter Empowerment* (O-COCOSDA 2026).

Authors: Maria Art Antonette D. Clariño, Arron B. Baranquil, Erin A. Evangelio, Zachary Andre A. Cruz, and Alaine Carlo R. Magdaluyo (De La Salle University). Corresponding author: Dr. Maria Art Antonette D. Clariño.

The dataset is historical and does not cover current elections. Candidate records are not endorsements; individual claims may require further source verification. Unrecognized questions can receive a clarification or an unsupported-topic response. Automated tests are regression checks, not a new accuracy or hallucination benchmark.

BotoBot is not an official COMELEC service and cannot access voter records. Consult [COMELEC](https://www.comelec.gov.ph/) for current rules. Do not enter personal information; translation may use a third-party service.
