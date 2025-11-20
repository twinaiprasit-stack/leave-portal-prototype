# app.py
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Leave & Time Portal",
    page_icon="🗓️",
    layout="wide"
)

# --------- Session State (login & page) ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# --------- Fake data (demo only) ----------
FAKE_QUOTA = {
    "annual": {"remaining": 10, "total": 15, "label": "Annual Leave"},
    "sick": {"remaining": 2, "total": 10, "label": "Sick Leave"},
    "business": {"remaining": 1, "total": 5, "label": "Business Leave"},
}

FAKE_ACTIVITY = [
    {
        "title": "Annual Leave · 10–12 Nov 2025",
        "status": "Pending DM",
        "detail": "Waiting for DM approval",
    },
    {
        "title": "Sick Leave · 03 Nov 2025",
        "status": "Approved",
        "detail": "Approved by DM & HR",
    },
    {
        "title": "Business Leave · 25 Oct 2025",
        "status": "Rejected",
        "detail": "Rejected · insufficient detail",
    },
]

# --------- Helper ---------
def badge_status(text: str):
    if text.lower().startswith("pending"):
        st.markdown(
            f"<span style='background:#FEF9C3;"
            f"border:1px solid #FACC15;border-radius:999px;"
            f"padding:2px 8px;font-size:11px;color:#854D0E;'>● {text}</span>",
            unsafe_allow_html=True,
        )
    elif text.lower().startswith("approved"):
        st.markdown(
            f"<span style='background:#DCFCE7;"
            f"border:1px solid #22C55E;border-radius:999px;"
            f"padding:2px 8px;font-size:11px;color:#166534;'>✓ {text}</span>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<span style='background:#FEE2E2;"
            f"border:1px solid #F97373;border-radius:999px;"
            f"padding:2px 8px;font-size:11px;color:#B91C1C;'>! {text}</span>",
            unsafe_allow_html=True,
        )


