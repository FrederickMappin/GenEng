import pandas as pd
import argparse

def single_aa_sub(filename, position, output_filename):
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
        print(f"Error: Position {position} is greater than sequence length {len(sequence)}")
        return  
    
    
    output_data = []
    for aa in amino_acids.keys():
        new_sequence = sequence[:position - 1] + aa + sequence[position:]
        output_data.append([aa, position, new_sequence])

    output_df = pd.DataFrame(output_data, columns=['Amino Acid', 'Position', 'New Sequence'])
    output_df.to_csv(output_filename, index=False)

def main(args):
    if args.function == 'single_aa_sub':
        single_aa_sub(args.fasta, args.pos, args.output)
    else:
        print(f"Unknown function: {args.function}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--function', type=str, required=True, help='The function to execute')
    parser.add_argument('--fasta', type=str, required=True, help='The path to the fasta file')
    parser.add_argument('--pos', type=int, required=True, help='The position in the sequence to substitute')
    parser.add_argument('--output', type=str, required=True, help='The path to the output CSV file')
    args = parser.parse_args()

    main(args)

'''
python mutantmaker.py --function single_aa_sub --fasta /Users/freddymappin/Desktop/gene.fa --pos 10 --output /Users/freddymappin/Desktop/gene2.csv  
'''