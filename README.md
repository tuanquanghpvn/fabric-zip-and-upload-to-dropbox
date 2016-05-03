# fabric-zip-and-upload-to-dropbox
Fabric Auto Zip File Or Folder And Upload To Dropbox

### 1. Install dropbox api

pip install dropbox

### 2. Set token dropbox

env["token"] = "your-token-here"

### 3. Auto zip and upload to dropbox

run command: fab zip_code upload_to_dropbox

### 4. If you don't want zip code

Set env["zip_complete"] = True

run command: fab upload_top_dropbox
