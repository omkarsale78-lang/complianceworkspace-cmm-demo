import io
from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ComplianceWorkspace — CMM Demo", page_icon="✅", layout="wide")

TEAM = ["R. Sharma — Principal Officer", "Priya Mehta — Compliance Officer", "Arjun Nair — Company Secretary", "Meera Das — Legal", "Vikram Joshi — Operations"]
SEED = [
    {"id": 1, "category": "Category 1", "requirement": "Client agreement — required clauses verified", "status": "Compliant", "owner": TEAM[1], "evidence": 2, "due": "", "note": "Sample agreements reviewed against the illustrative checklist."},
    {"id": 2, "category": "Category 1", "requirement": "AML/KYC policy and due-diligence evidence", "status": "Partially compliant", "owner": TEAM[2], "evidence": 1, "due": "2025-08-25", "note": "Policy uploaded; sample approval sign-off remains outstanding."},
    {"id": 3, "category": "Category 1", "requirement": "Board-approved fee disclosure", "status": "Compliant", "owner": TEAM[3], "evidence": 3, "due": "", "note": "Illustrative disclosure approved and attached."},
    {"id": 4, "category": "Category 2", "requirement": "Investor grievance policy and quarterly log", "status": "Not started", "owner": "Unassigned", "evidence": 0, "due": "2025-08-30", "note": "Sample policy and quarterly log are missing."},
    {"id": 5, "category": "Category 1", "requirement": "Business Continuity Plan", "status": "Compliant", "owner": TEAM[4], "evidence": 2, "due": "", "note": "Sample BCP uploaded and marked reviewed."},
    {"id": 6, "category": "Category 2", "requirement": "Separate client bank account maintained", "status": "Compliant", "owner": TEAM[1], "evidence": 1, "due": "", "note": "Fictional bank evidence attached."},
    {"id": 7, "category": "Category 1", "requirement": "Fit and proper declaration — PO and directors", "status": "Partially compliant", "owner": TEAM[0], "evidence": 2, "due": "2025-08-28", "note": "One fictional director declaration remains outstanding."},
]
SAMPLE_DOCS = [
    ("AML_Policy_v3.pdf", "v3", "Approved", "1.2 MB"),
    ("Client_Agreement_Template.docx", "v5", "Approved", "840 KB"),
    ("Investor_Grievance_Log.xlsx", "v2", "Pending review", "320 KB"),
    ("BCP_2026.pdf", "v1", "Pending approval", "2.1 MB"),
    ("Disclosure_Cert_FY26.pdf", "v1", "Approved", "560 KB"),
]

if "items" not in st.session_state:
    st.session_state["items"] = [x.copy() for x in SEED]
if "uploads" not in st.session_state:
    st.session_state.uploads = []
if "reviewer_done" not in st.session_state:
    st.session_state.reviewer_done = False
if "po_done" not in st.session_state:
    st.session_state.po_done = False

