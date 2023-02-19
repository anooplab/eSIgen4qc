import re
import argparse
import subprocess


<<<<<<< HEAD
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
            float(l.strip().split()[4])
            for l in reversed(list(open(orca_output_file)))
            if 'FINAL SINGLE POINT ENERGY' in l
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
    This function reads the gibbs energy correction from the output file of the Orca quantum chemistry software.

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


def count_imag(orca_output_file: str) -> bool | int | None:
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
=======
def read_energy(orca_output_file: str) -> float:
    """
    Given a file path to an ORCA output file, return the final single point energy
    from the file. If the energy cannot be found in the file, return None.
    """
    for l in reversed(list(open(orca_output_file))):
        if 'FINAL SINGLE POINT ENERGY' in l:
            return float(l.strip().split()[4])
>>>>>>> db283fc4eea410498f8d5e778e6185a492901706
    else:
        return None


def convert_to_docx(md_file, docx_file):
    '''
    Convert the markdown file to docx file using pandoc.
    '''
    subprocess.run(['pandoc', md_file, '-o', docx_file])


def convert_to_tex(md_file, tex_file):
    '''
    Convert the markdown file to tex file using pandoc.
    '''
    subprocess.run(['pandoc', md_file, '-o', tex_file])


def convert_to_pdf(md_file, pdf_file):
    '''
    Convert the markdown file to pdf file using pandoc.
    '''
    subprocess.run(['pandoc', md_file, '-o', pdf_file])


def write_markdown(data, output_file):
    """
    Write the data to the output file.
    """
    with open(output_file, 'w') as f:
        f.write(data)


def main():
    """
    Read energies from ORCA output files and create a table suitable for
    Supporting Information.
    """
    parser = argparse.ArgumentParser(description='''
    Read energies from ORCA output files and create a table suitable for
    Supporting Information 
    ''',)

    parser.add_argument('output_file', nargs='+', help='OrCA output file(s) to '
                                                       'read energies from')
    parser.add_argument('-o', '--output', default=None, help='Output file')

    args = parser.parse_args()

    orca_output_files = args.output_file
    output_file = args.output
    print("something")

    # create a string with the data
    data = '| Name | Total Energy | Gibbs Free Energy | Free energy ' \
           'correction | ZPE | NImag |\n| --- | --- | --- | --- | --- | --- | ' \
           '--- |\n'

    for orca_output_file in orca_output_files:
        e = read_energy(orca_output_file)
        f = read_free_energy(orca_output_file)
        fc = read_gibbs_correction(orca_output_file)
        zpe = read_zpe(orca_output_file)
        nimag = count_imag(orca_output_file)

        # add a row to the string
        row = f'| {re.sub(".out", "", orca_output_file)} | {e or 0:.5f} | {f or 0:.5f} | {fc or 0:.5f} | {zpe or 0:.5f} | {nimag or 0} |\n'
        data += row

    if output_file is None:
        print(data)
    elif output_file.endswith('.md'):
        write_markdown(data, output_file)
    elif output_file.endswith('.docx'):
        write_markdown(data, 'data.md')
        convert_to_docx('data.md', output_file)
    elif output_file.endswith('.tex'):
        write_markdown(data, 'data.md')
        convert_to_tex('data.md', output_file)
    elif output_file.endswith('.pdf'):
        write_markdown(data, 'data.md')
        convert_to_pdf('data.md', output_file)
    else:
        raise ValueError('Unknown output file format')


if __name__ == '__main__':
    main()
