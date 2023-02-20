# eSIgen4qc
eSIgen4qc is a Python command-line tool that reads and analyses data from 
Orca quantum chemistry output files. This tool provides various functions for 
the extracting Total energy, Gibbs Free energy, ZPE, and the number of imaginary
frequencies. The user can call the tool and provide the name of the Orca output 
files to collect the data create Markdown, docx, pdf, or tex file, or just print
to the terminal.

Usage

    Open the terminal.
    Navigate to the location of the files.
    Run python <path/to/python/script/eSIgen4qc.py followed by the names of the Orca output files.

The tool provides the following functionalities:

    Reads the single point energy from a given ORCA output file.
    Reads Gibbs free energy from Orca output file.
    Reads the gibbs energy correction from the output file of the Orca quantum chemistry software.
    Reads the zero-point energy (ZPE) from the ORCA output file.
    Counts the number of imaginary frequencies in an ORCA output file.
    Converts the markdown file to tex file using pandoc.
    Converts the markdown file to pdf file using pandoc.
    Writes data to an output file in Markdown format.
    Writes data to a DOCX file.

Installation

    Clone this repository: git clone https://github.com/biostars/python-orca.git
    Navigate into the cloned directory.
    Run pip install -r requirements.txt to install the required packages.
    The tool is now ready to use.

Dependencies

    argparse
    subprocess
    pandas
    docx (to convert Markdown to docx format)
    pandoc (to convert Markdown to pdf format and Markdown to tex format)


Contributing

Contributions are welcome. Please fork the repository, make changes, and submit a pull request.
License

This software is licensed under the GPLv3 License. Please refer to the LICENSE file for more information.