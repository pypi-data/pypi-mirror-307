def FilePathway(source_folder_path,destination_folder_path,process_type='transfer',head_nfiles=None,tail_nfiles=None,show_status=True):
    """
    Move or copy files from a source folder to a destination folder based on specified criteria.

    Parameters:
    
       * source_folder_path (str): Path to the source folder containing files.
    
       * destination_folder_path (str): Path to the destination folder.
    
       * process_type (str, optional): Process type, either 'transfer' (default) or 'copy'.
    
       * head_nfiles (int, optional): Number of files to process from the start of the list.
    
       * tail_nfiles (int, optional): Number of files to process from the end of the list.
    
       * show_status (bool, optional): If True (default), display status messages after processing.

    
    Returns:
       - str: Confirmation message indicating the directory where files are saved.

    Notes:
       - This function processes files from the source folder based on specified criteria and either moves or copies them to the destination folder.
       - If both 'head_nfiles' and 'tail_nfiles' are provided, files will be processed from the start and end of the list.
       - If 'show_status' is True, success messages are displayed based on the process type.

    Example:
    ```
    FilePathway('/path/to/source', '/path/to/destination', process_type='copy', head_nfiles=5, show_status=True)
    ```
    """
    
    import os
    import shutil
    
    s1=0
    d1=0
    
    new_list=[]
    
    s=source_folder_path
    d=destination_folder_path
    
    os.makedirs(s,exist_ok=True)
    os.makedirs(d,exist_ok=True)
    
    l=os.listdir(s)
    
        
    if head_nfiles == None and tail_nfiles == None:
        for file in l:
            s1=os.path.join(s,file)
            d1=os.path.join(d,file)
            if process_type == 'transfer':
                shutil.move(s1,d1)
                
            elif process_type == 'copy':
                shutil.copy(s1,d1)
                
            elif process_type not in('transfer','copy'):
                raise ValueError("The value of 'process_type' can be ether 'transfer' or 'copy'")
        if show_status == True and process_type == 'transfer':
            print('All the files has been transfered successfully')
        elif show_status == True and process_type == 'copy':
            print('All the files has been copied and pasted successfully')
        
    
    elif head_nfiles != None and tail_nfiles == None:
        for file1 in l[0:head_nfiles]:
            s1=os.path.join(s,file1)
            d1=os.path.join(d,file1)
            if process_type == 'transfer':
                shutil.move(s1,d1)
            elif process_type == 'copy':
                shutil.copy(s1,d1)
            elif process_type not in('transfer','copy'):
                raise ValueError("The value of 'process_type' can be ether 'transfer' or 'copy'")
        if show_status == True and process_type == 'transfer':
                    print('First ',head_nfiles,' files has been transfered successfully')
        elif show_status == True and process_type == 'copy':
                    print('First ',head_nfiles,' files has been copied and pasted successfully')
    
    elif head_nfiles == None and tail_nfiles != None:
        for file2 in l[-tail_nfiles:]:
            s1=os.path.join(s,file2)
            d1=os.path.join(d,file2)
            if process_type == 'transfer':
                shutil.move(s1,d1)
            elif process_type == 'copy':
                shutil.copy(s1,d1)
            elif process_type not in('transfer','copy'):
                raise ValueError("The value of 'process_type' can be ether 'transfer' or 'copy'")
            
        if show_status == True and process_type == 'transfer':
            print('Last ',tail_nfiles,' files has been transfered successfully')
        elif show_status == True and process_type == 'copy':
            print('Last ',tail_nfiles,' files has been copied and pasted successfully')
    
    elif head_nfiles != None and tail_nfiles != None:
        for f in l[0:head_nfiles]:
            new_list.append(f)
        for f1 in l[-tail_nfiles:]:
            new_list.append(f1)
        for file3 in new_list:
            s1=os.path.join(s,file3)
            d1=os.path.join(d,file3)
            if process_type == 'transfer':
                shutil.move(s1,d1)
            elif process_type == 'copy':
                shutil.copy(s1,d1)
            elif process_type not in('transfer','copy'):
                raise ValueError("The value of 'process_type' can be ether 'transfer' or 'copy'")
        if show_status == True and process_type == 'transfer':
            print('First '+str(head_nfiles),' and last '+str(tail_nfiles),' files has been transfered successfully')
        elif show_status == True and process_type == 'copy':
            print('First '+str(head_nfiles),' and last '+str(tail_nfiles),' files has been copied and pasted successfully')
            print()
    return  'All files saved to ',s,' directory'