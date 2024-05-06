import streamlit as st
from data_management import  approve_completion, edit_completion,check_action_and_prompt_password
from utils import format_proposal_as_markdown, format_completion_as_markdown,archive_source_repo_into_target
import pandas as pd

# local_dir = r"D:\Capstone Website - streamlit_dup\Data-Science-Capstone-Website\github clones"
# target_repo_url = "https://github.com/Renga-99/Data-Science-Capstone-Website.git"
# source_repo_url = "https://github.com/mecaneer23/python-snake-game.git"
def pending_approval_page(session):
    """
    Displays a page for approving, rejecting, or editing proposals that are pending approval.

    This function iterates through a session containing proposal data, displaying each proposal in an expandable section
    with buttons for approval, rejection, or editing. User actions trigger updates to the session state which are then handled by `check_action_and_prompt_password`.

    Parameters:
    - session (DataFrame): The DataFrame containing the proposals to be displayed and acted upon.

    There are no return values. This function interacts with the session state based on user actions.
    """
    # print(st.session_state['proposals']) 
    session = session.to_dict('index')
    session = [value for value in session.values()]
    if session:
        for index, proposal in enumerate(session):
            with st.expander(f"Approve/Reject/Edit:   {proposal['project_name']}, Year - {proposal['year']}, Semester - {proposal['semester']}, and Contributors - {proposal['contributors']}"):
                st.markdown(format_proposal_as_markdown(proposal), unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Approve", key=f"approve_{index}"):
                        st.session_state['action_type'] = 'approve'
                        st.session_state['action_index'] = index

                with col2:
                    if st.button("Reject", key=f"reject_{index}"):
                        st.session_state['action_type'] = 'reject'
                        st.session_state['action_index'] = index

                with col3:
                    if st.button("Edit", key=f"edit_{index}"):
                        st.session_state['action_type'] = 'edit'
                        st.session_state['action_index'] = index

        check_action_and_prompt_password()
    else:
        st.write("No pending proposals")


def show_approved(proposal):
    """
    Displays approved proposals in a tabular format.

    Parameters:
    - proposal (DataFrame): The DataFrame containing approved proposals to be displayed.

    There are no return values. This function updates the UI to show a table or a message if there are no proposals.
    """
    
    if st.session_state['approved']:
        st.table(proposal)
    else:
        st.write("No approved proposals")

def show_rejected(proposal):
    """
    Displays rejected proposals in a tabular format.

    Parameters:
    - proposal (DataFrame): The DataFrame containing rejected proposals to be displayed.

    There are no return values. This function updates the UI to show a table or a message if there are no proposals.
    """
    if st.session_state['rejected']:
        st.table(proposal)
    else:
        st.write("No rejected proposals")


def pending_completion_page(session):
    """
    Displays a page for approving or editing project completions that are pending approval.

    This function iterates through a session containing completion data, displaying each completion in an expandable section
    with options to approve or edit the completion details.

    Parameters:
    - session (DataFrame): The DataFrame containing the completions to be displayed and acted upon.

    There are no return values. This function interacts with the session state based on user actions.
    """
    session = session.to_dict('index')
    session = [value for value in session.values()]

    if session:
        for index, completion in enumerate(session):
            with st.expander(f"Approve/Edit Project Completion {completion['project_name']}"):            
                proposal_id_to_remove = completion["completion_id"]
                for i, proposal in enumerate(st.session_state['approved']):
                    if proposal.get('proposal_id') == proposal_id_to_remove:
                        del st.session_state['approved'][i]
                        break
                approve_completion(index) 
    else:
        st.write("No pending project completions")

def show_completed_projects(completion):
    """
    Displays completed projects in a tabular format.

    Parameters:
    - completion (DataFrame): The DataFrame containing completed projects to be displayed.

    There are no return values. This function updates the UI to show a table or a message if there are no completed projects.
    """
    if st.session_state['approved_completion']:
        st.table(completion)
    else:
        st.write("No completed projects")

