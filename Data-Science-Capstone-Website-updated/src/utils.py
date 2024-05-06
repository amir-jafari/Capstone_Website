from PIL import Image
import io
import base64
import streamlit as st
import subprocess
import os
import shutil
import uuid
import requests

# local_dir = r"D:/Capstone Website - streamlit_dup/Data-Science-Capstone-Website/github clones"
# target_repo_url = "https://github.com/Renga-99/Data-Science-Capstone-Website.git"

def pil_image_to_base64(image):
    """
    Converts a PIL image to a base64-encoded JPEG string suitable for embedding in HTML or Markdown.

    Parameters:
    - image (PIL.Image): The PIL Image object to convert.

    Returns:
    - str: A string containing the base64-encoded JPEG image, prefixed with the appropriate HTML src attribute.
    """
    img_buffer = io.BytesIO()
    image.save(img_buffer, format="JPEG")  # change 'JPEG' to 'PNG' if needed
    base64_img = base64.b64encode(img_buffer.getvalue()).decode()
    return f"data:image/jpeg;base64,{base64_img}"

def resize_image(image, width=300):
    """
    Resizes a PIL image to a specified width while maintaining the aspect ratio.

    Parameters:
    - image (PIL.Image): The PIL Image object to resize.
    - width (int): The target width to resize the image to.

    Returns:
    - PIL.Image: A new PIL Image object resized to the specified width.
    """
    
    # Calculate the target height to maintain the aspect ratio
    aspect_ratio = image.height / image.width
    target_height = int(aspect_ratio * width)
    return image.resize((width, target_height))

def handle_image_markdown(image_data):
    """
    Handles the conversion of an image from the session state to a Markdown embeddable image string.

    Parameters:
    - image_data (bytes): Raw image data from the session state.

    Returns:
    - str: A Markdown string with the embedded base64 image or a placeholder text if no image is provided.
    """
    if image_data is not None:
        image_bytes_io = io.BytesIO(image_data)
        image_obj = Image.open(image_bytes_io)
        resized_image = resize_image(image_obj)
        base64_image = pil_image_to_base64(resized_image)
        return f"![Uploaded Image]({base64_image})"
    else:
        return "No image uploaded"

def format_proposal_as_markdown(proposal):
    """
    Generates a Markdown representation of a project proposal including embedded images.

    This function formats a proposal dictionary into a Markdown string, embedding images for the objective, dataset,
    and possible issues if they exist in the session state. Images are resized, converted to base64, and inserted directly
    into the Markdown.

    Parameters:
    - proposal (dict): A dictionary containing all the necessary data to format the proposal.

    Returns:
    - str: A string containing the formatted proposal in Markdown format.
    """

    # Handling Objective Image
    image_markdown_obj = handle_image_markdown(st.session_state.get('objective_image_up'))
    
    # Handling Dataset Image
    image_markdown_data = handle_image_markdown(st.session_state.get('dataset_image_up'))
    
    # Handling Possible Issues Image
    image_markdown_issue = handle_image_markdown(st.session_state.get('possible_issues_image_up'))

    # Embed the Base64 image string in the Markdown template
    markdown_template = f"""
# Capstone Proposal
## {proposal["project_name"]}
### Proposed by: {proposal["name"]}
#### Mentor Email: {proposal["mentor_email"]}
#### Advisor: {proposal["mentor"]}
#### George Washington University  
#### Data Science Program

## 1. Objective:
{proposal["objective"]}


{image_markdown_obj}
## 2. Dataset:
{proposal["dataset"]}


{image_markdown_data}
## 3. Rationale:
{proposal["rationale"]}

## 4. Approach:
{proposal["approach"]}

## 5. Timeline:
{proposal["timeline"]}

## 6. Expected Number of Students:
{proposal["expected_students"]}

## 7. Possible Issues:
{proposal["possible_issues"]}

{image_markdown_issue}

## Contact
- Author: {proposal["name"]}
- Email: [{proposal["mentor_email"]}](mailto:{proposal["mentor_email"]})
- GitHub: [{proposal["github_link"]}]
"""
    

    return markdown_template

def format_completion_as_markdown(completion):
    """
    Generates a Markdown representation of a project completion document.

    This function formats the completion details of a capstone project into a Markdown string. The details include
    the project title, video link, GitHub link, project website, and the name of the uploaded document.

    Parameters:
    - completion (dict): A dictionary containing all the necessary data to format the completion document.

    Returns:
    - str: A string containing the formatted completion document in Markdown format.
    """

    markdown_template = f"""
# George Washington University  
## Data Science Program
### Capstone Final Completion
#### Project Title: {completion["project_name"]}
#### Video Link: {completion["video_link"]}
#### Github Link: {completion["github_link"]}
#### Project Website: {completion["project_website"]}  
#### Document uploaded name: {completion["project_document"]}


"""
    return markdown_template

def archive_source_repo_into_target(source_repo_url, target_repo_url, local_clone_path, archive_dir_name="Archive"):
    """
    Archives the contents of a source Git repository into a target Git repository under a specified directory.

    This function clones the source and target repositories locally, copies all files from the source repository
    (except the .git directory) into a specified archive directory in the target repository, and pushes the changes
    back to the target repository.

    Parameters:
    - source_repo_url (str): URL of the source Git repository.
    - target_repo_url (str): URL of the target Git repository.
    - local_clone_path (str): Path where the local clones will be stored.
    - archive_dir_name (str, optional): Name of the directory in the target repository where files will be archived.

    There are no return values. This function performs file operations and Git commands.
    """
    # Define paths for the local clones
    source_repo_dir = os.path.join(local_clone_path, "source_repo")
    target_repo_dir = os.path.join(local_clone_path, "target_repo")

    # Clone the source repository
    subprocess.run(["git", "clone", source_repo_url, source_repo_dir], check=True)

    # Clone the target repository if it hasn't been cloned already
    if not os.path.exists(target_repo_dir):
        subprocess.run(["git", "clone", target_repo_url, target_repo_dir], check=True)

    # Create the Archive directory in the target repo if it doesn't exist
    archive_path = os.path.join(target_repo_dir, archive_dir_name)
    os.makedirs(archive_path, exist_ok=True)

    # Copy the contents from the source repo to the Archive directory in the target repo
    for item in os.listdir(source_repo_dir):
        if item != ".git":  # Ignore the .git directory
            src_path = os.path.join(source_repo_dir, item)
            dst_path = os.path.join(archive_path, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)

    # Change to the target repo directory for Git operations
    os.chdir(target_repo_dir)
    
    # Git add, commit, and push changes
    subprocess.run(["git", "add", "."], check=True)
    commit_message = "Archived content from source repository"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)

    # Clean up: remove the local clone of the source repository
    shutil.rmtree(source_repo_dir, ignore_errors=True)

def generate_unique_id():
    """
    Generates a unique identifier using UUID4.

    Returns:
    - str: A unique identifier in string format.
    """
    # Generate a random UUID
    unique_id = uuid.uuid4()
    return str(unique_id)

def is_github_repo_valid(github_link):
    """
    Checks if the provided GitHub repository link is valid by making an API request.

    This function verifies a GitHub repository URL by using GitHub's API to fetch the repository data. It checks
    if the response status is 200, indicating that the repository exists and is accessible.

    Parameters:
    - github_link (str): The GitHub URL to be validated.

    Returns:
    - bool: True if the repository is valid, False otherwise.
    """
    if not github_link.startswith("https://github.com/"):
        return False
    parts = github_link.split("/")
    if len(parts) < 5:
        return False
    repo_owner, repo_name = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    response = requests.get(api_url)
    return response.status_code == 200