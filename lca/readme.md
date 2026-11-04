# LCA Project: Li-ion Battery Recycling (Hydrometallurgical)

## Overview
This Brightway2 project contains:
- **LCI**: Life Cycle Inventory of a simulated hydrometallurgical Li-ion battery (LiB) recycling model.
- **LCIA Methods**: Custom **Cumulative Exergy Dissipation** methods (internal/external) for resource assessment.
- **Biosphere**: Own biosphere flows for exergy-based indicators.

---

## Setup
1. **Load the Project**:
   Restore the Brightway2 backup (e.g., `brightway2-project-RA_ei-3.12-backup20-May-2026-10-22AM.tar.gz`) using:
   ```python
   import bw2io as bi
   bi.backup.restore_project_directory(fp="<backup_path>", project_name="RA_ei-3.12")