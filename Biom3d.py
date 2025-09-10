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
import omero.scripts as scripts
from omero.gateway import BlitzGateway
from omero.rtypes import rstring



PARAM_IMG_DIR = "Image Dataset ID"
PARAM_MSK_DIR = "Mask Dataset ID (Not needed for prediction)"
PARAM_CONFIG = "Configuration File ID (For Train module only)"
PARAM_NUM_CLASSES = "Number of classes (Not needed for prediction)"
PARAM_EPOCHS = "Number of epochs (Not needed for prediction)"
PARAM_MODEL = "Model ID (for prediction only)"
PARAM_HOST = "Hostname"
PARAM_DESC = "Name for your model (Not needed for prediction)"
PARAM_ACTION = "Action"
PARAM_TIME = "Job Time (hh:mm:ss)"
################################################################################


def run_as_script():
    """
    The main entry point of the script, as called by the client via the 
    scripting service, passing the required parameters. 
    """

    actions = [rstring('Autoconfig & Preprocess'),rstring('Train with config file'),rstring('Preprocess & Train'),rstring('Prediction')]
    
    client = scripts.client(
        'Biom3d :  ',
        """
        Run Biom3d in HPC2 Cluster.
        """,

        scripts.String(PARAM_ACTION, optional=False, grouping="00", values=actions,
        description="Action to perform."),

        scripts.String(PARAM_IMG_DIR, optional=False, grouping="01",
            description="Input Directory ID :"),
        
        scripts.String(PARAM_MSK_DIR, optional=True, grouping="02",
            description="Mask Directory ID :"),

        scripts.Int(PARAM_CONFIG, optional=True, grouping="04",
            description="Config ID :"),

        scripts.Long(PARAM_NUM_CLASSES, optional=True, grouping="05",
            description="NUMBER OF CLASSES "),

        scripts.Long(PARAM_EPOCHS, optional=True, grouping="06",
            description="NUMBER OF EPOCHS "),

        scripts.String(PARAM_DESC, optional=True, grouping="07",
            description="Name for your model."),

        scripts.String(PARAM_MODEL, optional=True, grouping="09",
            description="Model ID (for prediction only)."),

        scripts.String(PARAM_HOST, optional=False, grouping="10",
            description="OMERO Server Hostname, eg: omero.mesocentre.uca.fr"),

         scripts.String(PARAM_TIME, optional=False, grouping="11",
            description="Job Time"),
                       

        version = "1.0",
        authors = ["Sami SAFARBATI"],
        institutions = ["GReD"],
        contact = "sami.safarbati@uca.fr",
    ) 
    
    conn = BlitzGateway(client_obj=client)
    session_id = conn._sessionUuid

    # Get user email
    user = conn.getUser()
    email = user.getEmail()
    email = "sami.safarbati@uca.fr"
    print("Email: %s" % email)

    params = {}
    for key in client.getInputKeys():
        if client.getInput(key):
            params[key] = client.getInput(key, unwrap=True)

    modify_action = lambda x: "omero_preprocess_train --action pred" if x == "Prediction" else "omero_preprocess_train --action preprocess_train" if x == "Preprocess & Train" else "omero_preprocess_train --action preprocess" if x == "Autoconfig & Preprocess" else "omero_preprocess_train --action train" if x == "Train with config file" else x

    print("Parameters = %s" % params)

    chosen_action = params[PARAM_ACTION]
    print("Chosen action: %s" % chosen_action)

    biom3d_action =  "{}".format(modify_action(chosen_action))

    print("Running Module : ",biom3d_action)
    print("Current session ID : ", session_id)   

    if chosen_action == "Preprocess & Train" :
        print("Running Preprocess & Train !")
        command = "ssh hpc2 sbatch  -t {0} --mail-user={1} /storage/groups/omero/my-scratch/slurm-scripts/jobs/biom3d.sh {2} --raw {3} --mask {4} --num_classes {5} --num_epochs {6} --desc {7} --hostname {8} --session_id {9}".format(
            params[PARAM_TIME],
            email,
            biom3d_action,
            params[PARAM_IMG_DIR],
            params[PARAM_MSK_DIR],
            params[PARAM_NUM_CLASSES],
            params[PARAM_EPOCHS],
            params[PARAM_DESC],
            params[PARAM_HOST],
            session_id
        )


    elif chosen_action == "Autoconfig & Preprocess" : 
         print("Running Autoconfiguration !")
         command = "ssh hpc2 sbatch -t {0} --mail-user={1} /storage/groups/omero/my-scratch/slurm-scripts/jobs/biom3d.sh {2} --raw {3} --mask {4} --num_classes {5} --num_epochs {6} --desc {7} --hostname {8} --session_id {9} ".format(
            params[PARAM_TIME],
            email,
            biom3d_action,
            params[PARAM_IMG_DIR],
            params[PARAM_MSK_DIR],
            params[PARAM_NUM_CLASSES],
            params[PARAM_EPOCHS],
            params[PARAM_DESC],
            params[PARAM_HOST],
            session_id)
  

    elif chosen_action == "Train" :
         print("Running Training !")
         command = "ssh hpc2 sbatch -t {0} --mail-user={1} /storage/groups/omero/my-scratch/slurm-scripts/jobs/biom3d.sh {2} --raw {3}  --hostname {4} --session_id {5} --config {6} ".format(
            params[PARAM_TIME],
            email,
            biom3d_action,
            params[PARAM_IMG_DIR],
            params[PARAM_HOST],
            session_id,
            params[PARAM_CONFIG])
            
    else:
        print("Running Prediction ! ")      
        command = "ssh hpc2 sbatch -t {0} --mail-user={1} /storage/groups/omero/my-scratch/slurm-scripts/jobs/biom3d.sh {2} --raw {3}  --hostname {4} --session_id {5} --config {6}".format(params[PARAM_TIME],email, biom3d_action, params[PARAM_IMG_DIR], params[PARAM_HOST], session_id, params[PARAM_MODEL])

    msg = os.popen(command).read()
    
    print(msg)
    client.setOutput("Message", rstring("Done."))

    client.closeSession()


if __name__ == "__main__":
    """
    Python entry point
    """
    run_as_script()
    
