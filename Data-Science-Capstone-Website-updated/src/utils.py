from PIL import Image
import io
import base64
import streamlit as st
import subprocess
import os
import shutil
import uuid
import requests
import tarfile
from google.cloud import storage
import stat


# local_dir = r"D:/Capstone Website - streamlit_dup/Data-Science-Capstone-Website/github clones"
# target_repo_url = "https://github.com/Renga-99/Data-Science-Capstone-Website.git"

def convert_image_to_binary(file_uploader):
    if file_uploader is not None:
        # Read the file uploaded in Streamlit
        bytes_data = file_uploader.getvalue()
        return bytes_data
    else:
        return None
def pil_image_to_base64(image):
    """Converts a PIL image to a base64 string for embedding in Markdown."""
    img_buffer = io.BytesIO()
    image.save(img_buffer, format="JPEG")
    base64_img = base64.b64encode(img_buffer.getvalue()).decode()
    return f"data:image/jpeg;base64,{base64_img}"

def resize_image(image, width=300):
    """Resizes the image to a specified width while maintaining aspect ratio."""
    aspect_ratio = image.height / image.width
    target_height = int(aspect_ratio * width)
    return image.resize((width, target_height))

def handle_image_markdown(blob_data):
    """Converts BLOB data to a Markdown-compatible image tag."""
    if blob_data is None:
        return "Not uploaded"
    else:
        image_bytes_io = io.BytesIO(blob_data)
        image = Image.open(image_bytes_io)
        resized_image = resize_image(image)
        base64_image = pil_image_to_base64(resized_image)
        return f"![Uploaded Image]({base64_image})"


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
    
    # Convert binary data to bytes, then to an Image
    
    objective_image = handle_image_markdown(proposal["objective_image"])
    dataset_image = handle_image_markdown(proposal["dataset_image"])
    possible_issues_image = handle_image_markdown(proposal["possible_issues_image"])


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

{objective_image}

## 2. Dataset:
{proposal["dataset"]}

{dataset_image}

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

{possible_issues_image}

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


def clone_repo(git_url, destination_path):
    """Clone the given repository URL into a specified directory."""
    os.makedirs(destination_path, exist_ok=True)
    try:
        subprocess.run(['git', 'clone', git_url, destination_path], check=True, capture_output=True, text=True)
        print("Repository cloned successfully into:", destination_path)
    except subprocess.CalledProcessError as e:
        print("Failed to clone repository:", e.stderr)
        raise RuntimeError(f"Git clone failed: {e.stderr}")

def make_files_writable(directory):
    """Recursively make all files in the directory writable."""
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            os.chmod(file_path, stat.S_IWRITE)

def compress_directory(source_dir, output_file, include_extensions=None, include_files=None):
    """Compress selected files from a directory into a tar.gz archive."""
    with tarfile.open(output_file, 'w:gz') as tar:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith(tuple(include_extensions)) or file in include_files:
                    file_path = os.path.join(root, file)
                    tar.add(file_path, arcname=os.path.relpath(file_path, start=source_dir))

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Upload a file to Google Cloud Storage."""
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def process_student_data(student_data):
    """Process data for a single student to clone their repo, archive it, and upload to GCS."""
    student_name = student_data['name']
    repo_url = student_data['repo_url']
    bucket_name = 'projects-capstone'
    local_repo_dir = os.path.join('./temp', student_name)  # Local directory for the repo
    compressed_file_path = os.path.join('./temp', f"{student_name}.tar.gz")

    try:
        clone_repo(repo_url, local_repo_dir)
        compress_directory(local_repo_dir, compressed_file_path, include_extensions=['.py', '.ipynb'], include_files=['README.md'])
        gcs_blob_name = f"projects/{student_data['semester']}/{student_name}/repo.tar.gz"
        upload_to_gcs(bucket_name, compressed_file_path, gcs_blob_name)
    finally:
        # Make files writable before deletion
        make_files_writable(local_repo_dir)
        shutil.rmtree(local_repo_dir, ignore_errors=True)
        if os.path.exists(compressed_file_path):
            os.remove(compressed_file_path)
        # Optionally, remove the entire temp directory
        if os.path.exists('./temp'):
            make_files_writable('./temp')
            shutil.rmtree('./temp', ignore_errors=True)
        print(f"Cleaned up {local_repo_dir} and {compressed_file_path}")

