"""Dashboard helper utilities.

This module provides common utility functions used across dashboard modules.
"""
from src.config.settings import get_config


def get_per_page() -> int:
    """Get items per page from settings.
    
    Returns:
        Number of items to display per page, defaults to 25
    """
    try:
        return get_config().dashboard_per_page
    except Exception:
        return 25


def get_refresh_interval() -> int:
    """Get auto refresh interval from settings.
    
    Returns:
        Auto refresh interval in milliseconds, defaults to 5000
    """
    try:
        return get_config().auto_refresh_interval_ms
    except Exception:
        return 5000


def display_pagination_controls(
    current_page: int,
    total_pages: int,
    session_state_key: str,
    key_prefix: str,
    total_count: int = None,
    record_label: str = "records"
) -> None:
    """Display pagination navigation controls.
    
    This is a reusable pagination component used across dashboards.
    
    Args:
        current_page: Current page number
        total_pages: Total number of pages
        session_state_key: The session state key for storing page number
        key_prefix: Prefix for button keys to ensure uniqueness
        total_count: Optional total record count to display
        record_label: Label for records (e.g., "records", "leads")
    """
    import streamlit as st
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("⏮️ First", disabled=current_page <= 1, key=f"{key_prefix}_first"):
            st.session_state[session_state_key] = 1
            st.rerun()
    
    with col2:
        if st.button("◀️ Previous", disabled=current_page <= 1, key=f"{key_prefix}_prev"):
            st.session_state[session_state_key] = current_page - 1
            st.rerun()
    
    with col3:
        if total_count is not None:
            center_text = f"Page **{current_page}** of **{total_pages}** ({total_count} {record_label})"
        else:
            center_text = f"Page {current_page} of {total_pages}"
        st.markdown(
            f"<div style='text-align: center;'>{center_text}</div>",
            unsafe_allow_html=True
        )
    
    with col4:
        if st.button("Next ▶️", disabled=current_page >= total_pages, key=f"{key_prefix}_next"):
            st.session_state[session_state_key] = current_page + 1
            st.rerun()
    
    with col5:
        if st.button("Last ⏭️", disabled=current_page >= total_pages, key=f"{key_prefix}_last"):
            st.session_state[session_state_key] = total_pages
            st.rerun()
