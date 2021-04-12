from shutil import copyfile
import glob
import os

'''
    Two useful methods for cermine processing.
        copy_files_to_directory: copies all files from one directory to another directory
        move_cermfiles_to_success_directory: move residual .cermfiles from z_pdfs_to_convert to successful_conversions 
'''

def copy_files_to_directory(file_type=''):
    # copy all .cermxml to their own directory
    output_directory = "z_pdfs_to_convert/"
    # for file in glob.glob("C:/Users/edwar/Zotero/storage/*/*.pdf"):
    for file in glob.glob("C:/Users/edwar/Desktop/Publishing Internship/All Giovanni Papers/*/*.pdf"):
        print(file)
        file_name = file.split("\\")[-2] + file_type
        copyfile(file, output_directory + file_name)


def move_cermfiles_to_success_directory():
    success_location_pdf = 'successful_conversions/'
    success_location_cermfiles = 'successful_cermfiles/'

    for file in glob.glob("aura-omi/z_pdfs_to_convert/*.cermzones"):
        base_file_name = file.split("\\")[-1]
        os.replace(file, success_location_cermfiles + base_file_name)


copy_files_to_directory(file_type='.pdf')