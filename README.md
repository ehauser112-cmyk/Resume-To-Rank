# Resume-To-Rank

Resume to Rank is a Flask app for uploading resumes, parsing candidate text, ranking candidates by selected skills, sorting the results, and exporting a ranked CSV.

## Local Setup

1. Create and activate a Python environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python serve_frontend.py
```

4. Open:

```text
http://127.0.0.1:5055
```

## Tests

Run the main test suite:

```powershell
python -m unittest tests.test_app -v
```

Run the manual-plan-mapped automated checks:

```powershell
python -m unittest tests.test_manual_plan_cases -v
```

## Hosting

The app is prepared for Python hosting services that support WSGI apps and Procfiles.

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn wsgi:app`
- Python runtime: `python-3.13.13`

GitHub Pages is configured for the static project page in `pages/`. GitHub Pages cannot run the Flask API because it does not support Python server-side execution.

Set these environment variables if the hosting platform provides writable storage paths:

- `UPLOAD_FOLDER`
- `OUTPUT_FOLDER`
- `TEMP_FOLDER`

Uploaded resumes and exported CSV files are runtime data and are intentionally excluded from version control.
