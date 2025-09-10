# OMERO–HPC Integration Scripts

This repository contains the set of **Python scripts** that must be deployed on the **OMERO server** in order to interact with the **HPC environment** for Biom3d used for bio-imaging workflows.  
They handle tasks such as:
- Submitting preprocessing and training jobs to the HPC scheduler (Slurm).
- Managing dataset and project metadata inside OMERO.
- Ensuring results produced on the HPC are stored back into OMERO in a reproducible way.

---

## Dev

- **Sami Safarbati** – Institut de Génétique, Reproduction et Développement (iGReD), UCA, CNRS, Clermont-Ferrand, France; Institut Pascal, UCA, CNRS, Aubière, France.  

- **Pierre Pouchin** – Institut de Génétique, Reproduction et Développement (iGReD), UCA, CNRS, Clermont-Ferrand, France.  




---

## Usage

1. Place the scripts in the appropriate OMERO server directory (typically alongside user scripts in `lib/scripts` or the configured scripts path).
2. Ensure the OMERO server has permission to submit jobs to the HPC (via the dedicated `omero` system user).
3. Configure the HPC job submission settings (`slurm` accounts, GPU access, temporary scratch paths, etc.) according to your environment.
4. From OMERO.web, users can trigger the scripts, which will handle the HPC job lifecycle transparently.

---

## Notes

- All jobs are submitted under the **`omero`** system user on the HPC(for our use case). This ensures consistency regardless of which OMERO user triggers the job.
- The `omero` account must have access to GPU nodes and the correct Slurm accounts configured.
- The code is designed for reproducibility and transparency: all datasets and results are traceable in OMERO.


---
