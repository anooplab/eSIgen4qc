import re
import argparse
import subprocess


def read_energy(orca_output_file: str) -> float | None:
    """
    Reads the single point energy from a given ORCA output file

    Parameters
    ----------
    orca_output_file : str
        Path to the orca output file

    Returns
    -------
    float
        The single point energy read from the ORCA output file
    None
        Returns None if no single point energy is found in the ORCA output file
    """
    return next(
        (
            float(line.strip().split()[4])
            for line in reversed(list(open(orca_output_file)))
            if 'FINAL SINGLE POINT ENERGY' in line
        ),
        None,
    )


def read_free_energy(orca_output_file: str) -> float | None:
    """
    Read Gibbs free energy from Orca output file.

    Parameters
    ----------
    orca_output_file : str
        Path to Orca output file.


    Returns
    -------
    float
        The Gibbs free energy read from the ORCA output file
    None
        Returns None if no free energy is found in the ORCA output file
    """
    return next(
        (
            float(line.strip().split()[5])
            for line in reversed(list(open(orca_output_file)))
            if 'Final Gibbs free energy' in line
        ),
        None,
    )


def read_gibbs_correction(orca_output_file: str) -> float:
    """
    This function reads the gibbs energy correction from the output file of the
    Orca quantum chemistry software.

    Parameters
    ----------
    orca_output_file : str
        Path to the Orca output file.

    Returns
    -------
    float
        The gibbs energy correction.
    """
    return next(
        (
            float(line.strip().split()[2])
            for line in reversed(list(open(orca_output_file)))
            if 'G-E(el)' in line
        ),
        None,
    )


def read_zpe(orca_output_file: str) -> float:
    """
    This function reads the zero-point energy (ZPE) from the ORCA output file.

    Parameters
    ----------
    orca_output_file : str
        The path to the ORCA output file.

    Returns
    -------
    float
        The zero-point energy (ZPE) of the ORCA run.
    """
    return next(
        (
            float(line.strip().split()[3])
            for line in reversed(list(open(orca_output_file)))
            if 'Non-thermal (ZPE) correction' in line
        ),
        None,
    )


def count_imaginary_modes(orca_output_file: str) -> bool | int | None:
    """Count the number of imaginary frequencies in an ORCA output file.

    Args:
        orca_output_file (str): The name of the ORCA output file.

    Returns:
        int: The number of imaginary frequencies in the ORCA output file. If no
             imaginary frequencies are found, None is returned.
    """
    if 'VIBRATIONAL FREQUENCIES' in open(orca_output_file).read():
        return sum(
            '***imaginary mode***' in line
            for line in reversed(list(open(orca_output_file)))
        )
    else:
        return None


def convert_to_tex(md_file, tex_file):
    """
    Convert the markdown file to tex file using pandoc.
    """
    subprocess.run(['pandoc', md_file, '-o', tex_file])


def convert_to_pdf(md_file, pdf_file):
    """
    Convert the markdown file to pdf file using pandoc.
    """
    subprocess.run(['pandoc', md_file, '-o', pdf_file])


def write_docx(csv_string, docx_file):
    import docx
    # Split the CSV string into lines
    lines = csv_string.strip().split('\n')

    # Split each line on the comma separator to get the fields
    csv_data = [line.split(',') for line in lines]

    # Create a new Word document
    doc = docx.Document()

    # Add a table to the document
    table = doc.add_table(rows=len(data), cols=len(data[0]))

    # Write the data to the table
    for i, the_row in enumerate(csv_data):
        for j, value in enumerate(the_row):
            table.cell(i, j).text = value

    # Save the document to a file
    doc.save(docx_file)


def write_markdown(csv_string, md_file):
    """
    Write the data to the output file in Markdown format.
    """
    # Split the CSV string into lines
    lines = csv_string.strip().split('\n')

    # Split each line on the comma separator to get the fields
    csv_data = [line.split(',') for line in lines]

    # Calculate the maximum width for each column
    max_widths = [len(field) + 1 for field in data[0]]
    with open(md_file, 'w') as fp:
        for i, the_row in enumerate(list(csv_data)):
            fp.write(f"| {' | '.join(the_row)} |\n")
            # Write the header row as a table
            if i == 0:
                fp.write(f"|{'-|'.join('-' * w for w in max_widths)}-|\n")


def print_tabular(csv_string):
    # Split the CSV string into lines and fields
    lines = csv_string.split('\n')
    fields = [line.split(',') for line in lines]

    # Find the maximum length of each field in each column
    max_lengths = [max(len(field[i]) for field in fields) for i in
                   range(len(fields[0]))]

    # Print the fields with adjusted column widths
    for field in fields:
        print('  '.join('{:>{}}'.format(field[i], max_lengths[i]) for i in
                        range(len(field))))


parser = argparse.ArgumentParser(description='''
Read energies from ORCA output files and create a table suitable for
Supporting Information 
''', )

parser.add_argument('orca_files', nargs='+', help='OrCA output file(s) to '
                                                  'read energies from')
parser.add_argument('-o', '--output', default=None, help='Output file')

args = parser.parse_args()

orca_output_files = args.orca_files
output_file = args.output

# create a string with the data
data = 'Name,Total Energy,Gibbs Free Energy,Free energy correction,ZPE,NImag'

for orca_file in orca_output_files:
    e = read_energy(orca_file)
    f = read_free_energy(orca_file)
    fc = read_gibbs_correction(orca_file)
    zpe = read_zpe(orca_file)
    n_imag = count_imaginary_modes(orca_file)

    # add a row to the string
    row = f'\n{re.sub(".out", "", orca_file)},' \
          f'{e or 0:.5f},{f or 0:.5f},{fc or 0:.5f},{zpe or 0:.5f},' \
          f'{n_imag or 0}'
    data += row

if output_file is None:
    print_tabular(data)
elif output_file.endswith('.md'):
    write_markdown(data, output_file)
elif output_file.endswith('.docx'):
    write_docx(data, output_file)
elif output_file.endswith('.tex'):
    write_markdown(data, 'data.md')
    convert_to_tex('data.md', output_file)
elif output_file.endswith('.pdf'):
    write_markdown(data, 'data.md')
    convert_to_pdf('data.md', output_file)
else:
    raise ValueError('Unknown output file format')
