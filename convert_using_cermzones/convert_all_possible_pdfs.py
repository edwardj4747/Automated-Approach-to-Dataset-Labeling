import os
import glob

command = 'java -cp cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path z_pdfs_to_convert -outputs zones 1>> a.txt 2> b.txt'

failed_conversions_location = 'failed_conversions/'
success_location_pdf = 'successful_conversions/'
success_location_cermfiles = 'successful_cermfiles/'

if os.path.exists('a.txt'):
    os.remove('a.txt')
    os.remove('b.txt')

keep_looping = True

while keep_looping:
    keep_looping = False

    os.system(command)
    # keep track of successful and unsuccessful conversions
    success = []
    failures = []

    with open('a.txt') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # print("i, ", index, " l ", line)

            if line.startswith("File processed"):
                file = line.split("File processed: ")[-1].replace("\n", '')
                if index == len(lines) - 1 or not lines[index + 1].startswith("Extraction time"):
                    print("failed_conversions on file ", file)
                    # failed conversion on file z_pdfs_to_convert\Luo et al. - 2017 - A Case Study of Mass Transport during the East-Wes.pdf

                    base_file_name = file.split("\\")[-1]
                    # move failed file to failed_conversions
                    os.replace(file, failed_conversions_location + base_file_name)

                    # make sure we run the whole process again
                    keep_looping = True
                    break
                else:
                    success.append(file)

    print(success)

    for file in success:
        base_file_name = file.split("\\")[-1]

        # move pdf to successful conversions
        os.replace(file, success_location_pdf + base_file_name)

        # move cermzone file to successful_cermfiles
        cermfile_name = file.replace(".pdf", ".cermzones")
        os.replace(cermfile_name, success_location_cermfiles + base_file_name.replace(".pdf", ".cermzones"))

    os.remove('a.txt')
    os.remove('b.txt')

# if we ended on a success there will still be files in z_pdfs_to_convert, so move those to correct directories now
for file in glob.glob('z_pdfs_to_convert/*.pdf'):
    base_file_name = file.split("\\")[-1]
    os.replace(file, success_location_pdf + base_file_name)

for file in glob.glob("z_pdfs_to_convert/*.cermzones"):
    base_file_name = file.split("\\")[-1]
    os.replace(file, success_location_cermfiles + base_file_name)
