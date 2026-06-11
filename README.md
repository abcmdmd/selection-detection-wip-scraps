# selection-detection-wip-scraps
sharing code while selection detection pipeline still in progress

### WIP protocol here:
https://docs.google.com/document/d/1p9DrWMMd1rcXhPKDfKtaoyxyQ1nTxjexktIIJTDnMsA/edit?tab=t.0#heading=h.3tus0apyit49

### Notes: 
- It is assumed that you're running this on the UR cluster, with access to Mel's /data folder. 

### How to use/grab a file: 
** Step 1: **
Run this command to download all of the necessary helper functions into your current working directory. 
These helper functions will come in the format of "pipeline_settings.py"

For a command in **.ipynb**:

	! wget -q -nc https://raw.githubusercontent.com/abcmdmd/selection-detection-wip-scraps/refs/heads/main/pipeline_settings.py


For a command in **terminal**:

	wget -q -nc https://raw.githubusercontent.com/abcmdmd/selection-detection-wip-scraps/main/pipeline_settings.py

** Step 2: **
Do the same for the requisite "worldwide_populations_inputfile.tsv". 

For a command in **.ipynb**:

	! wget -q -nc https://raw.githubusercontent.com/abcmdmd/selection-detection-wip-scraps/refs/heads/main/worldwide_populations_inputfile.tsv


For a command in **terminal**:

	wget -q -nc https://raw.githubusercontent.com/abcmdmd/selection-detection-wip-scraps/main/worldwide_populations_inputfile.tsv

** Step 3: **
Do the same for the specific file you're running. 

For a command in **.ipynb**:

	! wget -q -nc https://raw.githubusercontent.com/abcmdmd/selection-detection-wip-scraps/refs/heads/main/[[file]]


For a command in **terminal**:

	wget -q -nc https://raw.githubusercontent.com/abcmdmd/selection-detection-wip-scraps/main/[[file]]	
