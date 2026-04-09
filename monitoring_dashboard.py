import streamlit as st
import requests
import os

st.title("Exam Reminder Monitoring")

APP_ID = os.getenv("APPINSIGHTS_APP_ID")
ACCESS_TOKEN = os.getenv("AZURE_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def run_query(query):
    url = f"https://api.applicationinsights.io/v1/apps/{APP_ID}/query"
    response = requests.post(url, headers=headers, json={"query": query})
    
    if response.status_code != 200:
        st.error(f"Query failed: {response.text}")
        st.stop()

    return response.json()

# 🔹 Queries
requests_query = """
requests
| summarize count()
"""

errors_query = """
exceptions
| summarize count()
"""

latency_query = """
requests
| summarize avg(duration)
"""

# 🔹 Fetch data
try:
    requests_data = run_query(requests_query)
    errors_data = run_query(errors_query)
    latency_data = run_query(latency_query)

    total_requests = requests_data["tables"][0]["rows"][0][0]
    total_errors = errors_data["tables"][0]["rows"][0][0]
    avg_latency = latency_data["tables"][0]["rows"][0][0]

except Exception as e:
    st.error("Failed to load Azure data")
    st.stop()

# 🔹 Display real values
st.metric("Requests", total_requests)
st.metric("Errors", total_errors)
st.metric("Latency (ms)", round(avg_latency, 2))

st.success("Connected to Azure Application Insights ")