ProteinScape: Protein Structure Prediction Application
ProteinScape is a web-based application designed to predict and visualize the 3D structure of proteins from amino acid sequences. This application leverages the ESMFold API for structural predictions and provides an intuitive interface for researchers, educators, and students to gain insights into protein structures.

Features
Single Protein Structure Prediction: Predict the 3D structure of a single protein sequence.
Multiple Protein Structure Prediction: Predict the structure for multiple protein sequences (from FASTA file or manual input).
3D Visualization: Interactive 3D visualization of predicted protein structures using py3Dmol.
Amino Acid Distribution Analysis: Graphical display of the amino acid composition in the input sequence.
Sample Ramachandran Plot: A sample Ramachandran plot is generated for each sequence, showing the phi (ϕ) and psi (ψ) angles.
Tech Stack
Frontend: Streamlit
Backend: ESMFold API
Visualization: Py3Dmol
Plotting: Matplotlib, Seaborn
Data Handling: Pandas, Collections
Requests: Python requests library for API calls

Installation

Clone the repository:

git clone https://github.com/your-username/proteinscape.git
cd proteinscape
Install the required dependencies:

pip install -r requirements.txt
Ensure that you have installed all the required Python packages in requirements.txt:

streamlit
py3Dmol
matplotlib
seaborn
pandas
requests
numpy

Run the application:
streamlit run app.py
Open the provided localhost link in your browser.

Usage
Single Protein Structure Prediction
Enter a valid protein sequence (amino acids: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y).
Click the "Predict Structure" button.
View the predicted 3D structure of the protein in the interactive viewer.
Download the predicted structure as a .pdb file.
View the amino acid distribution and sample Ramachandran plot for further insights.
Multiple Protein Structure Prediction
Upload a FASTA file with multiple protein sequences or manually input sequences in FASTA format.
The application will predict the structure for each sequence and allow visualization and downloading of each result.
Similar to single predictions, view the amino acid distribution and Ramachandran plot for each sequence.
3D Visualization
Use the py3Dmol viewer to interact with the predicted protein structure.
Select different visualization styles: cartoon or stick.
API Information
The application uses the ESMFold API for protein structure prediction. The predicted output is displayed in .pdb format, which is rendered in the web application for real-time interaction.

Example Input
A valid protein sequence:
MKTAYIAKQRQISFVKSHFSRQDILDLWQYFSYGRAL

Output
3D predicted structure of the protein.
Downloadable .pdb file.
Bar chart of amino acid distribution.
Sample Ramachandran plot.

Known Limitations
The application can only predict structures for sequences shorter than 1,500 amino acids due to the ESMFold API limitations.
The predictions are based on AI models and should not be used for clinical purposes.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contact
For questions, feedback, or issues, please contact:

Abdul Rehman Ikram hanzo7n@gmail.com
