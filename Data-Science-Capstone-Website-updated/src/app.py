import streamlit as st
import pandas as pd
from pages import pending_approval_page, show_approved, show_rejected, pending_completion_page, show_completed_projects
from forms import proposal_request_form, completion_form, initialize_placeholder_data
from data_management import initialize_session_state,show_to_edit_completion,show_to_edit_proposals,show_prof_proposals,show_all
import os

def display_sidebar():
    """
    Displays the sidebar for navigation in the Streamlit app.

    This function creates prof sidebar with expandable sections for project proposals and completed projects,
    allowing users to navigate between different pages of the application.
    """

    st.sidebar.title("Navigation")
    projects_options = ["Proposal Request","Proposals by Professors", "Pending Approval", "Edit Proposals", "Rejected Proposals", "Approved Projects", "All Projects"]
    completed_projects_options = ["Project Completion Form", "Completed Projects"] # , "Project Completion Approval", "Edit Project Completion"
    
    # Active page handling
    if 'active_page' not in st.session_state:
        st.session_state.active_page = "Proposal Request" 
    
    with st.sidebar:
        with st.expander("Projects & Proposals"):
            for option in projects_options:
                if st.button(option):
                    st.session_state.active_page = option
        
        with st.expander("Completed Projects"):
            for option in completed_projects_options:
                if st.button(option):
                    st.session_state.active_page = option


def filter_proposals(proposals_df):
    """
    Applies filters to prof DataFrame based on user-selected criteria from the sidebar.

    Parameters:
    - proposals_df (DataFrame): DataFrame containing the project proposals data.

    Returns:
    - DataFrame: Filtered DataFrame based on the selected project name, year, semester, and student name.
    """
    
    if proposals_df.empty:
        return pd.DataFrame()  # Return an empty DataFrame if there are no proposals

    # Sidebar filters
    unique_semesters = proposals_df['semester'].unique().tolist()
    unique_project_names = proposals_df['project_name'].unique().tolist()
    unique_years = proposals_df['year'].unique().tolist()
    unique_names = proposals_df['name'].unique().tolist()
    
    
    selected_project_name = st.sidebar.selectbox("Filter by Project Name:", ['All'] + unique_project_names)
    selected_year = st.sidebar.selectbox("Filter by Year:", ['All'] + unique_years)
    selected_semester = st.sidebar.selectbox("Filter by Semester:", ['All'] + unique_semesters)
    selected_name = st.sidebar.selectbox("Filter by Student Name:", ['All'] + unique_names)

    # Apply filters
    if selected_semester != 'All':
        proposals_df = proposals_df[proposals_df['semester'] == selected_semester]
    if selected_project_name != 'All':
        proposals_df = proposals_df[proposals_df['project_name'] == selected_project_name]
    if selected_year != 'All':
        proposals_df = proposals_df[proposals_df['year'] == selected_year]
    if selected_name != 'All':
        proposals_df = proposals_df[proposals_df['name'] == selected_name]
    
    return proposals_df

def filter_proposals(proposals_df):
    """
    Collects filter options from the sidebar and returns the user-selected filters.

    Parameters:
    - proposals_df (DataFrame): DataFrame containing the project proposals data.

    Returns:
    - tuple: Contains lists of selected filters for project names, years, semesters, names, and prof specific proposal ID.
    """
    
    if proposals_df.empty:
        return [], [], [], [],'' # Return an empty DataFrame if there are no proposals

    # Sidebar filters
    unique_semesters = proposals_df['semester'].unique().tolist()
    unique_project_names = proposals_df['project_name'].unique().tolist()
    unique_years = proposals_df['year'].unique().tolist()
    unique_names = proposals_df['name'].unique().tolist()
    # proposal_id = proposals_df['proposal_id'].tolist()
    
    selected_project_name = st.sidebar.multiselect("Filter by Project Name:",  unique_project_names)
    selected_year = st.sidebar.multiselect("Filter by Year:",  unique_years)
    selected_semester = st.sidebar.multiselect("Filter by Semester:", unique_semesters)
    selected_name = st.sidebar.multiselect("Filter by Student Name:",  unique_names)
    # selected_proposal_id = st.sidebar.selectbox("Filter by proposal id:", ['All'] + proposal_id)
    selected_proposal_id = st.sidebar.text_input("Enter Proposal ID to search:")

    return selected_project_name,selected_year,selected_semester, selected_name,selected_proposal_id

def apply_filters(proposals_df,selected_semester,selected_project_name,selected_year,selected_name,selected_proposal_id):
    """
    Applies user-selected filters to the DataFrame containing project proposals.

    Parameters:
    - proposals_df (DataFrame): The DataFrame to be filtered.
    - selected_semester, selected_project_name, selected_year, selected_name (list): Filters selected by the user.
    - selected_proposal_id (str): Specific proposal ID to filter by.

    Returns:
    - DataFrame: The filtered DataFrame based on the provided criteria.
    """
    if proposals_df.empty:
        return proposals_df
  
    # Apply filters only if selections are made
    if selected_semester:
        proposals_df = proposals_df[proposals_df['semester'].isin(selected_semester)]
    if selected_project_name:
        proposals_df = proposals_df[proposals_df['project_name'].isin(selected_project_name)]
    if selected_year:
        proposals_df = proposals_df[proposals_df['year'].isin(selected_year)]
    if selected_name:
        proposals_df = proposals_df[proposals_df['name'].isin(selected_name)]
    if selected_proposal_id:
        proposals_df = proposals_df[proposals_df['proposal_id'] == selected_proposal_id]
    
    return proposals_df


