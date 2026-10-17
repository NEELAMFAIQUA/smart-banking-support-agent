# Banking Support Assistant

An original local FAQ retrieval demo for general banking education.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

This prototype is educational only. It does not provide personalized financial
advice, access accounts, or make transactions. Never enter account numbers,
passwords, PINs, or verification codes. Verify important information using
official institutions and regulators.

Run checks with `python -m unittest discover -s tests -v`.
