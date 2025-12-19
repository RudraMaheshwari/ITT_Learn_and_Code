"""Email count tracking dashboard module.

This module provides the dashboard for viewing email sequence tracking
data with pagination and stage reference.
"""
from typing import Dict, List, Any, Tuple
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from src.database.repositories import EmailSequenceTrackingRepository
from src.utils.logger import get_logger
from src.utils.dashboard_helpers import get_per_page, get_refresh_interval, display_pagination_controls

logger = get_logger(__name__)

EMAIL_STAGE_INFO = {
    "1": "Welcome to Our Platform",
    "2a": "Can you confirm you received our email?",
    "2b": "What's holding you back?",
    "3": "Quick reminder",
    "4": "Special offer for you",
    "5": "Success stories from our customers",
    "6": "Last chance to join us",
    "7": "Final follow-up",
}

COLUMN_MAPPINGS = {
    'id': 'ID',
    'lead_id': 'Lead ID',
    'email': 'Email',
    'name': 'Name',
    'initial_email_sent_time': 'Initial Email Sent',
    'email_step_number': 'Email Stage',
    'last_email_sent_time': 'Last Email Sent'
}

DISPLAY_COLUMNS = ['Name', 'Email', 'Email Stage', 'Initial Email Sent', 'Last Email Sent']

def _init_session_state() -> None:
    """Initialize pagination session state."""
    if 'email_page' not in st.session_state:
        st.session_state.email_page = 1

def _fetch_tracking_data(page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
    """Fetch paginated email tracking data.
    
    Args:
        page: Current page number
        per_page: Items per page
        
    Returns:
        Tuple of (tracking_data, total_count)
    """
    try:
        return EmailSequenceTrackingRepository.get_email_tracking_paginated(
            page=page,
            per_page=per_page
        )
    except Exception as e:
        logger.exception(f"Error fetching email tracking data: {e}")
        return [], 0

def _prepare_dataframe(tracking_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Prepare and format dataframe for display.
    
    Args:
        tracking_data: List of tracking records
        
    Returns:
        Formatted DataFrame
    """
    df = pd.DataFrame(tracking_data)
    df = df.rename(columns=COLUMN_MAPPINGS)
    
    display_cols = [col for col in DISPLAY_COLUMNS if col in df.columns]
    return df[display_cols]

def _display_stage_reference() -> None:
    """Display email stage reference information."""
    st.divider()
    with st.expander("📋 Email Stage Reference", expanded=False):
        st.markdown("**Each email stage corresponds to a specific email type:**")
        for stage, description in EMAIL_STAGE_INFO.items():
            st.markdown(f"- **Stage {stage}**: {description}")

def display_email_count_dashboard() -> None:
    """Display the Email Count Tracking Dashboard with pagination."""
    try:
        st.header("📧 Email Count Tracking")
        
        st_autorefresh(interval=get_refresh_interval(), key="email_tracking_refresh")
        st.caption("🔄 Auto-refreshing every 5 seconds...")
        
        _init_session_state()
        
        current_page = st.session_state.email_page
        per_page = get_per_page()
        tracking_data, total_count = _fetch_tracking_data(current_page, per_page)
        total_pages = max(1, (total_count + per_page - 1) // per_page)
        
        st.info(f"📈 Email sequence tracking data ({total_count} total records)")
        
        if tracking_data:
            df_display = _prepare_dataframe(tracking_data)
            st.dataframe(df_display, width='stretch', hide_index=True)
            
            st.divider()
            display_pagination_controls(
                current_page=current_page,
                total_pages=total_pages,
                session_state_key="email_page",
                key_prefix="email",
                total_count=total_count,
                record_label="records"
            )
        else:
            st.info("No email tracking data found. Data will appear here when emails are sent to leads.")
        
        _display_stage_reference()
    except Exception as e:
        logger.exception(f"Error displaying email count dashboard: {e}")
        st.error("Unable to load email count dashboard. Please try again.")
