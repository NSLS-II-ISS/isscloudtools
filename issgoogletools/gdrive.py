from googleapiclient.http import MediaFileUpload



def folder_exists_in_root(drive_service, folder_name = ''):
    fid = None
    if folder_name:
        results = drive_service.files().list(
            pageSize=100, q=("mimeType = 'application/vnd.google-apps.folder' "
                             "and 'root' in parents"),
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files',[])
        for item in items:
            if item['name'] == folder_name:
                fid = item['id']
    return fid

def folder_exists(drive_service, parent='', folder_name=''):
    fid = None
    if folder_name:
        results = drive_service.files().list(
            pageSize=100, q=("mimeType = 'application/vnd.google-apps.folder' "
                             "and '{}' in parents".format(parent)),
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files',[])
        for item in items:
            if item['name'] == folder_name:
                fid = item['id']
    return fid

def create_folder(drive_service, parent = '',folder_name = ''):
    if folder_name:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent:
            file_metadata['parents'] = [parent]
        #print(file_metadata)
        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        fid = file.get('id')
        return fid

def upload_file(drive_service, parent = '', file_name='', from_local_file=''):
    file_metadata = {
        'name': file_name,
        'parents': [parent]
    }
    media = MediaFileUpload(from_local_file,
                            mimetype='text/html')

    file_id = drive_service.files().create(body=file_metadata, media_body=media).execute()
    return file_id