st.markdown("""
<style>
:root{--blue:#2563eb;--ink:#111827;--line:#e5e7eb}
[data-testid="stAppViewContainer"]{background:#f8f9fb}
[data-testid="stHeader"]{background:transparent}
.block-container{padding-top:1.25rem;max-width:1220px}
.cw-head{background:#0f1623;color:white;padding:18px 22px;border-radius:10px;margin-bottom:16px;display:flex;justify-content:space-between;align-items:center}
.cw-brand{font-size:18px;font-weight:700}.cw-brand span{background:#2563eb;padding:6px 8px;border-radius:6px;margin-right:9px;font-size:12px}
.cw-sub{color:#94a3b8;font-size:12px;margin-top:5px}.demo{border:1px solid #3b82f6;color:#bfdbfe;padding:5px 9px;border-radius:6px;font-size:11px;font-weight:700}
.card{background:white;border:1px solid #e5e7eb;border-radius:9px;padding:15px;margin-bottom:10px}.card h4{margin:0 0 4px;font-size:14px}.muted{color:#6b7280;font-size:12px}.tag{display:inline-block;padding:3px 7px;border-radius:99px;font-size:10px;font-weight:700}.green{background:#f0fdf4;color:#168447}.amber{background:#fffbeb;color:#b45309}.red{background:#fef2f2;color:#dc2626}.blue{background:#eff6ff;color:#1d4ed8}
.notice{background:#fffbeb;border:1px solid #fde68a;color:#92400e;padding:12px 14px;border-radius:8px;font-size:12px}.legal{font-size:11px;color:#6b7280;border-top:1px solid #e5e7eb;padding-top:14px;margin-top:25px}
div[data-testid="stMetric"]{background:white;border:1px solid #e5e7eb;padding:13px;border-radius:9px}div[data-testid="stMetricValue"]{font-size:28px}
.stButton button,.stDownloadButton button{border-radius:6px;font-weight:700;min-height:40px}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="cw-head"><div><div class="cw-brand"><span>CW</span>ComplianceWorkspace</div><div class="cw-sub">PMS • CMM readiness workflow</div></div><div class="demo">WORKING PROTOTYPE • FICTIONAL DATA</div></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Arjun Capital Advisors")
    st.caption("INP000007XXX • fictional firm")
    page = st.radio("Navigate", ["Readiness dashboard", "CMM checklist", "Document vault", "Review & approval", "CA feedback"], label_visibility="collapsed")
    st.divider()
    st.caption("Quarter")
    st.write("**Q2 FY 2025–26**")
    st.caption("Illustrative deadline")
    st.write("**31 Oct 2025**")
    if st.button("Reset demo", use_container_width=True):
        st.session_state["items"] = [x.copy() for x in SEED]
        st.session_state.uploads = []
        st.session_state.reviewer_done = False
        st.session_state.po_done = False
        st.rerun()

items = st.session_state["items"]
compliant = sum(x["status"] == "Compliant" for x in items)
partial = sum(x["status"] == "Partially compliant" for x in items)
not_started = sum(x["status"] == "Not started" for x in items)
missing_evidence = sum(x["evidence"] == 0 for x in items)
readiness = round((compliant / len(items)) * 100)
blockers = sum(x["status"] != "Compliant" or x["evidence"] == 0 for x in items)

if page == "Readiness dashboard":
    st.title("Ready before the deadline")
    st.caption("A single view of responses, evidence, ownership and approvals.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Compliant", compliant, f"of {len(items)} sample controls")
    c2.metric("Partial", partial)
    c3.metric("Not started", not_started)
    c4.metric("Readiness", f"{readiness}%")
    st.progress(readiness / 100)
    if blockers:
        st.markdown(f'<div class="notice"><b>{blockers} checklist blockers remain.</b> Resolve incomplete responses and missing evidence before final internal sign-off.</div>', unsafe_allow_html=True)
    else:
        st.success("All sample checklist items are ready for internal sign-off.")
    st.subheader("Priority actions")
    priority = [x for x in items if x["status"] != "Compliant" or x["evidence"] == 0]
    for x in priority:
        cls = "red" if x["status"] == "Not started" else "amber"
        st.markdown(f'<div class="card"><span class="tag {cls}">{x["status"]}</span><h4>{x["requirement"]}</h4><div class="muted">Owner: {x["owner"]} • Evidence: {x["evidence"]} file(s){" • Due " + x["due"] if x["due"] else ""}</div></div>', unsafe_allow_html=True)
    export_df = pd.DataFrame(items)
    st.download_button("Download internal readiness CSV", export_df.to_csv(index=False).encode("utf-8"), "cmm_readiness_demo.csv", "text/csv")

elif page == "CMM checklist":
    st.title("CMM checklist")
    st.caption("Edit sample responses, ownership and evidence counts. Changes remain only in this browser session.")
    choice = st.segmented_control("Filter", ["All", "Pending", "Compliant"], default="All")
    shown = items if choice == "All" else [x for x in items if (x["status"] == "Compliant") == (choice == "Compliant")]
    for x in shown:
        badge = "green" if x["status"] == "Compliant" else "amber" if x["status"] == "Partially compliant" else "red"
        with st.expander(f'{x["category"]}  •  {x["requirement"]}'):
            st.markdown(f'<span class="tag {badge}">{x["status"]}</span>', unsafe_allow_html=True)
            a, b, c = st.columns([1.1, 1.4, .7])
            new_status = a.selectbox("Response", ["Compliant", "Partially compliant", "Not started", "Not applicable"], index=["Compliant", "Partially compliant", "Not started", "Not applicable"].index(x["status"]) if x["status"] in ["Compliant", "Partially compliant", "Not started", "Not applicable"] else 0, key=f'status_{x["id"]}')
            owner_options = ["Unassigned"] + TEAM
            new_owner = b.selectbox("Owner", owner_options, index=owner_options.index(x["owner"]), key=f'owner_{x["id"]}')
            new_evidence = c.number_input("Evidence", min_value=0, max_value=25, value=int(x["evidence"]), key=f'evidence_{x["id"]}')
            new_note = st.text_area("Internal note", value=x["note"], key=f'note_{x["id"]}')
            uploaded = st.file_uploader("Attach dummy or redacted evidence", key=f'file_{x["id"]}')
            if st.button("Save item", key=f'save_{x["id"]}'):
                x.update(status=new_status, owner=new_owner, evidence=int(new_evidence) + (1 if uploaded else 0), note=new_note)
                if uploaded:
                    st.session_state.uploads.append({"name": uploaded.name, "size": uploaded.size, "item": x["requirement"]})
                st.success("Item updated for this demo session.")
                st.rerun()

elif page == "Document vault":
    st.title("Document vault")
    st.caption("Sample document register plus session-only uploads. Do not upload confidential information to this prototype.")
    for name, version, status, size in SAMPLE_DOCS:
        cls = "green" if status == "Approved" else "amber" if status == "Pending review" else "blue"
        st.markdown(f'<div class="card"><span class="tag {cls}">{status}</span><h4>{name}</h4><div class="muted">{version} • {size}</div></div>', unsafe_allow_html=True)
    for doc in st.session_state.uploads:
        st.markdown(f'<div class="card"><span class="tag blue">Session upload</span><h4>{doc["name"]}</h4><div class="muted">Linked to: {doc["item"]} • {round(doc["size"]/1024)} KB</div></div>', unsafe_allow_html=True)
    general = st.file_uploader("Upload a dummy or redacted document", accept_multiple_files=True)
    if st.button("Add to session vault") and general:
        for f in general:
            st.session_state.uploads.append({"name": f.name, "size": f.size, "item": "General evidence"})
        st.success(f"Added {len(general)} file(s) to this session.")
        st.rerun()

elif page == "Review & approval":
    st.title("Review and approval")
    st.caption("Demonstrates separation between preparation, review and Principal Officer sign-off.")
    st.markdown('<div class="card"><span class="tag green">Completed</span><h4>Preparer — Arjun Nair</h4><div class="muted">Sample evidence uploaded and checklist prepared.</div></div>', unsafe_allow_html=True)
    st.session_state.reviewer_done = st.checkbox("Compliance Officer review completed", value=st.session_state.reviewer_done)
    can_sign = blockers == 0 and st.session_state.reviewer_done
    if blockers:
        st.warning(f"Principal Officer sign-off is blocked by {blockers} incomplete checklist item(s).")
    elif not st.session_state.reviewer_done:
        st.info("Complete Compliance Officer review before final sign-off.")
    if st.button("Apply Principal Officer sign-off", disabled=not can_sign):
        st.session_state.po_done = True
        st.success("Demo sign-off recorded for this browser session.")
    if st.session_state.po_done:
        st.success("Principal Officer sign-off completed.")
    audit = pd.DataFrame([{"Step":"Preparation","Person":"Arjun Nair","Status":"Complete"},{"Step":"Review","Person":"Priya Mehta","Status":"Complete" if st.session_state.reviewer_done else "Pending"},{"Step":"Final sign-off","Person":"R. Sharma","Status":"Complete" if st.session_state.po_done else "Pending"}])
    st.download_button("Download approval trail", audit.to_csv(index=False).encode("utf-8"), "approval_trail_demo.csv", "text/csv")

else:
    st.title("CA feedback")
    st.caption("No meeting required. Record whether the workflow resembles real PMS compliance preparation.")
    score = st.radio("Does this workflow reflect real practice?", ["Yes, broadly", "Partly", "No"], horizontal=True)
    missing = st.text_area("What is missing or incorrect?")
    useful = st.multiselect("Most useful areas", ["Ownership", "Evidence tracking", "Review workflow", "Deadline dashboard", "Export pack", "Audit trail"])
    if st.button("Prepare feedback summary"):
        summary = f"Workflow fit: {score}\nMost useful: {', '.join(useful) or 'Not selected'}\nComments: {missing or 'None'}\n"
        st.download_button("Download feedback", summary.encode("utf-8"), "ca_feedback.txt", "text/plain")
        st.success("Feedback summary prepared. Nothing was transmitted externally.")

st.markdown("""<div class="legal"><b>Important:</b> This prototype uses fictional names, masked registration details and illustrative controls and dates. A qualified compliance professional must validate the exact questionnaire, applicability, deadlines, evidence and submission format against current official requirements. It does not provide legal advice, submit to any regulator or guarantee acceptance.</div>""", unsafe_allow_html=True)
