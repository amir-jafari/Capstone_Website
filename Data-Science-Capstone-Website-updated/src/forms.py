import streamlit as st
from data_management import save_uploaded_images, submit_proposal, submit_completion, save_uploaded_file, submit_prof_proposal,fetch_project_details
from utils import format_proposal_as_markdown,generate_unique_id, is_github_repo_valid, convert_image_to_binary,process_student_data
import pandas as pd
def initialize_placeholder_data():
    # Placeholder proposal data structure
    placeholder_data = {
        'project_name': 'Project 1',
        'year': 2023,
        'semester': 'Spring',
        'name': 'Renga',
        'mentor': 'Edwin Lo',
        'github_link': 'https://github.com/example',
        'objective': 'Convert Neural Network Design Demos from Pyqt to Streamlit App...',
        'objective_image': None,  
        'rationale': 'This project will help students...',
        'timeline': '1 Week: Streamlit environment setup...',
        'contributors': 'Student 1, Student 2',
        'status': 'Approved.. In Progress',  
        'proposal_id': generate_unique_id(),  
        'semester': "Spring",
        'expected_students': 1,
        'mentor_email': "abc@gmail.com",
        'dataset': "No dataset required",
        'dataset_image_name' : None,
        'approach': """I plan on approaching this capstone through several steps.  
                                                        1. Familiarize yourself with Streamlit environment.
                                                        2. Design the web layout with 2 books and all the chapters.  
                                                        3. Create a modular widgets can be used across all the chapters (Reusable).
                                                        4. Create a documentation from the begging till the end of the product.
                                                        5. After all demos is done, testing it in local machine.
                                                        6. Create the container that can be used in deployment.
                                                        7. Deploy it on a server that can be accessed over the internet. """,
        'possible_issues': " The challenge is on creating modular widgets and create a same layout as the book. Also, web deployment and containerizing it is also another challenge. ",
        'possible_issues_image_name': None,
        'year': '2021',
    
        'proposed_by_professor': False,
      
    }

    # List of session states to initialize if they're not already present
    session_states = ['approved', 'rejected', 'to_edit_proposal', 'prof_proposal'] #, 'completion', 'edit_completion', 'approved_completion']

    for state in session_states:
        if state not in st.session_state or not st.session_state[state]:
            st.session_state[state] = [placeholder_data]


