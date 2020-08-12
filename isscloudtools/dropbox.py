import os



def dropbox_folder_exists(service, folder):
    try:
        service.files_get_metadata(folder)
        return True
    except:
        return False

def dropbox_upload_files(service, origin, dropbox_folder, destination):
    with open(origin,"rb") as f:
        return service.files_upload(f.read(),f'{dropbox_folder}{destination}')

def dropbox_get_shared_link(service,object):
    link = service.sharing_create_shared_link(object)
    return link.url

def dropbox_create_folder(service, dropbox_folder):
   return service.files_create_folder(dropbox_folder)





