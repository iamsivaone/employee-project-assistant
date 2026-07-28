import json
import requests
import streamlit as st

import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Employee Project Assistant",
    page_icon="🤖",
    layout="wide",
)

##################################################
# Load Data
##################################################

@st.cache_data(ttl=5)
def get_users():
    """Fetch users list from backend API endpoint with caching.

    Returns:
        list[dict]: List of user records from backend API.
    """
    response = requests.get(
        f"{BASE_URL}/users"
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=5)
def get_projects():
    """Fetch available projects list from backend API endpoint with caching.

    Returns:
        list[dict]: List of project records from backend API.
    """
    response = requests.get(
        f"{BASE_URL}/projects"
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=5)
def get_permissions():
    """Fetch user-project permissions list from backend API endpoint with caching.

    Returns:
        list[dict]: List of permission records from backend API.
    """
    response = requests.get(
        f"{BASE_URL}/admin/get-permissions"
    )

    response.raise_for_status()

    return response.json()


users = get_users()
projects = get_projects()
permissions = get_permissions()

##################################################
# Sidebar
##################################################

st.sidebar.title("👤 Login")

selected_user = st.sidebar.selectbox(
    "Login As",
    users,
    format_func=lambda x: x["name"],
    key="login_user",
)

role = selected_user["role"]

st.sidebar.success(role)

##################################################
# Projects
##################################################

user_projects = []
# st.sidebar.write(selected_user)
# st.sidebar.write(f"Role: {role}")
if role == "Admin":

    user_projects = projects

else:

    for permission in permissions:

        if (
            permission["user_id"] == selected_user["id"]
            and permission["access"]
        ):

            user_projects.append(
                {
                    "id": permission["project_id"],
                    "name": permission["project_name"],
                }
            )

selected_project = None

if user_projects:

    selected_project = st.sidebar.selectbox(
        "Project",
        user_projects,
        format_func=lambda x: x["name"],
    )

else:

    st.sidebar.warning("No projects assigned.")

    selected_project = None

##################################################
# Upload
##################################################

st.sidebar.divider()
if role == "Admin":
    uploaded_file = st.sidebar.file_uploader(
        "Upload",
        type=["pdf", "docx", "txt"],
    )

    if uploaded_file:

        if st.sidebar.button("Upload"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            data = {
                "user": selected_user["name"],
            }

            response = requests.post(
                f"{BASE_URL}/upload/",
                files=files,
                data=data,
                timeout=120,
            )

            if response.ok:

                st.sidebar.success(
                    "✅ File uploaded successfully."
                )

            else:

                st.sidebar.error(
                    response.text
                )

##################################################
# Chat
##################################################

st.title("🤖 Employee Project Assistant")
if role == "employee":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a question")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            placeholder = st.empty()

            answer = ""

            tool_calls = []

            payload = {
                "message": prompt,
                "thread_id": str(selected_user["id"]),
                "user": selected_user["id"],
                "project_name": selected_project["name"],
            }

            with requests.post(
                f"{BASE_URL}/chat/stream/",
                json=payload,
                stream=True,
                timeout=300,
            ) as response:

                for line in response.iter_lines():

                    if not line:
                        continue

                    line = line.decode()

                    if line.startswith("data: "):
                        line = line[6:]

                    if line == "[DONE]":
                        break

                    event = json.loads(line)

                    if event["type"] == "token":

                        answer += event["content"]

                        placeholder.markdown(answer + "▌")

                    elif event["type"] == "tool_call":

                        tool_calls.append(event)

            placeholder.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            if tool_calls:

                with st.expander("🧠 Agent Execution"):

                    for tool in tool_calls:

                        st.write(tool["tool"])

                        if isinstance(tool["input"], dict):
                            st.json(tool["input"])
                        else:
                            st.write(tool["input"])

                        st.write(tool["output"])

##################################################
# Admin
##################################################

if role == "Admin":

    st.divider()

    st.header("Permission Management")

    for permission in permissions:

        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])

        with c1:
            st.write(permission["user_name"])

        with c2:
            st.write(permission["project_name"])

        with c3:

            access = st.toggle(
                "Access",
                value=permission["access"],
                key=f"{permission['user_id']}_{permission['project_id']}",
            )

        with c4:

            if st.button(
                "Save",
                key=f"save_{permission['user_id']}_{permission['project_id']}",
            ):

                payload = {
                    "user_id": permission["user_id"],
                    "project_id": permission["project_id"],
                    "access": access,
                }

                try:

                    response = requests.post(
                        f"{BASE_URL}/admin/update-permission",
                        json=payload,
                        timeout=30,
                    )

                    response.raise_for_status()

                    result = response.json()

                    if result["success"]:

                        st.success(result["message"])

                        st.cache_data.clear()

                        st.rerun()

                    else:

                        st.error(result["message"])

                except Exception as e:

                    st.error(str(e))