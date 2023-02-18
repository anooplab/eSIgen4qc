import sys
import argparse
import subprocess


def read_energy(orca_output_file: str) -> float:
    """
    Given a file path to an ORCA output file, return the final single point energy
    from the file. If the energy cannot be found in the file, return None.
    """
    for l in reversed(list(open(orca_output_file))):
        if 'FINAL SINGLE POINT ENERGY' in l:
            return float(l.strip().split()[4])
    else:
        return None


def read_free_energy(orca_output_file):
    for line in reversed(list(open(orca_output_file))):
        if 'Final Gibbs free energy' in line:
            return float(line.strip().split()[5])
    else:
        return None

def read_gibbs_correction(orca_output_file):
    for line in reversed(list(open(orca_output_file))):
        if 'G-E(el)' in line:
            return float(line.strip().split()[2])
    else:
        return None

def read_zpe(orca_output_file):
    for line in reversed(list(open(orca_output_file))):
        if 'Non-thermal (ZPE) correction' in line:
            return float(line.strip().split()[3])
    else:
        return None

def count_imag(orca_output_file):
    if 'VIBRATIONAL FREQUENCIES' in open(orca_output_file).read(): 
        nimag = 0
        for line in reversed(list(open(orca_output_file))):
            if '***imaginary mode***' in line:
                nimag += 1
        return nimag
    else:
        return None




parser = argparse.ArgumentParser(description='''
   Read energies from ORCA output files and create a table suitable for
Supporting Information 
   ''',)

parser.add_argument('output_file', nargs='+')

args = parser.parse_args()

orca_output_files = args.output_file

# create a string with the data
data = '''| Name | Total Energy | Gibbs Free Energy | Free energy correction | ZPE | NImag | Name |
| --- | --- | --- | --- | --- | --- | --- |
'''

for i, output_file in enumerate(orca_output_files):
    e = read_energy(output_file)
    f = read_free_energy(output_file)
    fc = read_gibbs_correction(output_file)
    zpe = read_zpe(output_file)
    nimag = count_imag(output_file)

    # add a row to the string
    row = f'| {i} | {e if e else 0:.5f} | {f if f else 0:.5f} | {fc if fc else 0:.5f} | {zpe if zpe else 0:.5f} | {nimag if nimag else 0} | {output_file} |\n'
    data += row

print(data)

# create a markdown file to store the Markdown content
with open('data.md', 'w') as f:
    f.write(data)

