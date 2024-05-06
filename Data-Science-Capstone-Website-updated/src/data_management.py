import streamlit as st
from PIL import Image
import pandas as pd
from utils import pil_image_to_base64,format_proposal_as_markdown, resize_image, generate_unique_id
import base64
from io import BytesIO
import os

# Get the password from the environment variable
PASSWORD = os.getenv("STREAMLIT_PASSWORD")

def initialize_session_state():
    """
    Initializes the session state for a Streamlit application by setting default values for various state variables.

    This function populates the `st.session_state` with default values for a range of session variables if they do not already exist. The session variables are used to track the state of the application, including user interactions and data management tasks.

    The session variables initialized are:
    - `proposals`: List to store proposal entries.
    - `approved`: List to store approved proposals.
    - `rejected`: List to store rejected proposals.
    - `completion`: List to store completion statuses.
    - `approved_completion`: List to store completion statuses of approved items.
    - `edit_completion`: List to store completion statuses of items being edited.
    - `objective_image_up`: Placeholder for an uploaded objective image.
    - `dataset_image_up`: Placeholder for an uploaded dataset image.
    - `possible_issues_image_up`: Placeholder for an uploaded image of possible issues.
    - `to_edit_proposal`: List to store proposals selected for editing.
    - `editing_index`: Index of the proposal being edited.
    - `show_edit_form`: Flag to show or hide the editing form.
    - `uploaded_word_doc`: Placeholder for an uploaded Word document.
    - `uploaded_word_doc_name`: Name of the uploaded Word document.
    - `prof_proposal`: List to store profiling information for proposals.
    - `prof_edit`: List to store profiling information for edits.
    - `prof_submit`: List to store profiling information for submissions.
    - `prof_delete`: List to store profiling information for deletions.

    No parameters are required, and there is no return value.
    """
    default_values = {
        'proposals': [],
        'approved': [],
        'rejected': [],
        'completion': [],
        'approved_completion': [],
        'edit_completion': [],
        'objective_image_up': None,
        'dataset_image_up': None,
        'possible_issues_image_up': None,
        'to_edit_proposal': [],
        'editing_index': None,
        'show_edit_form': None,
        'uploaded_word_doc':None,
        'uploaded_word_doc_name' : None,
        'prof_proposal': [],
        'prof_edit': [],
        'prof_submit': [],
        'prof_delete': []
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def submit_proposal(proposal_data):
    """
    Adds a new proposal to the session state and notifies the user of successful submission.

    This function appends the provided proposal data to the 'proposals' list within the Streamlit session state (`st.session_state`). 
    It prints the updated list of proposals to the console and displays a success message to the user through the Streamlit UI.

    Parameters:
    - proposal_data (Any): The data representing a proposal. This could be a string, dictionary, or any other data structure suitable for representing proposal details.

    There are no return values for this function.
    """
    st.session_state['proposals'].append(proposal_data)
    print("Current proposals:", st.session_state['proposals'])
    st.success("Proposal submitted successfully!")


def approve_proposal(index):
    """
    Approves a proposal based on the given index, updates its status, and moves it to the approved list.

    This function removes the proposal at the specified index from the 'proposals' list, updates its status to "Approved.. In Progress", 
    and then appends it to the 'approved' list. After updating the proposal status, it triggers a rerun of the Streamlit app to reflect the changes in the UI.

    Parameters:
    - index (int): The index of the proposal in the 'proposals' list to be approved.

    There are no return values for this function.
    """
    proposal = st.session_state['proposals'].pop(index)
    proposal['status'] = "Approved.. In Progress"
    st.session_state['approved'].append(proposal)
    st.rerun()

def reject_proposal(index):
    """
    Rejects a proposal based on the given index, updates its status, and moves it to the rejected list.

    This function removes the proposal at the specified index from the 'proposals' list, updates its status to "Rejected", 
    and then appends it to the 'rejected' list. It triggers a rerun of the Streamlit app to reflect these changes in the UI.

    Parameters:
    - index (int): The index of the proposal in the 'proposals' list to be rejected.

    There are no return values for this function.
    """
    proposal = st.session_state['proposals'].pop(index)
    proposal['status'] = "Rejected"
    st.session_state['rejected'].append(proposal)
    st.rerun()

def edit_proposal(index):
    """
    Marks a proposal for editing based on the given index, updates its status, and moves it to the editing list.

    This function removes the proposal at the specified index from the 'proposals' list, updates its status to "Proposal to be edited",
    and then appends it to the 'to_edit_proposal' list. It triggers a rerun of the Streamlit app to update the UI accordingly.

    Parameters:
    - index (int): The index of the proposal in the 'proposals' list to be marked for editing.

    There are no return values for this function.
    """
    proposal = st.session_state['proposals'].pop(index)
    proposal['status'] = "Proposal to be edited"
    st.session_state['to_edit_proposal'].append(proposal)
    st.rerun()
    

def submit_completion(completion):
    """
    Submits a project completion form and records it in the session state.

    This function appends the provided completion data to the 'completion' list within the Streamlit session state and displays a success message to the user.

    Parameters:
    - completion (dict): The data representing a project completion form.

    There are no return values for this function.
    """
    st.session_state['completion'].append(completion)
    st.success("Project completion form submitted successfully!")

def approve_completion(index):
    """
    Approves a project completion form based on the given index and updates its status.

    This function removes the project completion data at the specified index from the 'completion' list, updates its status to "Completed", 
    and appends it to the 'approved_completion' list. It then triggers a rerun of the Streamlit app to reflect the changes.

    Parameters:
    - index (int): The index of the completion form in the 'completion' list to be approved.

    There are no return values for this function.
    """
    completion = st.session_state['completion'].pop(index)
    completion["status"] = "Completed"
    st.session_state['approved_completion'].append(completion)
    st.rerun()

def edit_completion(index):
    """
    Marks a project completion form for editing based on the given index and updates its status.

    This function removes the completion form at the specified index from the 'completion' list, updates its status to "Pending Completion", 
    and appends it to the 'edit_completion' list. It triggers a rerun of the Streamlit app to update the UI accordingly.

    Parameters:
    - index (int): The index of the completion form in the 'completion' list to be edited.

    There are no return values for this function.
    """
    completion = st.session_state['completion'].pop(index)
    completion["status"] = "Pending Completion"
    st.session_state['edit_completion'].append(completion)
    st.rerun()

def show_approved_completion():
    """
    Displays a DataFrame of all approved completion forms using Streamlit.

    This function converts the 'approved_completion' list into a DataFrame and displays it in the Streamlit app. 
    This allows users to visually inspect the details of all approved project completions.

    There are no parameters or return values for this function.
    """
    df_approved = pd.DataFrame(st.session_state.approved_completion)
    st.write(df_approved)



def submit_prof_proposal(proposal_data):
    """
    Submits a proposal for proffesors and adds it to the session state.

    This function appends the provided profiling proposal data to the 'prof_proposal' list within the Streamlit session state, 
    prints the updated list of profiling proposals to the console, and displays a success message to the user.

    Parameters:
    - proposal_data (dict): The data representing a professors proposal.

    There are no return values for this function.
    """
    st.session_state['prof_proposal'].append(proposal_data)
    print("Current proposals:", st.session_state['prof_proposal'])
    st.success("Proposal submitted successfully!")

def delete_prof_proposal(index):
    """
    Deletes a proffesors proposal based on the given index and updates the session state.

    This function removes the profiling proposal at the specified index from the 'prof_proposal' list and appends it to the 'prof_delete' list,
    effectively marking it as deleted. It then triggers a rerun of the Streamlit app to reflect the changes.

    Parameters:
    - index (int): The index of the professors proposal in the 'prof_proposal' list to be deleted.

    There are no return values for this function.
    """
    proposal = st.session_state['prof_proposal'].pop(index)
    st.session_state['prof_delete'].append(proposal)
    st.rerun()

def show_prof_proposals(session):
    """
    Displays all proposals from the provided session data using Streamlit components,
    with options to edit or delete each proposal interactively.

    This function takes a session list of proposal dictionaries and uses Streamlit's UI components to display each proposal. 
    Proposals are shown with expanders containing detailed views, and include interactive options to edit or delete proposals. 
    If editing is initiated, it shows a form populated with the proposal's data allowing modifications.

    Parameters:
    - session (list of dicts): The session list containing proposal data. Each dictionary in the list should represent a proposal with complete details.

    This function does not return values but modifies the Streamlit session state based on user interactions such as editing or deleting proposals.

    Additional features include:
    - Displaying images linked to proposals if uploaded, e.g., objective images, dataset images, and possible issues images.
    - Providing interactive buttons within each proposal's view to trigger editing or deletion of the proposal.
    - If an edit is triggered, a detailed form is provided to edit and resubmit the proposal with new data.
    """

    matching_proposals = pd.DataFrame(session)

    # st.write(matching_proposals)
    if not matching_proposals.empty:
        for index, proposal in matching_proposals.iterrows():
            with st.expander(f"Proposal {index + 1}: {proposal['name']}"):


                left_col, right_col = st.columns(2)

                with left_col:

                    st.write(f"**Project Name:** {proposal['project_name']}")
                    st.write(f"**Mentor:** {proposal['mentor']}")
                    st.write(f"**Objective:** {proposal['objective']}")
                    if st.session_state.get('objective_image_up') is not None:
                        st.image(st.session_state['objective_image_up'], caption="Objective Image", use_column_width=True)
                    else:
                        st.write("No objective image uploaded.")
                    st.write(f"**Rationale:** {proposal['rationale']}")
                    st.write(f"**Dataset:** {proposal['dataset']}")
                    if st.session_state.get('dataset_image_up') is not None:
                        st.image(st.session_state['dataset_image_up'], caption=" dataset image ", use_column_width=True)
                    else:
                        st.write("No Dataset Image uploaded.")
                    
                    st.write(f"**Timeline:** {proposal['timeline']}")
                    st.write(f"**Contributors:** {proposal['contributors']}")
                    

                with right_col:
                    st.write(f"**Semester:** {proposal['semester']}")
                    st.write(f"**Expected Students:** {proposal['expected_students']}")
                    st.write(f"**Mentor Email:** {proposal['mentor_email']}")
                    st.write(f"**Approach:** {proposal['approach']}")
                    st.write(f"**Possible Issues:** {proposal['possible_issues']}")
                    if st.session_state.get('dataset_image_up') is not None:
                        st.image(st.session_state['possible_issues_image_up'], caption=" Possible Issues Image ", use_column_width=True)
                    else:
                        st.write("No Possible Issues Image uploaded.")
                    
                    st.write(f"**GitHub Link:** {proposal['github_link']}")
                    st.write(f"**Year:** {proposal['year']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_{index}"):
                        st.session_state['editing_index'] = index
                        st.session_state['show_edit_form'] = True
                        break  
                with col2:
                    if st.button("Delete", key=f"delete_{index}"):
                        st.session_state['action_type'] = 'delete'
                        st.session_state['action_index'] = index
                        
            check_action_and_prompt_password()


        # Check if we should display the editing form
        if st.session_state.get('show_edit_form', False):
            # Obtain the index of the proposal being edited

            with st.form(key='edit_proposal_form'):                
                    st.subheader("Edit Proposal Request Form")
                    left_col, right_col = st.columns(2)
                    
                    with left_col:
                        # proposal_id = prof_df.loc[index,"proposal_id"]
                        name = st.text_input("Name",value=matching_proposals.loc[index,"name"])
                        project_name = st.text_input("Project Name",value=matching_proposals.loc[index,"project_name"])
                        mentor = st.text_input("Mentor for the project",value=matching_proposals.loc[index,"mentor"])
                        github_link = st.text_input("Github Link",value=matching_proposals.loc[index,"github_link"])
                        objective = st.text_area("Objective",value=matching_proposals.loc[index,"objective"])
                        rationale = st.text_area("Rationale",value=matching_proposals.loc[index,"rationale"])
                        timeline = st.text_area("Timeline",value=matching_proposals.loc[index,"timeline"])
                        contributors = st.text_input("Contributors",value=matching_proposals.loc[index,"contributors"])

                    with right_col:
                        semester = st.selectbox("Semester", options=["Spring", "Summer", "Fall"])
                        expected_students = st.number_input("Expected number of students",value=matching_proposals.loc[index,"expected_students"])
                        mentor_email = st.text_input("Mentor email",value=matching_proposals.loc[index,"mentor_email"])
                        dataset = st.text_area("Dataset",value=matching_proposals.loc[index,"dataset"])
                        approach = st.text_area("Approach",value=matching_proposals.loc[index,"approach"])
                        possible_issues = st.text_area("Possible Issues",value=matching_proposals.loc[index,"possible_issues"])
                        year = st.selectbox("Year", options=["2021", "2022", "2023", "2024"])

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        proposal_id = generate_unique_id()
                        proposal_data_edit = {
                            "name": name,
                            "project_name": project_name,
                            "mentor": mentor,
                            "github_link": github_link,
                            "objective": objective,
                            "rationale": rationale,
                            "timeline": timeline,
                            "contributors": contributors,
                            "semester": semester,
                            "expected_students": expected_students,
                            "mentor_email": mentor_email,
                            "dataset": dataset,
                            "approach": approach,
                            "possible_issues": possible_issues,
                            "year": year,
                            "proposal_id": proposal_id,
                            "proposed_by_professor": False 
                        
                        }
                        
                        # Update the appropriate proposal in the session state
                        # st.session_state['to_edit_proposal'][index].append(proposal_data_edit)
                        # Reset flags to hide the form
                        st.session_state['show_edit_form'] = False
                        st.session_state['editing_index'] = None

                        # moving the updated proposal back to the 'proposals' list
                        st.session_state.proposals.append(proposal_data_edit)
                        st.info(f"Note your new Project id{proposal_id}")
                    
                        # st.rerun() 


    
def show_to_edit_proposals(session):
    proposal_id_to_edit = st.text_input("Enter the Proposal ID to edit:")
    # Convert DataFrame for easier ID checking
    df_edit = pd.DataFrame(session)
    st.write(df_edit)
                            
    if proposal_id_to_edit:

        # Check if the entered ID matches any proposal ID
        # st.write(df_edit[df_edit['proposal_id'] == proposal_id_to_edit])
        matching_proposals = df_edit[df_edit['proposal_id'] == proposal_id_to_edit]

        if not matching_proposals.empty:
                    
            for index, proposal in matching_proposals.iterrows():
                    with st.expander(f"Proposal {index + 1}: {proposal['name']}"):
    

                        left_col, right_col = st.columns(2)
                        
                        with left_col:
                            st.write(f"**Project ID:** {proposal['proposal_id']}")
                            st.write(f"**Project Name:** {proposal['project_name']}")
                            st.write(f"**Mentor:** {proposal['mentor']}")
                            st.write(f"**Objective:** {proposal['objective']}")
                            if st.session_state.get('objective_image_up') is not None:
                                st.image(st.session_state['objective_image_up'], caption="Objective Image", use_column_width=True)
                            else:
                                st.write("No objective image uploaded.")
                            st.write(f"**Rationale:** {proposal['rationale']}")
                            st.write(f"**Dataset:** {proposal['dataset']}")
                            if st.session_state.get('dataset_image_up') is not None:
                                st.image(st.session_state['dataset_image_up'], caption="Dataset Image", use_column_width=True)
                            else:
                                st.write("No dataset image uploaded.")
            
                            st.write(f"**Timeline:** {proposal['timeline']}")
                            st.write(f"**Contributors:** {proposal['contributors']}")
                            

                        with right_col:
                            st.write(f"**Semester:** {proposal['semester']}")
                            st.write(f"**Expected Students:** {proposal['expected_students']}")
                            st.write(f"**Mentor Email:** {proposal['mentor_email']}")
                            st.write(f"**Approach:** {proposal['approach']}")
                            st.write(f"**Possible Issues:** {proposal['possible_issues']}")
                            if st.session_state.get('possible_issues_image_up') is not None:
                                st.image(st.session_state['possible_issues_image_up'], caption="Possible Issues Image", use_column_width=True)
                            else:
                                st.write("No Possible Issues Image uploaded.")
            
                            st.write(f"**GitHub Link:** {proposal['github_link']}")
                            st.write(f"**Year:** {proposal['year']}")
                        
                        if st.button("Edit", key=f"edit_{index}"):
                            st.session_state['editing_index'] = index
                            st.session_state['show_edit_form'] = True
                            break  # Exit the loop to only process one form at a time

            # Check if we should display the editing form
            if st.session_state.get('show_edit_form', False):
                # Obtain the index of the proposal being edited
                index = st.session_state['editing_index']
                row = df_edit.loc[index]

                with st.form(key='edit_proposal_form'):                
                        st.subheader("Edit Proposal Request Form")
                        left_col, right_col = st.columns(2)

                        with left_col:
                            proposal_id = df_edit.loc[index,"proposal_id"]
                            name = st.text_input("Name",value=df_edit.loc[index,"name"])
                            project_name = st.text_input("Project Name",value=df_edit.loc[index,"project_name"])
                            mentor = st.text_input("Mentor for the project",value=df_edit.loc[index,"mentor"])
                            github_link = st.text_input("Github Link",value=df_edit.loc[index,"github_link"])
                            objective = st.text_area("Objective",value=df_edit.loc[index,"objective"])
                            rationale = st.text_area("Rationale",value=df_edit.loc[index,"rationale"])
                            timeline = st.text_area("Timeline",value=df_edit.loc[index,"timeline"])
                            contributors = st.text_input("Contributors",value=df_edit.loc[index,"contributors"])
                            status = df_edit.loc[index,"status"]

                        with right_col:
                            semester = st.selectbox("Semester", options=["Spring", "Summer", "Fall"])
                            expected_students = st.number_input("Expected number of students",value=df_edit.loc[index,"expected_students"])
                            mentor_email = st.text_input("Mentor email",value=df_edit.loc[index,"mentor_email"])
                            dataset = st.text_area("Dataset",value=df_edit.loc[index,"dataset"])
                            approach = st.text_area("Approach",value=df_edit.loc[index,"approach"])
                            possible_issues = st.text_area("Possible Issues",value=df_edit.loc[index,"possible_issues"])
                            year = st.selectbox("Year", options=["2021", "2022", "2023", "2024"])

                        submitted = st.form_submit_button("Submit")
                        if submitted:
                            proposal_data_edit = {
                                "name": name,
                                "project_name": project_name,
                                "mentor": mentor,
                                "github_link": github_link,
                                "objective": objective,
                                "rationale": rationale,
                                "timeline": timeline,
                                "contributors": contributors,
                                "semester": semester,
                                "expected_students": expected_students,
                                "mentor_email": mentor_email,
                                "dataset": dataset,
                                "approach": approach,
                                "possible_issues": possible_issues,
                                "year": year,
                                "proposal_id": proposal_id,
                                "status" : status
                            }
                            # Updating the appropriate proposal in the session state
                            st.session_state.to_edit_proposal[index] = proposal_data_edit
                            # Reset flags to hide the form
                            st.session_state['show_edit_form'] = False
                            st.session_state['editing_index'] = None

                            # moving the updated proposal back to the 'proposals' list
                            updated_proposal = st.session_state.to_edit_proposal.pop(index)
                            st.session_state.proposals.append(updated_proposal)

                            # Rerun the app to refresh the state and UI
                            st.rerun() 

        else:
            st.write("No matching proposal found for the entered ID.")


def show_to_edit_completion(session):
    """
    Displays proposals for editing based on a user-specified proposal ID and provides a form for editing.

    This function first prompts the user to enter a proposal ID. If a valid ID is entered and it matches an entry in the session,
    the corresponding proposal is displayed in an expander with the option to edit its details.
    If the user opts to edit the proposal, a detailed form is displayed allowing the user to update the proposal's information.

    Parameters:
    - session (list of dicts): A list containing dictionaries with each dictionary representing a proposal. It is assumed
      that each dictionary includes at least a 'proposal_id' and other relevant details.

    The function modifies the Streamlit session state based on user interactions (e.g., editing a proposal) and does not return a value.
    """
    proposal_id_to_edit = st.text_input("Enter the Proposal ID to edit:")
    df_edit = pd.DataFrame(session)
    st.write(df_edit)
    if proposal_id_to_edit:

        # Check if the entered ID matches any proposal ID
        # st.write(df_edit[df_edit['proposal_id'] == proposal_id_to_edit])
        matching_proposals = df_edit[df_edit['proposal_id'] == proposal_id_to_edit]

        if not matching_proposals.empty:
            for index, proposal in df_edit.iterrows():
                with st.expander(f"Proposal {index + 1}: {proposal['project_name']}"):
                    # Define columns here, inside each expander's context
                    st.write(f"**project title:** {proposal['project_name']}")
                    st.write(f"**Video Link** {proposal['video_link']}")
                    st.write(f"**github repo:** {proposal['github_link']}")
                    st.write(f"**project website:** {proposal['project_website']}")
                    st.write(f"**Year:** {proposal['year']}")
                    st.write(f"**Semester:** {proposal['semester']}")
                    st.write(f"**Submitted by:** {proposal['name']}")

                    if st.button("Edit", key=f"edit_{index}"):
                        st.session_state['editing_index'] = index
                        st.session_state['show_edit_form'] = True
                        break  # Exit the loop to only process one form at a time
            # Check if we should display the editing form
            if st.session_state.get('show_edit_form', False):
                # Obtain the index of the proposal being edited
                index = st.session_state['editing_index']
                row = df_edit.loc[index]

                with st.form(key='edit_proposal_form'):
                        st.subheader("Edit Completion Form")
                        project_title = st.text_input("Name",value=df_edit.loc[index,"project_name"])
                        video_link = st.text_input("Video Link",value=df_edit.loc[index,"video_link"])
                        github_link = st.text_input("github repo",value=df_edit.loc[index,"github_link"])
                        website = st.text_input("project website",value=df_edit.loc[index,"project_website"])
                        year = st.text_input("year",value=df_edit.loc[index,"year"])
                        semester = st.text_input("semester",value=df_edit.loc[index,"semester"])
                        name = st.text_input("Proposed by",value=df_edit.loc[index,"name"])
                        # Word document upload field
                        document = st.file_uploader("Upload your project document", type=['docx'])

                        submitted = st.form_submit_button("Submit")
                        
                        if submitted:
                            completion_id = proposal_id_to_edit
                            save_uploaded_file(document)
                            data_edit = {
                                "project_name": project_title,
                                "video_link": video_link,
                                "github_link": github_link,
                                "project_website": website,
                                "project_document": document.name if document is not None else "File not uploaded",
                                "year": year,
                                "semester": semester,
                                "name": name,
                                "completion_id": completion_id,
                                "mentor": df_edit.loc[index,"mentor"],
                                "objective": df_edit.loc[index,"objective"],
                                "objective_image_name":df_edit.loc[index,"objective_image_name"],
                                "rationale":df_edit.loc[index,"rationale"],
                                "timeline":df_edit.loc[index,"timeline"],
                                "contributors":df_edit.loc[index,"contributors"],
                                "expected_students":df_edit.loc[index,"expected_students"],
                                "mentor_email": df_edit.loc[index,"mentor_email"],
                                "dataset": df_edit.loc[index,"dataset"],
                                "dataset_image_name": df_edit.loc[index,"dataset_image_name"] if df_edit.loc[index,"dataset_image_name"] is not None else "Not uploaded",
                                "approach": df_edit.loc[index,"approach"],
                                "possible_issues_image_name":df_edit.loc[index,"possible_issues_image_name"] if df_edit.loc[index,"possible_issues_image_name"] is not None else "Not uploaded",
                                "proposal_id":df_edit.loc[index,"proposal_id"],
                                "proposed_by_professor": df_edit.loc[index,"proposed_by_professor"],
                                "status":df_edit.loc[index,"status"],
                                "possible_issues" : df_edit.loc[index,"possible_issues"]
                            }
                            # Updating the appropriate proposal in the session state
                            st.session_state.edit_completion[index] = data_edit
                            # Reset flags to hide the form
                            st.session_state['show_edit_form'] = False
                            st.session_state['editing_index'] = None

                            # moving the updated proposal back to the 'proposals' list
                            updated_proposal = st.session_state.edit_completion.pop(index)
                            st.session_state.completion.append(updated_proposal)
                            st.info(f"Note your new Project Completion id is {completion_id}")

                            # Rerun the app to refresh the state and UI
                            st.rerun()


def save_uploaded_images(objective_file, dataset_file, possible_issues_file):
    """
    Saves uploaded images for objective, dataset, and possible issues to the session state.

    This function checks if any files have been uploaded for objective, dataset, or possible issues and,
    if so, saves the image data to the session state. It allows these images to be displayed later in the application.

    Parameters:
    - objective_file (UploadedFile): The file uploaded for the objective image.
    - dataset_file (UploadedFile): The file uploaded for the dataset image.
    - possible_issues_file (UploadedFile): The file uploaded for the possible issues image.

    There are no return values for this function.
    """
    if objective_file is not None:
        st.session_state.objective_image_up = objective_file.getvalue()
    if dataset_file is not None:
        st.session_state.dataset_image_up = dataset_file.getvalue()
    if possible_issues_file is not None:
        st.session_state.possible_issues_image_up = possible_issues_file.getvalue()



def get_image_display_code(image_data):
    """
    Converts an image data to a Markdown compatible base64 image format for display.

    This function takes an image data object, converts it to a base64-encoded string, and
    returns the Markdown string to display the image inline in the application.

    Parameters:
    - image_data (Image): An image object to be converted to base64.

    Returns:
    - str: A string containing the Markdown code to display the image inline.
    """
    base64_img = pil_image_to_base64(image_data)
    return f"![image](data:image/png;base64,{base64_img})"

def save_uploaded_file(uploaded_file):
    """
    Saves an uploaded Word document to the session state.

    This function reads the contents of an uploaded file into a bytes object, stores it in the session state,
    and sets the file name in the session state. It notifies the user of successful upload.

    Parameters:
    - uploaded_file (UploadedFile): The Word document file uploaded by the user.

    There are no return values for this function.
    """
    if uploaded_file is not None:
        # Read the file data into a bytes object
        bytes_data = uploaded_file.read()
        # Save the bytes data in the session state
        st.session_state['uploaded_word_doc'] = bytes_data
        st.session_state['uploaded_word_doc_name'] = uploaded_file.name
        st.success(f"Uploaded {uploaded_file.name} successfully.")



def check_action_and_prompt_password():
    """
    Checks the requested action type and index from the session state, prompts for a password, 
    and executes the action if the password is correct.

    This function retrieves the action type and index from the session state. If these are set, it displays a password input field.
    If the user enters the correct password ('root'), it executes the corresponding action (approve, reject, edit, or delete a proposal).
    Upon successful action execution, it clears the relevant session state entries and displays a success message.
    If the password is incorrect, it displays an error message.

    There are no parameters and no return values. This function modifies the session state and the UI based on the action and password validation.
    """
    action_type = st.session_state.get('action_type')
    action_index = st.session_state.get('action_index')

    if action_type and action_index is not None:
        password = st.text_input("Enter password to proceed with the action:", type="password")

        if password:  # Assuming the password input is not empty
            if password == PASSWORD: 
                if action_type == 'approve':
                    approve_proposal(action_index)
                elif action_type == 'reject':
                    reject_proposal(action_index)
                elif action_type == 'edit':
                    edit_proposal(action_index)
                elif action_type == 'delete':
                    delete_prof_proposal(action_index)

                # Clear action_type and action_index after the action is performed
                del st.session_state['action_type']
                del st.session_state['action_index']
                st.success("Action performed successfully.")
            else:
                st.error("Incorrect password.")

def download_proposal(proposal):
    """
    Provides a link for downloading proposal data in CSV format.

    This function takes a proposal data, converts it to a CSV format, and encodes it in base64.
    It then creates a hyperlink which, when clicked, will download the data as a CSV file.

    Parameters:
    - proposal (DataFrame): A DataFrame containing the proposal data to be downloaded.

    There are no return values for this function.
    """
    # Convert proposal details to CSV
    csv = proposal.to_csv(index=False)
    # Convert CSV string to bytes
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="proposal.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

def delete_approved_proposal(index):
    """
    Deletes an approved proposal from the session state based on its index and reruns the Streamlit application to update the UI.

    Parameters:
    - index (int): The index of the approved proposal in the 'approved' list to be deleted.

    There are no return values for this function, but it triggers a UI update by rerunning the Streamlit application.
    """
    # Remove proposal from session state
    del st.session_state['approved'][index]
    # Update the display
    st.rerun()

def generate_markdown_file(markdown_content):
    """
    Creates a downloadable file containing the given markdown content.

    This function generates a BytesIO object from a given markdown string, making it ready for download through a Streamlit interface.

    Parameters:
    - markdown_content (str): The markdown content to be written into a file.

    Returns:
    - BytesIO: A BytesIO object containing the encoded markdown content.
    """
    bytes_io = BytesIO()
    bytes_io.write(markdown_content.encode('utf-8'))
    bytes_io.seek(0)  # move to the start of the BytesIO object
    return bytes_io

def display_section(df, section_name, section_key):
    st.header(section_name)

    if df.empty:
        st.write("No Proposals to show in this section.")
        return

    for index, row in df.iterrows():
        proposal_markdown = format_proposal_as_markdown(row.to_dict())
        markdown_file = generate_markdown_file(proposal_markdown)

        with st.expander(f"{row['project_name']} (Details)"):
            st.markdown(proposal_markdown, unsafe_allow_html=True)
            download_button_key = f"download_{section_name}_{index}"
            delete_button_key = f"delete_{section_name}_{index}"
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(label="Download",
                                   data=markdown_file,
                                   file_name=f"{row['project_name'].replace(' ', '_')}_proposal.md",
                                   mime="text/markdown",
                                   key=download_button_key)

            with col2:
                if st.button("Delete", key=delete_button_key):
                    # Store pending deletion details in session state
                    st.session_state.pending_deletion = {"index": index, "section_key": section_key}
                    # Prompt for password
                    password_prompt()




def password_prompt():
    """
    Displays a password input to confirm a deletion action, only if there's a pending deletion in the session state.

    This function checks if there is a pending deletion action (indicated by 'pending_deletion' in the session state).
    If such an action exists, it presents a password field for the user to enter a password. If the password is entered,
    it calls `handle_delete_action` to process the deletion.

    There are no parameters and no return values. This function modifies the session state based on user input.
    """
    # Only show the password prompt if there's a pending deletion
    if 'pending_deletion' in st.session_state:
        with st.container():
            password = st.text_input("Enter password to confirm deletion:", type="password", key="delete_password")

            if password:
                # Verify password and handle deletion if correct
                handle_delete_action()

def handle_delete_action():
    """
    Processes the deletion of an item from a list in the session state based on user authentication.

    This function checks the session state for a correct password and pending deletion details.
    If the password matches and the item index and section are valid, it deletes the item from the appropriate list.
    It provides feedback on the success or failure of the deletion and clears the deletion-related session state.

    There are no parameters and no return values. This function modifies the session state and updates the UI accordingly.
    """
    if 'pending_deletion' in st.session_state and 'delete_password' in st.session_state:
        correct_password = PASSWORD # password from env variable
        if st.session_state.delete_password == correct_password:
            # Retrieve the index and section key from session state
            index = st.session_state.pending_deletion["index"]
            section_key = st.session_state.pending_deletion["section_key"]
            
            if section_key in st.session_state and len(st.session_state[section_key]) > index:
                # Perform deletion
                del st.session_state[section_key][index]
                st.success("Deletion successful.")
            else:
                st.error("Deletion failed. Item not found.")
            
            # Clear session state related to deletion
            del st.session_state['pending_deletion']
            del st.session_state['delete_password']
            st.experimental_rerun()
        else:
            st.error("Incorrect password.")


def show_all(filtered_approved, filtered_rejected, filtered_edit_prop, filtered_completed, filtered_edit_completion):
    """
    Displays multiple sections of proposals, each with specific filters applied.

    This function iterates over a list of tuples that define sections of data (like approved projects or rejected proposals).
    Each section is displayed with its respective DataFrame. If there is a pending deletion action, it also handles it.

    Parameters:
    - filtered_approved (DataFrame): Filtered DataFrame for approved projects.
    - filtered_rejected (DataFrame): Filtered DataFrame for rejected proposals.
    - filtered_edit_prop (DataFrame): Filtered DataFrame for proposals to be edited.
    - filtered_completed (DataFrame): Filtered DataFrame for completed projects.
    - filtered_edit_completion (DataFrame): Filtered DataFrame for completion requiring edits.

    There are no return values. This function updates the UI and may modify the session state based on user interactions.
    """
    # Display Sections with Filtered DataFrames
    sections = [
        ("Approved Projects", "approved", filtered_approved),
        ("Rejected Proposals", "rejected", filtered_rejected),
        ("Proposals to be Edited", "to_edit_proposal", filtered_edit_prop),
        ("Completed Projects", "approved_completion", filtered_completed),
        ("Completion Requiring Edits", "edit_completion", filtered_edit_completion),
    ]

    for section_name, section_key, df in sections:
        display_section(df, section_name, section_key)

    # Handle global deletion action
    if 'pending_deletion' in st.session_state and st.session_state.pending_deletion:
        handle_delete_action()
    
