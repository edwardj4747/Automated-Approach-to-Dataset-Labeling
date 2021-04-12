import os

new_cermzone_directories = ['failed_conversions', 'preprocessed', 'successful_cermfiles', 'successful_conversions', 'text', 'z_pdfs_to_convert']

for folder in new_cermzone_directories:
    os.makedirs(folder)