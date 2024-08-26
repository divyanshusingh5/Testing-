import streamlit as st
import openai
import pandas as pd

# Initialize OpenAI API
openai.api_key = 'sk-proj-FGvkF3TW08GqN2AzJkyrT3BlbkFJJdYvoZjFQLLMWclJLHJP'

# Function to generate questions using the LLM
def generate_question(conversation):
    messages = [
        {"role": "system", "content": "You are a design lead gathering requirements from a client for a website project. Ask focused, relevant questions to understand the client's needs and vision. Each question should build upon previous answers."},
    ]
    
    for q, a in conversation:
        messages.append({"role": "assistant", "content": q})
        messages.append({"role": "user", "content": a})
    
    messages.append({"role": "user", "content": "Based on the conversation so far, what's the next important question to ask the client about their website requirements?"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content'].strip()

# Function to generate summary points from the conversation
def generate_summary(conversation):
    summary_prompt = "As a design lead, summarize the following Q&A log into key website design requirements points:\n\n"
    for idx, (question, answer) in enumerate(conversation):
        summary_prompt += f"Q{idx+1}: {question}\nA{idx+1}: {answer}\n\n"
    summary_prompt += "\nProvide a concise list of the main website requirements based on this conversation."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a design lead summarizing client requirements for a website project."},
            {"role": "user", "content": summary_prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    initial_question = "What type of website are you looking to create for your business?"
    st.session_state.conversation.append((initial_question, ""))

# Streamlit Layout
st.set_page_config(layout="wide", page_title="Website Requirements Gathering")
st.title("Website Requirements Gathering Interface")

# Custom CSS for scrollable Q&A Log section
st.markdown("""
    <style>
    .scrollable-section {
        max-height: 600px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for controls and summary
with st.sidebar:
    st.header("Project Summary")
    if st.button("Generate Summary"):
        summary = generate_summary(st.session_state.conversation)
        st.session_state.summary = summary
    
    if 'summary' in st.session_state:
        st.subheader("Website Requirements Summary")
        st.info(st.session_state.summary)
    
    if st.button("Download Q&A Log"):
        df = pd.DataFrame(st.session_state.conversation, columns=["Question", "Answer"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Q&A Log as CSV", data=csv, file_name="website_requirements_qa_log.csv", mime="text/csv")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Conversation with Design Lead")
    
    chat_container = st.container()
    with chat_container:
        for idx, (question, answer) in enumerate(st.session_state.conversation):
            with st.chat_message("assistant"):
                st.markdown(f"**Design Lead:** {question}")
            if answer:
                with st.chat_message("user"):
                    st.markdown(f"**You:** {answer}")

    # Input for user to provide the next answer
    user_input = st.chat_input("Your response:")
    if user_input:
        st.session_state.conversation[-1] = (st.session_state.conversation[-1][0], user_input)
        with chat_container.chat_message("user"):
            st.markdown(f"**You:** {user_input}")
        
        # Generate next question
        with st.spinner("Generating next question..."):
            next_question = generate_question(st.session_state.conversation)
        st.session_state.conversation.append((next_question, ""))
        with chat_container.chat_message("assistant"):
            st.markdown(f"**Design Lead:** {next_question}")
        
        st.rerun()

with col2:
    st.header("Editable Q&A Log")
    
    # Add the scrollable class here
    with st.container():
        st.markdown('<div class="scrollable-section">', unsafe_allow_html=True)
        
        for idx, (question, answer) in enumerate(st.session_state.conversation):
            with st.expander(f"Q&A Pair {idx+1}", expanded=True):
                edited_question = st.text_area(f"Question {idx+1}", value=question, key=f"q{idx}")
                edited_answer = st.text_area(f"Answer {idx+1}", value=answer, key=f"a{idx}")
                
                if st.button("Update", key=f"update{idx}"):
                    st.session_state.conversation[idx] = (edited_question, edited_answer)
                    with st.spinner("Updating conversation..."):
                        for i in range(idx + 1, len(st.session_state.conversation)):
                            new_question = generate_question(st.session_state.conversation[:i])
                            st.session_state.conversation[i] = (new_question, st.session_state.conversation[i][1])
                    st.success("Updated successfully! Subsequent questions have been regenerated.")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("This interface helps gather website requirements through an AI-assisted conversation. Edit responses in the Q&A Log to refine the requirements.")
