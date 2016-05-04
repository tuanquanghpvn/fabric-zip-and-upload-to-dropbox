from fabric.api import run, env, local, cd
from fabric.contrib.files import exists

# Include the Dropbox SDK
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import sys
import dropbox


#####################################################################################################
#####################################################################################################
#####################################################################################################

# Info SSH
env.hosts = ["truong.tuan.quang@127.0.0.1"]
env.key_filename = ["~/.ssh/id_rsa.pem"]
# env.passwords = {'truong.tuan.quang@127.0.0.1:22': 'your-password-here'}

# Config dropbox api
# Add OAuth2 access token here. 
# You can generate one for yourself in the App Console.
# See <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>
env["token"] = "your-token-here"

# Config Task
env["code_dir"] = "Documents/Python" # Root folder

# Config zip folder or file
env["folder_name"] = "images/" # Name folder you want to zip

# Config upload file to dropbox
env["local_file"] = "images.tar.gz" # Name local file you want to upload
env["upload_file"] = "/my-file-backup.tar.gz" # Name file upload and save to dropbox


#####################################################################################################
#####################################################################################################
#####################################################################################################

# Function fabric

def test():
    run("uname -s")

def zip_code():
    with cd(env["code_dir"]):
        if exists(env["folder_name"], use_sudo=True):
            cmd = "tar -cvf {0} {1}".format(env["local_file"], env["folder_name"])
            result = run(cmd)
            if result.return_code == 0:
                print "Zip complete!"
            else:
                sys.exit(result) # print error
        else:
            sys.exit("Not found folder images!")


def upload_to_dropbox():
    with cd(env["code_dir"]):
        if exists(env["local_file"], use_sudo=True):
            _dropbox_api()
        else:
            sys.exit("Not found file name {0}".format(env["local_file"]))


#####################################################################################################
#####################################################################################################
#####################################################################################################
# Function upload file to dropbox
def _dropbox_api():
    LOCALFILE = env["local_file"]
    BACKUPPATH = env["upload_file"]
    TOKEN = env["token"]
    
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(TOKEN)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    with open(LOCALFILE, 'r') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f, BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
