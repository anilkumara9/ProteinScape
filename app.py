import streamlit as st
from stmol import showmol
import py3Dmol
import tempfile
import re
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import numpy as np
import seaborn as sns
import requests

# Define function to predict structure using ESMFold API
@st.cache_resource
def predict_structure_api(sequence):
    """Use the ESMFold API to predict the protein structure."""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence, timeout=60)
        response.raise_for_status()
        pdb_content = response.content.decode('utf-8')
    except requests.exceptions.RequestException as e:
        st.error(f"Error during prediction: {e}")
        pdb_content = None
    return pdb_content

def validate_sequence(sequence):
    """Validate if the sequence contains only valid amino acid characters."""
    valid_chars = re.compile(r'^[ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy]+$')
    if valid_chars.match(sequence):
        return True
    else:
        return False

def show_structure(pdb_str, style='cartoon'):
    """Use py3Dmol to show the structure with different styles."""
    view = py3Dmol.view(width=800, height=500)
    view.addModel(pdb_str, "pdb")
    view.setStyle({style: {'color': 'spectrum'}})
    view.setBackgroundColor('white')
    view.zoomTo()
    view.spin(True)
    return view

def plot_amino_acid_distribution(sequence):
    """Plot the amino acid distribution in the given sequence."""
    sequence = sequence.upper()
    amino_acid_count = Counter(sequence)
    amino_acids = list(amino_acid_count.keys())
    counts = list(amino_acid_count.values())
    
    fig, ax = plt.subplots()
    ax.bar(amino_acids, counts, color='skyblue')
    ax.set_xlabel('Amino Acid')
    ax.set_ylabel('Count')
    ax.set_title('Amino Acid Distribution')
    st.pyplot(fig)

def plot_ramachandran():
    """Plot a sample Ramachandran plot."""
    x = np.random.uniform(-180, 180, 1000)
    y = np.random.uniform(-180, 180, 1000)
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.histplot(x=x, y=y, bins=100, pthresh=.1, cmap="mako", ax=ax)
    ax.set_xlabel('Phi (ϕ) Angle')
    ax.set_ylabel('Psi (ψ) Angle')
    ax.set_title('Sample Ramachandran Plot')
    st.pyplot(fig)

# Sidebar for navigation
st.set_page_config(
    page_title="ProteinScape",  # Your app's title
    page_icon="favicon.ico",  # Path to your favicon file
)
st.sidebar.image('logo.png', width=200)  # Add a logo (adjust the path accordingly)

# Sidebar title and introduction
st.sidebar.title('🧬 ProteinScape: Protein Structure Prediction and Visualization')
st.sidebar.write('[*ProteinScape*](https://esmatlas.com/about) is a powerful web application designed to predict and visualize the 3D structure of proteins from their amino acid sequences. Leveraging the ESMFold API, this tool provides an intuitive interface for researchers, educators, and students to gain insights into protein structures. Whether you are analyzing a single protein or multiple sequences, ProteinScape offers an easy and effective solution for visualization and structure prediction.')
st.sidebar.markdown("---")  # Divider

# Navigation options
app_mode = st.sidebar.radio(
    "Choose Prediction Type:",
    ["Single Protein Structure Prediction", "Multiple Protein Structure Prediction"]
)
st.sidebar.markdown("---")  # Divider

# Additional information
st.sidebar.header("About")
st.sidebar.write(
    "This tool is designed to predict the 3D structure of proteins based on their sequence using the ESMFold API. "
    "Upload a sequence to see the predicted structure and download the corresponding PDB file."
)
st.sidebar.markdown("---")  # Divider

# Contact information
st.sidebar.write("Created by Abdul Rehman Ikram. For feedback, contact: [hanzo7n@gmail.com](mailto:hanzo7n@gmail.com)")

