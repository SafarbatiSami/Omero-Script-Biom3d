import omero
import omero.scripts as scripts
from omero.gateway import BlitzGateway
from omero.rtypes import rstring

# Constants for script parameters
PARAM_PY_FILE = "Python File"

def get_all_py_file_annotations(conn):
    """
    Retrieve all .py file annotations in the current session.
    """
    py_files = []
    
    # Get all file annotations in the current session
    file_annotations = conn.getObjects("FileAnnotation")
    for ann in file_annotations:
        file_name = ann.getFile().getName()
        if file_name.endswith('.py'):
            py_files.append((file_name, ann.getId()))
    
    return py_files

def print_py_files(py_files):
    """
    Print all .py files with their IDs.
    """
    for idx, (name, id) in enumerate(py_files, start=1):
        print(f"{idx}: {name} (ID: {id})")

def run_as_script():
    client = scripts.client(
        'List Python File Annotations',
        """
        This script lists all Python (.py) file annotations for Biom3d in the current session.
        """,
        version = "1.0",
        authors = ["Sami SAFARBATI"],
        institutions = ["GReD"],
        contact = "sami.safarbati@uca.fr",
    )
    
    try:
        conn = BlitzGateway(client_obj=client)
        
        py_files = get_all_py_file_annotations(conn)
        
        if not py_files:
            print("No .py files found")
        else:
            # Print all .py files with their IDs
            print_py_files(py_files)
        
        # If needed, retrieve the selected file
        # selected_file = client.getInput(PARAM_PY_FILE, unwrap=True)
        # print("Selected Python file:", selected_file)
        
    finally:
        client.closeSession()

if __name__ == "__main__":
    run_as_script()
