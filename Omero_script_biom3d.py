#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
------------------------------------------------------------------------------
This runs Biom3d on the selected data.

@author Sami SAFARBATI
<a href="mailto:sami.safarbati@uca.fr">sami.safarbati@uca.fr</a>
@version 5.6
"""

import os
import omero
import omero.scripts as scripts
from omero.gateway import BlitzGateway
from omero.rtypes import rstring, rlong
from biomero import SlurmClient
# ssh hpc2 srun --mail-user=jean.dupont@uca.fr /storage/groups/omero/job.sh dataset_id project_id session_id group_id


PARAM_IMG_DIR = "Image Directory :"
PARAM_MSK_DIR = "Mask Directory :"
PARAM_NUM_CLASSES = "Number of classes :"
PARAM_MAIL = "Mail :"
PARAM_DESC = "Name for your model :"

################################################################################


def run_as_script():
    """
    The main entry point of the script, as called by the client via the 
    scripting service, passing the required parameters. 
    """

    dataTypes = [rstring('tag'),rstring('project'),rstring('dataset'),rstring('image')]
    actions = [rstring('autocrop'),rstring('segmentation')]
    
    client = scripts.client(
        'Biom3d : Preprocessing ',
        """
        Run Preprocessing.
        """,

        scripts.String(PARAM_IMG_DIR, optional=False, grouping="1",
            description="Input Directory :"),
        
        scripts.String(PARAM_MSK_DIR, optional=False, grouping="2",
            description="Mask Directory :"),

        scripts.Long(PARAM_NUM_CLASSES, optional=False, grouping="3",
            description="NUMBER OF CLASSES "),

        scripts.String(PARAM_DESC, optional=False, grouping="4",
            description="Name for your model."),

        scripts.String(PARAM_MAIL, optional=False, grouping="5",
            description="User email."),

        version = "1.0",
        authors = ["Sami ", "SAFARBATI"],
        institutions = ["GReD"],
        contact = "sami.safarbati@uca.fr",
    ) 
    
    conn = BlitzGateway(client_obj=client)
    
    # Process the list of args above. 
    params = {}
    for key in client.getInputKeys():
        if client.getInput(key):
            params[key] = client.getInput(key, unwrap=True)
    
    print("Parameters = %s" % params)



    with SlurmClient.from_config() as slurmClient:
      # Call the main script
      jobs_path = SlurmClient.get_slurm_jobs_path()
      print("jobs path :",jobs_path)
    #command = "ssh localslurm srun --mail-user={0} /data/my-scratch/slurm-scripts/jobs/biom3d.sh --img_dir {1} --msk_dir {2} --num_classes {3}  --desc {4}  ".format(params[PARAM_MAIL], params[PARAM_IMG_DIR], params[PARAM_MSK_DIR], params[PARAM_NUM_CLASSES], params[PARAM_DESC])
    msg = os.popen(command).read()
    
    print(msg)
    client.setOutput("Message", rstring("Done."))

    client.closeSession()


if __name__ == "__main__":
    """
    Python entry point
    """
    run_as_script()
    
