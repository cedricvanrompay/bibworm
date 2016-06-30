# standard libraries
import subprocess

def open_pdf(path_to_pdf):
    subprocess.Popen(['evince', path_to_pdf],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
