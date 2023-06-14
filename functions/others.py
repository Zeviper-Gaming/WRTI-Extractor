import shutil

def name_cfg_from_url(url):
    filename = url.split("/")[-1]
    filename = filename.lower()
    filename = filename.replace(".", "")
    filename = filename.replace("-", "_")
    filename += ".cfg"
    return filename

def copy_cfg_file_as(target_name,destination=""):
    shutil.copy("custom.cfg",f"{destination}/{target_name}")