def proposal_request_form():
    """
    Displays a form for users to submit or preview a new project proposal.

    This form collects comprehensive details about a project proposal, including images and text inputs. Users can preview their
    input before submission or directly submit it. Images uploaded are saved to the session state, and the proposal data is either
    submitted as a professional proposal or a regular proposal based on a checkbox selection.

    There are no parameters and no return values. This function interacts with the global `st.session_state` and can modify it based on user actions.
    """
    with st.form("proposal_form"):
        st.subheader("Proposal Request Form")
        left_col, right_col = st.columns(2)
        
        with left_col:
            name = st.text_input("Name", value="Renga")
            project_name = st.text_input("Project Name",value="Project 1")
            mentor = st.text_input("Mentor for the project",value="Edwin Lo")
            github_link = st.text_input("Github Link", value="abc.com")
            objective = st.text_area("Objective",value="""The goal of this project is to convert all the Neural Network Design Demos from Pyqt to streamlit App. 
                                                        Currently all the demos are in pyqt environment and can be installed by pip (https://pypi.org/project/nndesigndemos/).
                                                        In the project, you job is is converting All the current demos which is written in python and uses pyqt widgets to 
                                                        Streamlit webapp. And then create a container that can be deployed in the web domain. The final product is using the 
                                                        demos by providing a user a link that opens up a webpage and all the demos will be accessed through internet.""")
            objective_image = st.file_uploader("Upload an image for objective if needed", type=["jpg", "jpeg", "png"],key="objective_image")
            
            objective_image_binary = convert_image_to_binary(objective_image)
    
            

            rationale = st.text_area("Rationale",value="""This project is going to help students to use the Neural Network book demos in web format and it would easier for students 
                                                        to access them. This is project is educational case that helps Neural Network Community to understand Neural Network
                                                        in more conceptual way.""")
            timeline = st.text_area("Timeline",value= """This a rough time line for this project:  
                                                        - (1 Weeks) Streamlit environment.  
                                                        - (2 Weeks) Web layout  
                                                        - (1 Weeks) Modular widgets  
                                                        - (4 Weeks) Convert all the demos 
                                                        - (2 Weeks) Container  
                                                        - (2 Weeks) Web Deployment
                                                        - (2 Weeks) Documentation""")
            contributors = st.text_input("Contributors",value="Student 1, Student 2")
            proposal_id = generate_unique_id()

        with right_col:
            semester = st.selectbox("Semester", options=["Spring", "Summer", "Fall"])
            expected_students = st.number_input("Expected number of students", min_value=1, value=1)
            mentor_email = st.text_input("Mentor email",value="abc@gmail.com")
            dataset = st.text_area("Dataset",value="No dataset required")
            dataset_image = st.file_uploader("Upload an image for dataset", type=["jpg", "jpeg", "png"], key="dataset_image")
            dataset_image_binary = convert_image_to_binary(dataset_image)

            approach = st.text_area("Approach",value="""I plan on approaching this capstone through several steps.  
                                                        1. Familiarize yourself with Streamlit environment.
                                                        2. Design the web layout with 2 books and all the chapters.  
                                                        3. Create a modular widgets can be used across all the chapters (Reusable).
                                                        4. Create a documentation from the begging till the end of the product.
                                                        5. After all demos is done, testing it in local machine.
                                                        6. Create the container that can be used in deployment.
                                                        7. Deploy it on a server that can be accessed over the internet. """)
            possible_issues = st.text_area("Possible Issues",value=" The challenge is on creating modular widgets and create a same layout as the book. Also, web deployment and containerizing it is also another challenge. ")
            possible_issues_image = st.file_uploader("Upload an image for possible issues", type=["jpg", "jpeg", "png"],key="possible_issues_image")
            possible_issues_image_binary = convert_image_to_binary(possible_issues_image)
  
 
            year = st.selectbox("Year", options=["2021", "2022", "2023", "2024"])
            proposed_by_professor = st.checkbox("Proposed by a Professor")
        
       


        preview = st.form_submit_button("Preview")
        submitted = st.form_submit_button("Submit")

        if submitted:
            # save_uploaded_images(objective_image,dataset_image,possible_issues_image)
            proposal_data = {
                "name": name,
                "project_name": project_name,
                "mentor": mentor,
                "github_link": github_link,
                "objective": objective,
                "objective_image" : objective_image_binary ,
                "rationale": rationale,
                "timeline": timeline,
                "contributors": contributors,
                "semester": semester,
                "expected_students": expected_students,
                "mentor_email": mentor_email,
                "dataset": dataset,
                "dataset_image" : dataset_image_binary,
                "approach": approach,
                "possible_issues": possible_issues,
                "possible_issues_image": possible_issues_image_binary,
                "year": year,
                "proposal_id": proposal_id,
                "proposed_by_professor":proposed_by_professor,
                "status" : "Pending Approval"
                
            }
            # proposal_data = pd.DataFrame.from_dict(proposal_data, orient = "index")
            if proposed_by_professor == True:
                submit_prof_proposal(proposal_data)
            else:
                submit_proposal(proposal_data)
            st.info(f' Proposal ID: {proposal_id}. This is an info alert! Make sure to note down your proposal ID number!')

      
        if preview:
            # if objective_image is not None:
            #     st.session_state.objective_image_up = objective_image.getvalue()
            #     objective_image_name = objective_image.name
            # # No else part needed since default value is already set

            # if dataset_image is not None:
            #     st.session_state.dataset_image_up = dataset_image.getvalue()
            #     dataset_image_name = dataset_image.name
            # # No else part needed since default value is already set

            # if possible_issues_image is not None:
            #     st.session_state.possible_issues_image_up = possible_issues_image.getvalue()
            #     possible_issues_image_name = possible_issues_image.name
            # # No else part needed since default value is already set
        
            preview_data = {
                "name": name,
                "project_name": project_name,
                "mentor": mentor,
                "github_link": github_link,
                "objective": objective,
                "objective_image" : objective_image_binary,
                "rationale": rationale,
                "timeline": timeline,
                "contributors": contributors,
                "semester": semester,
                "expected_students": expected_students,
                "mentor_email": mentor_email,
                "dataset": dataset,
                "dataset_image" : dataset_image_binary,
                "approach": approach,
                "possible_issues": possible_issues,
                "possible_issues_image": possible_issues_image_binary ,
                "year": year,
                "proposal_id": proposal_id,
                "proposed_by_professor" : proposed_by_professor,
                "status": "Pending Approval"

            }
        
            st.markdown(format_proposal_as_markdown(preview_data), unsafe_allow_html=True)