# Main app logic
if app_mode == "Single Protein Structure Prediction":
    st.title("Single Protein Structure Prediction")
    st.write("Enter a protein sequence below to predict its structure.")
    
    # Input for single sequence
    DEFAULT_SEQ = "MKTAYIAKQRQISFVKSHFSRQDILDLWQYFSYGRAL"
    input_sequence = st.text_area("Enter Protein Sequence:", DEFAULT_SEQ, height=275)
    
    # Validate sequence and predict structure
    if st.button("Predict Structure"):
        if input_sequence:
            if validate_sequence(input_sequence):
                st.write("Predicting structure, please wait...")
                pdb_str = predict_structure_api(input_sequence)
                if pdb_str:
                    st.session_state.pdb_str = pdb_str
            else:
                st.warning("Invalid sequence. Please enter a valid protein sequence containing only standard amino acid characters.")
        else:
            st.warning("Please enter a valid protein sequence.")

    # Display 3D visualization if structure is available
    if 'pdb_str' in st.session_state:
        st.write("### Predicted Protein Structure")
        visualization_style = st.selectbox("Select Visualization Style:", ["cartoon", "stick"])
        view = show_structure(st.session_state.pdb_str, style=visualization_style)
        view_html = view._make_html()
        st.components.v1.html(view_html, height=500)
        
        # Save and allow PDB download
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdb") as temp_pdb:
            temp_pdb.write(st.session_state.pdb_str.encode())
            temp_pdb.close()
            st.download_button(
                label="Download PDB File",
                data=open(temp_pdb.name, 'rb').read(),
                file_name="predicted_structure.pdb",
                mime="text/plain"
            )

    # Amino Acid Distribution
    if input_sequence and validate_sequence(input_sequence):
        st.write("### Amino Acid Distribution")
        plot_amino_acid_distribution(input_sequence)
        
        # Ramachandran Plot
        st.write("### Sample Ramachandran Plot")
        plot_ramachandran()

elif app_mode == "Multiple Protein Structure Prediction":
    st.title("Multiple Protein Structure Prediction")
    st.write("Upload a file with multiple protein sequences (FASTA format) to predict their structures or enter sequences manually.")
    
    # File uploader for multiple sequences
    uploaded_file = st.file_uploader("Upload FASTA File (Optional):", type=["fasta", "txt"])
    input_sequences = st.text_area("Or enter multiple protein sequences (FASTA format):", height=275)
    
    sequences = []
    if uploaded_file is not None:
        sequences = uploaded_file.read().decode('utf-8').split('>')[1:]
        sequences = [seq.partition('\n')[2].replace('\n', '') for seq in sequences]
    elif input_sequences:
        sequences = input_sequences.split('>')[1:]
        sequences = [seq.partition('\n')[2].replace('\n', '') for seq in sequences]
    
    # Processing and prediction
    if sequences:
        st.write("Processing uploaded sequences...")
        progress_bar = st.progress(0)
        total_sequences = len(sequences)
        valid_sequences = []
        
        for idx, sequence in enumerate(sequences):
            if len(sequence) > 1500:
                st.warning(f"Sequence {idx + 1} is too long and will be skipped (max length: 1500 characters).")
                continue
            if not validate_sequence(sequence):
                st.warning(f"Sequence {idx + 1} contains invalid characters and will be skipped.")
                continue
            
            st.write(f"### Predicted Structure for Sequence {idx + 1}")
            pdb_str = predict_structure_api(sequence)
            
            # Display 3D visualization
            if pdb_str:
                visualization_style = st.selectbox(f"Select Visualization Style for Sequence {idx + 1}:", ["cartoon", "stick"], key=f"style_{idx}")
                view = show_structure(pdb_str, style=visualization_style)
                view_html = view._make_html()
                st.components.v1.html(view_html, height=500)
                
                # Save and allow PDB download
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_sequence_{idx + 1}.pdb") as temp_pdb:
                    temp_pdb.write(pdb_str.encode())
                    temp_pdb.close()
                    st.download_button(
                        label=f"Download PDB File for Sequence {idx + 1}",
                        data=open(temp_pdb.name, 'rb').read(),
                        file_name=f"predicted_structure_sequence_{idx + 1}.pdb",
                        mime="text/plain"
                    )
                valid_sequences.append(sequence)
                
                # Amino Acid Distribution
                st.write(f"### Amino Acid Distribution for Sequence {idx + 1}")
                plot_amino_acid_distribution(sequence)
                
                # Ramachandran Plot
                st.write(f"### Sample Ramachandran Plot for Sequence {idx + 1}")
                plot_ramachandran()
            
            # Update progress
            progress_bar.progress((idx + 1) / total_sequences)
        
        if valid_sequences:
            st.write(f"**Summary:** Successfully processed {len(valid_sequences)} out of {total_sequences} sequences.")
    else:
        st.warning("Please upload a valid FASTA file or enter sequences in the provided text area.")

# Footer with disclaimer
st.markdown("---")
st.write("**Disclaimer:** This tool provides predicted protein structures based on input sequences. These predictions are for research purposes only and should not be used for clinical decision-making.")