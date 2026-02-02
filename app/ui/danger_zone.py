import streamlit as st

from ..db.database import undo_last_save, clear_history

def render_danger_zone():
    """
    Render the "Danger Zone" section in Streamlit with destructive actions.

    Features:
        - Undo the most recent saved record.
        - Delete all analysis history.
        - Requires confirmation before executing any action.

    Uses:
        st.session_state.confirm_action to track user confirmation.
    """
    st.divider()

    st.markdown("""
    <div style="background:#2b0f0f;padding:20px;border-radius:12px;border:1px solid #ff4d4d">
    <h3 style="color:#ff4d4d;">⚠️ Danger Zone</h3>
    <p style="color:white;">Irreversible actions. Proceed carefully.</p>
    </div>
    """, unsafe_allow_html=True)

    dz1, dz2 = st.columns(2)
    if dz1.button("↩️ Undo Last Save", use_container_width=True):
        st.session_state.confirm_action = "undo"
    if dz2.button("🗑️ Delete ALL History", use_container_width=True):
        st.session_state.confirm_action = "clear"

    if st.session_state.confirm_action:
        st.markdown("""
        <div style="background:#3b0d0d;padding:25px;border-radius:14px;border:2px solid #ff4d4d">
        <h2 style="color:#ff4d4d;">Confirm Action</h2>
        <p style="color:white;">This action cannot be undone.</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        if c1.button("🔥 Yes, Proceed"):
            if st.session_state.confirm_action == "undo":
                undo_last_save()
            else:
                clear_history()
            st.session_state.confirm_action = None
            st.rerun()

        if c2.button("❌ Cancel"):
            st.session_state.confirm_action = None