# --------- Login screen ----------
def login_view():
    st.markdown("### Leave & Time Portal")
    st.caption("Sign in with your corporate account")

    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("ID / Username", value="", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            remember = st.checkbox("Remember me on this device", value=True)
            submitted = st.form_submit_button("Sign in", use_container_width=True)

        if submitted:
            if username.strip() and password.strip():
                st.session_state.logged_in = True
                st.success("Signed in successfully. Welcome to Leave & Time Portal.")
            else:
                st.error("Please enter both username and password.")

    with col2:
        st.info(
            "🔐 This is a **prototype** login. In real use, it should connect to AD/SSO.",
            icon="ℹ️",
        )
        st.write("**PDPA Note**")
        st.caption(
            "User data and leave information must be handled according to internal "
            "security & PDPA policies."
        )


# --------- Dashboard view ----------
def dashboard_view():
    st.subheader("Dashboard")
    st.caption("Your leave summary and recent activity")

    # KPI cards
    c1, c2, c3 = st.columns(3)
    with c1:
        k = FAKE_QUOTA["annual"]
        st.metric("Annual Leave", f"{k['remaining']} / {k['total']} days")
    with c2:
        k = FAKE_QUOTA["sick"]
        st.metric("Sick Leave", f"{k['remaining']} / {k['total']} days")
    with c3:
        k = FAKE_QUOTA["business"]
        st.metric("Business Leave", f"{k['remaining']} / {k['total']} days")

    st.markdown("---")

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("#### Recent leave activity")
        for item in FAKE_ACTIVITY:
            with st.container():
                st.markdown(f"**{item['title']}**")
                cols = st.columns([2, 1])
                with cols[0]:
                    st.caption(item["detail"])
                with cols[1]:
                    badge_status(item["status"])
                st.markdown("---")

    with right:
        st.markdown("#### Quick actions")
        if st.button("➕ Request new leave", use_container_width=True):
            st.session_state.page = "Request Leave"
            st.experimental_rerun()
        st.caption("You can also review your recent approvals above.")

        st.markdown("#### This month (mock calendar)")
        st.caption("Simple preview – real calendar UI can be integrated later.")
        st.write("📅 Today:", date.today().strftime("%d %b %Y"))
        st.markdown(
            "- 🔵 **Leave days**: 7–9 Nov (Annual Leave)\n"
            "- 🟢 **Approved leave**: 3 Nov (Sick Leave)\n"
            "- 🔴 **Rejected**: 25 Oct (Business Leave)"
        )

        st.markdown("#### Notifications")
        st.info("✅ Leave approved by HR – Sick Leave · 03 Nov 2025", icon="✅")
        st.info("⏳ Your new leave is waiting for DM approval.", icon="⏳")
        st.info("📤 Timesheet CSV export is ready.", icon="📤")


# --------- Request Leave view ----------
def request_leave_view():
    st.subheader("Request new leave")
    st.caption("Fill in details and submit for approval.")

    left, right = st.columns([1.5, 1])

    with left:
        with st.form("leave_form"):
            leave_type = st.selectbox(
                "Leave type",
                ["Annual Leave", "Sick Leave", "Business Leave"],
                index=0,
            )

            c1, c2 = st.columns(2)
            with c1:
                date_from = st.date_input("From", value=date.today())
            with c2:
                date_to = st.date_input("To", value=date.today())

            half_day = st.checkbox("Half day")
            half_session = None
            if half_day:
                half_session = st.selectbox("Session", ["Morning (AM)", "Afternoon (PM)"])

            reason = st.text_area(
                "Reason",
                placeholder="e.g. Personal errands, family matters, or medical check-up.",
            )
            attachment = st.file_uploader("Attachment (optional)")

            submit = st.form_submit_button("Submit request")

        if submit:
            if not reason.strip():
                st.error("Please fill in the reason before submitting.")
            elif date_to < date_from:
                st.error("End date cannot be earlier than start date.")
            else:
                st.success(
                    "Leave request submitted. Waiting for DM and HR approval "
                    "(mock workflow)."
                )

    with right:
        # Map type name -> quota key
        lt_map = {
            "Annual Leave": "annual",
            "Sick Leave": "sick",
            "Business Leave": "business",
        }
        q_key = lt_map.get(leave_type, "annual")
        q = FAKE_QUOTA[q_key]

        st.markdown("#### Leave quota overview")
        st.metric("Remaining", f"{q['remaining']} days")
        st.metric("Total", f"{q['total']} days")

        if q["remaining"] <= 1 and leave_type == "Business Leave":
            st.warning(
                "Your business leave quota is relatively low. "
                "If requested days exceed remaining quota, "
                "the system should block submission and ask you to contact HR.",
                icon="⚠️",
            )
        else:
            if leave_type == "Sick Leave":
                st.info(
                    "Sick leave may require a medical certificate for HR approval.",
                    icon="💊",
                )
            else:
                st.info(
                    "You have enough quota for normal requests.",
                    icon="✅",
                )

        st.markdown("#### Approval flow")
        st.markdown(
            "1. Request goes to your **DM** for review.\n"
            "2. After DM approval, **HR** will review and deduct leave quota.\n"
            "3. You receive notifications at every step."
        )


# --------- Timesheet preview ----------
def timesheet_view():
    st.subheader("Timesheet overview (preview)")
    st.caption("Simple mock view – connect to real data later.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total hours", "168 h", "This month")
    with c2:
        st.metric("Average / day", "8.0 h", "Mon–Fri")
    with c3:
        st.metric("Overtime", "6 h", "Logged as OT")

    st.markdown("---")
    st.markdown("#### Recent timesheet entries")

    import pandas as pd

    data = pd.DataFrame(
        [
            {
                "Date": "2025-11-17",
                "Project": "Leave Portal Enhancement",
                "Hours": 8.0,
                "Note": "UI refinement & testing",
            },
            {
                "Date": "2025-11-16",
                "Project": "Core HR Integration",
                "Hours": 7.5,
                "Note": "API mapping & review",
            },
            {
                "Date": "2025-11-15",
                "Project": "Meeting & Planning",
                "Hours": 8.0,
                "Note": "Sprint planning",
            },
        ]
    )
    st.dataframe(data, use_container_width=True, hide_index=True)

    if st.button("Export CSV"):
        st.success("Timesheet export started (demo only). In real system, generate CSV file.")


# --------- MAIN APP ---------
def main():
    if not st.session_state.logged_in:
        login_view()
        return

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🗓️ Leave & Time Portal")
        choice = st.radio(
            "Navigation",
            ["Dashboard", "Request Leave", "Timesheet"],
            index=["Dashboard", "Request Leave", "Timesheet"].index(st.session_state.page),
        )
        st.session_state.page = choice

        st.markdown("---")
        st.caption("Role: Employee (demo)")
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.experimental_rerun()

    if st.session_state.page == "Dashboard":
        dashboard_view()
    elif st.session_state.page == "Request Leave":
        request_leave_view()
    elif st.session_state.page == "Timesheet":
        timesheet_view()


if __name__ == "__main__":
    main()
