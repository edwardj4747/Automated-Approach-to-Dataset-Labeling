from shutil import copyfile
import glob
import os


def cermine_files_to_directory():
    # copy all .cermxml to their own directory
    output_directory = "z_pdfs_to_convert/"
    for file in glob.glob("C:/Users/edwar/Zotero/storage/*/*.pdf"):
        print(file)
        file_name = file.split("\\")[-1]
        copyfile(file, output_directory + file_name)


def cermzone_cleanup():
    success_location_pdf = 'successful_conversions/'
    success_location_cermfiles = 'successful_cermfiles/'

    for file in glob.glob("z_pdfs_to_convert/*.cermzones"):
        base_file_name = file.split("\\")[-1]
        os.replace(file, success_location_cermfiles + base_file_name)

cermzone_cleanup()