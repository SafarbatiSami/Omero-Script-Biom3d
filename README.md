# OMERO–HPC Integration Scripts for Biom3d
  
This repository contains the set of **Python scripts** that must be deployed on the **OMERO server** in order to interact with the **HPC environment** for Biom3d bio-imaging workflows.  
They handle tasks such as:  
- Submitting preprocessing, training, and prediction jobs to the HPC scheduler (Slurm).  
- Managing dataset and project metadata inside OMERO.  
- The workflow ensure results produced on the HPC are stored back into OMERO in a reproducible and traceable way.  
  
---  
  
## Developers  
  
- **Sami Safarbati** – Institut de Génétique, Reproduction et Développement (iGReD), UCA, CNRS, Clermont-Ferrand, France; Institut Pascal, UCA, CNRS, Aubière, France.  
- **Pierre Pouchin** – Institut de Génétique, Reproduction et Développement (iGReD), UCA, CNRS, Clermont-Ferrand, France.  
  

---  
  
## Singularity Image  
  
The HPC jobs run inside a **Singularity image** built directly from a Docker image hosted on **DockerHub**.  
There is no `Dockerfile` or recipe in this repository, because the image is pulled manually:  
  
```bash  
 singularirty build biom3d_mg.sif docker://gumougeot/biom3d:v0.1.1-x86_64-torch2.3.1-cuda11.8-cudnn8
```
The resulting .sif file (e.g. biom3d.sif) is then used by the Slurm job script (biom3d.sh).  
  
⚠️ In the current configuration, the image path is defined as:  
  
**/storage/groups/omero/my-scratch/singularity\_images/workflows/biom3d/biom3d.sif**  
- This path is specific to the Mésocentre cluster. For portability, you should adapt this path to your HPC environment or make it configurable (via environment variable or script argument).  

---
## OMERO Interface Scripts  
  
- Two Python scripts in this repository **Biom3d.py** and **Biom3d-config.py** are OMERO interface scripts.  
  
- They must be stored on the OMERO server in the scripts directory (e.g. OMERO.server/lib/scripts/).  
  
- They appear in OMERO.web and allow users to launch Biom3d jobs on the HPC directly from the OMERO interface.  
  
- They act as the bridge between OMERO and the HPC job submission.  

---  

## Usage  
  

1.  **Deploy OMERO scripts**
-  Copy Biom3d.py and Biom3d-config.py into the OMERO server scripts directory (e.g. lib/scripts).
2.  **Prepare Singularity image**
- On the HPC cluster, pull the Docker image with Singularity and store it in the path expected by biom3d.sh (or adapt the script).
3.  Configure HPC job submission
- Ensure the OMERO system user (omero) can submit Slurm jobs.
4.  Grant access to GPU nodes if required.
5.  Adapt job time, account settings, and scratch paths according to your environment.
6.  Trigger jobs from OMERO.web
-  Users select images/datasets in OMERO.web, choose the Biom3d script, and parameters.
- The OMERO script submits the corresponding Slurm job, which runs Biom3d inside the Singularity container.

---

**Notes**  
  

*   All jobs are submitted under the omero system user on the HPC (for our setup). This ensures consistency regardless of which OMERO user triggers the job.
*   The current biom3d.sh contains cluster-specific paths. For reusability, adapt them to your environment or generalize with variables.
*   The system is designed for reproducibility: all datasets, jobs, and outputs remain linked to OMERO objects.