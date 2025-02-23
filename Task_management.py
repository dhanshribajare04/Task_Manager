import streamlit as st
from datetime import datetime, date

class TaskManager:
    def __init__(self):
        if "tasks" not in st.session_state:
            st.session_state.tasks = {}

    def add_task(self, task_id, description, due_date, priority):
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
            st.session_state.tasks[task_id] = {
                'description': description,
                'status': 'Pending',
                'due_date': due_date_obj,
                'priority': priority
            }
            st.success(f"✅ Task '{description}' added with ID {task_id}, Due Date: {due_date}, Priority: {priority}.")
        except ValueError:
            st.error("⚠️ Invalid date format! Please use YYYY-MM-DD.")

    def update_task(self, task_id, status=None, due_date=None):
        if task_id in st.session_state.tasks:
            if status:
                st.session_state.tasks[task_id]['status'] = status
                st.success(f"🔄 Task ID {task_id} status updated to '{status}'.")
            
            if due_date:
                try:
                    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
                    st.session_state.tasks[task_id]['due_date'] = due_date_obj
                    st.success(f"📅 Task ID {task_id} due date updated to {due_date}.")
                except ValueError:
                    st.error("⚠️ Invalid date format! Please use YYYY-MM-DD.")
        else:
            st.error("❌ Task ID not found.")

    def view_tasks(self):
        if not st.session_state.tasks:
            st.warning("No tasks available.")
            return
        for task_id, task in st.session_state.tasks.items():
            due_date = task['due_date'].strftime("%Y-%m-%d")
            days_remaining = (task['due_date'] - date.today()).days
            st.markdown(f"""
            ---
            **📌 Task ID:** `{task_id}`  
            **📝 Description:** `{task['description']}`  
            **📊 Status:** `{task['status']}`  
            **🎯 Priority:** `{task['priority']}`  
            **⏳ Due Date:** `{due_date}`  
            **⏳ Days Remaining:** `{days_remaining}` days
            """)

    def search_task(self, keyword):
        found = False
        for task_id, task in st.session_state.tasks.items():
            if keyword.lower() in task['description'].lower() or keyword.lower() == task['status'].lower():
                due_date = task['due_date'].strftime("%Y-%m-%d")
                days_remaining = (task['due_date'] - date.today()).days
                st.markdown(f"""
                ---
                **🔍 Task ID:** `{task_id}`  
                **📝 Description:** `{task['description']}`  
                **📊 Status:** `{task['status']}`  
                **🎯 Priority:** `{task['priority']}`  
                **⏳ Due Date:** `{due_date}`  
                **⏳ Days Remaining:** `{days_remaining}` days
                """)
                found = True
        if not found:
            st.warning("🚫 No matching tasks found.")

# Streamlit UI
st.set_page_config(page_title="Task Manager", page_icon="✅", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 5px;
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #007BFF;
    }
    .stSelectbox>div>div>select {
        border-radius: 5px;
        border: 1px solid #007BFF;
    }
    .stMarkdown {
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📝 Task Manager with Streamlit")

manager = TaskManager()

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Task", "🔄 Update Task", "📋 View Tasks", "🔍 Search Task"])

with tab1:
    st.subheader("➕ Add a New Task")
    task_id = st.text_input("Enter Task ID")
    description = st.text_input("Enter Task Description")
    due_date = st.date_input("Enter Due Date", min_value=date.today())
    priority = st.selectbox("Select Priority", ["High", "Medium", "Low"])
    if st.button("Add Task"):
        if task_id and description:
            manager.add_task(task_id, description, due_date.strftime("%Y-%m-%d"), priority)
        else:
            st.warning("⚠️ Please enter Task ID and Description.")

with tab2:
    st.subheader("🔄 Update Task Status or Due Date")
    task_id_update = st.text_input("Enter Task ID to Update")
    status = st.selectbox("Select New Status", ["", "Pending", "In Progress", "Completed"])
    due_date_update = st.date_input("Update Due Date", min_value=date.today())
    if st.button("Update Task"):
        if task_id_update:
            manager.update_task(task_id_update, status if status else None, due_date_update.strftime("%Y-%m-%d"))
        else:
            st.warning("⚠️ Please enter a valid Task ID.")

with tab3:
    st.subheader("📋 View All Tasks")
    manager.view_tasks()

with tab4:
    st.subheader("🔍 Search Task by Description or Status")
    keyword = st.text_input("Enter Description or Status")
    if st.button("Search"):
        manager.search_task(keyword)
