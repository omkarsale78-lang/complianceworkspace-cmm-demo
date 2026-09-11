# ComplianceWorkspace CMM Demo

A working Streamlit prototype for demonstrating a PMS compliance-readiness workflow to a Chartered Accountant or compliance professional.

## Features

- Readiness dashboard and priority blockers
- Editable sample CMM checklist
- Owner assignment and session-only evidence uploads
- Document vault
- Reviewer and Principal Officer sign-off controls
- Internal readiness and approval-trail CSV exports
- CA feedback form

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Push this folder to a separate GitHub repository, then deploy `app.py` with Streamlit Community Cloud or Render.

## Safety and scope

This is a prototype with fictional data and illustrative controls and dates. Do not upload confidential or personal information. A qualified compliance professional must validate requirements before any production or regulatory use. It does not submit to SEBI or guarantee acceptance.