def completion_form():
    """
    Displays a form for users to submit completion details of an approved project proposal.

    This form allows users to enter a proposal ID to retrieve details of an approved project, which are then used to pre-fill
    the form fields. Users can provide additional details and documentation necessary for project completion. The form validates
    the GitHub repository link and only submits the completion if the repository is valid. On successful submission, it updates
    the session state and displays the completion ID.

    There are no parameters and no return values. This function interacts with the global `st.session_state` and can modify it based on user actions.
    """

    st.subheader("Project Completion Form")
     # Search box for proposal ID
    proposal_id_search = st.text_input("Enter Proposal ID to retrieve project details:")

    # Attempt to fetch project details if a proposal ID is given
    project_details = pd.DataFrame()
    if proposal_id_search:
        project_details = fetch_project_details(proposal_id_search)
  
    if not project_details.empty:
        st.info("Project details retrieved successfully:")
        # st.json(project_details) 
    
        with st.form(key='completion_form'):
            
            project_title = st.text_input("Project Title",value=project_details["project_name"][0])
            video_link = st.text_input("Video Link")
            github_repo = st.text_input("GitHub Repository",value=project_details["github_link"][0])
            project_website = st.text_input("Project Website Link if available")
            year = st.text_input("Year",value=project_details["year"][0])
            semester = st.text_input("semester",value=project_details["semester"][0])
            name = st.text_input("Submitted by",value=project_details["name"][0])
            # Word document upload field
            uploaded_file = st.file_uploader("Upload your project document", type=['docx'])
            proposal_id = project_details["proposal_id"][0]
            # Form submission button
            validate_button = st.form_submit_button("Validate GitHub Link")
            submit_button = st.form_submit_button(label='Submit')
            
            if validate_button:
                if is_github_repo_valid(github_repo):
                    st.success("GitHub repository is valid.")
                else:
                    st.error("Invalid GitHub repository. Please check the URL.")

            if submit_button:
                if not is_github_repo_valid(github_repo):
                    st.error("Cannot submit: Invalid GitHub repository. Please validate the URL first.")
                    return
                # Save the uploaded Word document when the form is submitted
                save_uploaded_file(uploaded_file)
                # completion_id = generate_unique_id()
                completion = {
                    "project_name" : project_title,
                    "video_link" : video_link,
                    "github_link" : github_repo,
                    "project_website": project_website,
                    "project_document" : uploaded_file.name if uploaded_file is not None else "File not uploaded",
                    "year" : year,
                    "semester": semester,
                    "name": name,
                    "proposal_id": proposal_id[0],
                    "status": "Pending Completion Approval",
                    "mentor": project_details["mentor"][0],
                    "objective": project_details["objective"][0],
                    "rationale":project_details["rationale"][0],
                    "timeline":project_details["timeline"][0],
                    "contributors":project_details["contributors"][0],
                    "expected_students":project_details["expected_students"][0],
                    "mentor_email": project_details["mentor_email"][0],
                    "possible_issues": project_details["possible_issues"][0],
                    "dataset": project_details["dataset"][0],
                    "approach": project_details["approach"][0],
                    "proposal_id":project_details["proposal_id"][0],
                    "proposed_by_professor": project_details["proposed_by_professor"][0],
                    "status":project_details["status"][0],
                    "objective_image":project_details["objective_image"][0],
                    "dataset_image":project_details["dataset_image"][0],
                    "possible_issues_image": project_details["possible_issues_image"][0]
                }
                
                submit_completion(completion)
                # Example student data
                student_data = {
                    'semester': str(semester) + " " +str(year),
                    'name': str(name),
                    'repo_url': str(github_repo)
                }
                process_student_data(student_data)
                st.info(f"Note your Project Completion id is {proposal_id}")
            
                st.rerun()
    else:
        st.info("Enter a correct proposal ID")



