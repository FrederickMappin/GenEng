import streamlit as st
import pandas as pd

def single_aa_sub(filename, position):
    amino_acids = {
        'A': 'Alanine',
        'R': 'Arginine',
        'N': 'Asparagine',
        'D': 'Aspartic acid',
        'C': 'Cysteine',
        'E': 'Glutamic acid',
        'Q': 'Glutamine',
        'G': 'Glycine',
        'H': 'Histidine',
        'I': 'Isoleucine',
        'L': 'Leucine',
        'K': 'Lysine',
        'M': 'Methionine',
        'F': 'Phenylalanine',
        'P': 'Proline',
        'S': 'Serine',
        'T': 'Threonine',
        'W': 'Tryptophan',
        'Y': 'Tyrosine',
        'V': 'Valine'
    }
    
    data = pd.read_csv(filename, comment='>', header=None)
    sequence = ''.join(data[0].tolist())  # Join all sequences into one

    if position > len(sequence):
        st.error(f"Error: Position {position} is greater than sequence length {len(sequence)}")
        return  
    
    output_data = []
    for aa in amino_acids.keys():
        new_sequence = sequence[:position - 1] + aa + sequence[position:]
        output_data.append([aa, position, new_sequence])

    output_df = pd.DataFrame(output_data, columns=['Amino Acid', 'Position', 'New Sequence'])
    return output_df

st.title('Mutant Maker')
fasta_file = st.file_uploader("Upload FASTA", type=['fasta', 'fa'])
position = st.number_input('Position', min_value=1, value=1, step=1)

if st.button('Generate Mutations'):
    if fasta_file is not None and position is not None:
        df = single_aa_sub(fasta_file, position)
        st.dataframe(df)
    else:
        st.error('Please upload a file and specify a position.')