def main():
    # Path to the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the image file relative to the current script
    image_path = os.path.join(current_dir, '..', 'data', 'gw-data-science-header.jpg')

    # Use Streamlit to display the image
    st.image(image_path, use_column_width=True)
    st.title("Data Science Capstone Website")

    # Initialize session state for app-wide variables
    initialize_session_state()

    # Display sidebar for navigation
    display_sidebar()
    
    proposals_df = pd.DataFrame(st.session_state.get('approved', []))
    rejected_df = pd.DataFrame(st.session_state.get('rejected', []))
    to_edit_df = pd.DataFrame(st.session_state.get('to_edit_proposal', []))
    prof_proposal_df = pd.DataFrame(st.session_state.get('prof_proposal', []))
    completion_df = pd.DataFrame(st.session_state.get('completion', []))
    edit_completion_df = pd.DataFrame(st.session_state.get('edit_completion', []))
    approved_completion_df = pd.DataFrame(st.session_state.get('approved_completion', []))
    prop_df = pd.DataFrame(st.session_state.get('proposals', []))
  
    # Default columns that can be added to the display
    default_columns = ["name", "project_name", "mentor", "semester", "year"]
    # additional columns that can be added to the display
    additional_columns = ["rationale","expected_students", "objective", "github_link", "dataset","timeline","approach","possible_issues","proposal_id","status"] 

    full_df = pd.concat([proposals_df, rejected_df, to_edit_df, prof_proposal_df,completion_df,edit_completion_df,approved_completion_df,prop_df])
    
    proj_name, year, sem, name,proposal_id= filter_proposals(full_df)
    prof = apply_filters(pd.DataFrame(st.session_state.prof_proposal),sem,proj_name, year, name,proposal_id)
    proposal = apply_filters(pd.DataFrame(st.session_state.proposals),sem,proj_name, year, name,proposal_id)
    edit_proposal = apply_filters(pd.DataFrame(st.session_state.to_edit_proposal),sem,proj_name, year, name,proposal_id)
    in_completion = apply_filters(pd.DataFrame(st.session_state.completion),sem,proj_name, year, name,proposal_id)
    edit_completion = apply_filters(pd.DataFrame(st.session_state.edit_completion),sem,proj_name, year, name,proposal_id)
    completed = apply_filters(pd.DataFrame(st.session_state.approved_completion),sem,proj_name, year, name,proposal_id)
    filtered_proposals1 = apply_filters(pd.DataFrame(st.session_state.rejected),sem,proj_name, year, name,proposal_id)
    filtered_proposals2 = apply_filters(pd.DataFrame(st.session_state.approved),sem,proj_name, year, name,proposal_id)
    all_data = apply_filters(full_df,sem,proj_name, year, name,proposal_id)

    # Display content based on the active page
    if st.session_state.active_page == "Proposal Request":

        proposal_request_form()
    
    elif st.session_state.active_page == "Proposals by Professors":
        
        if prof.empty:
            st.write("No matching records found based on the filter criteria.")
        else:
            show_prof_proposals(prof)

    elif st.session_state.active_page == "Pending Approval":

        if proposal.empty:
            st.write("No matching records found based on the filter criteria.")
        else:
            pending_approval_page(proposal)
    elif st.session_state.active_page == "Edit Proposals":

        show_to_edit_proposals(edit_proposal)

    elif st.session_state.active_page == "Rejected Proposals":
        # Use prof multiselect widget to allow users to select additional columns to display
        selected_columns = st.multiselect("Select additional columns to display:", additional_columns)
        # Combine default columns with selected additional columns
        columns_to_display = default_columns + selected_columns

        show_rejected(filtered_proposals1[columns_to_display])

    elif st.session_state.active_page == "Approved Projects":
        # Use prof multiselect widget to allow users to select additional columns to display
        selected_columns = st.multiselect("Select additional columns to display:", additional_columns)

        # Combine default columns with selected additional columns
        columns_to_display = default_columns + selected_columns
        # filtered_proposals = filter_proposals(proposals_df) 
        # st.write(filtered_proposals)
        show_approved(filtered_proposals2[columns_to_display]) 

    elif st.session_state.active_page == "Project Completion Form":
        completion_form()
        
    elif st.session_state.active_page == "Completed Projects":
        # Use prof multiselect widget to allow users to select additional columns to display
        selected_columns = st.multiselect("Select additional columns to display:", additional_columns)

        # Combine default columns with selected additional columns
        columns_to_display = default_columns + selected_columns
        show_completed_projects(completed[columns_to_display])
        
    elif st.session_state.active_page == "All Projects":
        # selected_columns = st.multiselect("Select additional columns to display:", additional_columns)
        # columns_to_display = default_columns + selected_columns
        show_all(filtered_proposals2,filtered_proposals1,edit_proposal,completed,edit_completion)
        st.header("All Projects  - Downloadable in CSV format")
        st.write(all_data[["name", "project_name", "mentor", "semester", "year", "status","proposal_id"]])
    else:
        st.write("Select an option from the sidebar.")

if __name__ == "__main__":
    main()
