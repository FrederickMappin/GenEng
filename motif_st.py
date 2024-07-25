import streamlit as st
import pandas as pd
import re

# Function to find the complement of a nucleotide
def complement(nucleotide):
    return {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}.get(nucleotide, nucleotide)

# Function to find the reverse complement of the motif
def reverse_complement(seq):
    return ''.join([complement(nucleotide) for nucleotide in reversed(seq)])

def motif_finder(sequence, motif, sgRNA_length):
    # Convert motif to a regular expression, where "N" matches any character
    motif_regex = motif.replace('N', '.')
    motif_regex = '(?=(' + motif_regex + '))'
    start_locations = [match.start() for match in re.finditer(motif_regex, sequence)]
    valid_start_locations = [start for start in start_locations if start >= sgRNA_length]
    sequences_before_motif = []
    data_for_df = []

    for start in valid_start_locations:
        seq_start = max(start - sgRNA_length, 0)
        seq_before_motif = sequence[seq_start:start]
        motif_seq = sequence[start:start + len(motif)]
        sequences_before_motif.append(seq_before_motif)
        data_for_df.append({"Start_Position": start + 1, "Forward": seq_before_motif, "Motif": motif_seq})

    df = pd.DataFrame(data_for_df)

    rev_complement_motif = reverse_complement(motif)
    rev_complement_motif_regex = rev_complement_motif.replace('N', '.')
    rev_complement_motif_regex = '(?=(' + rev_complement_motif_regex + '))'
    end_locations_revC = [match.end() + len(rev_complement_motif) for match in re.finditer(rev_complement_motif_regex, sequence)]
    valid_start_locations = [loc for loc in end_locations_revC if loc + sgRNA_length <= len(sequence)]
    sequences_after_motif = []
    data_for_df_rev = []

    for end in valid_start_locations:
        motif_start = (end - len(motif))
        motif_seq = sequence[motif_start:end]
        rev_comp_motif_seq = reverse_complement(motif_seq)
        sgRNA_length_end = end + sgRNA_length
        seq_after_motif = sequence[end + 1:sgRNA_length_end]
        rev_comp_seq_after_motif = reverse_complement(seq_after_motif)
        sequences_after_motif.append(rev_comp_seq_after_motif)
        data_for_df_rev.append({"Start_Position": sgRNA_length_end - 1, "Reverse": rev_comp_seq_after_motif, "Motif": rev_comp_motif_seq})

    df2 = pd.DataFrame(data_for_df_rev)

    return df, df2

# Streamlit app starts here
st.title('Cas Guide Design Tool')
st.markdown("""
## Welcome to the Cas Guide Design Tool App

This application allows you to find specific motifs within a DNA sequence. You can upload a file containing the sequence, specify the motif you are looking for, and define the length of the sgRNA.

### Instructions:
1. **Upload a File**: Upload a file containing the DNA sequence in CSV format.
2. **Enter the Motif**: Specify the motif you are looking for (e.g., 'NGG').
3. **Specify sgRNA Length**: Enter the length of the sgRNA designed directly upstream of motif.""")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    sequence = ''.join(pd.read_csv(uploaded_file, comment='>', header=None)[0].tolist())
    motif = st.text_input('Enter the motif', 'NGG')
    sgRNA_length = st.number_input('Enter the sgRNA length', min_value=1, value=20)

    if st.button('Find Motifs'):
        df, df2 = motif_finder(sequence, motif, sgRNA_length)
        st.write("Sequences Before Motif:")
        st.dataframe(df)
        st.write("Sequences After Motif:")
        st.dataframe(df2)