from registrationLogic import user

def upload_file(user_id, file_name, file_path):
    result = True
    user_file = { "user": user_id, "file_name": file_name, "file_path": file_path }
    files_table = user.connect_to_mongodb("files")
    if files_table.find_one({"user": user_id, "file_name": file_name}) is None:
        files_table.insert_one(user_file)
    else:
        result = False
        
    return result
    
def delete_file(user_id, file_name):
    user_file = { "user": user_id, "file_name": file_name }
    files_table = user.connect_to_mongodb("files")
    files_table.delete_one(user_file)
    return True
    
def list_files(user_id):
    files_table = user.connect_to_mongodb("files")
    files = files_table.find({"user" : user_id})
    return [x["file_name"] for x in files]
    
def get_filepath(user_id, file_name):
    user_file = { "user": user_id, "file_name": file_name }
    files_table = user.connect_to_mongodb("files")
    full_user_file = files_table.find_one(user_file)
    return full_user_file["file_path"]