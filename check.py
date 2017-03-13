import exiftool
import os
import argparse
import yaml

parser = argparse.ArgumentParser(description='Enter Your File Path')
parser.add_argument("-p", "--path", dest="path", help="Specify the path to your files", required=True)
parser.add_argument("-s", "--standard", dest="standard", help="Specify the standard to test against as defined in YAML "
                                                              "file.", required=True)

args = parser.parse_args()
path = args.path
utk_standard = args.standard
affected_files = {}
settings = yaml.load(open('standards.yaml', 'r'))
definitions = yaml.load(open('definitions.yaml', 'r'))
output_file = open('bad_files.txt', 'w')


def choose_files():
    for x in os.walk(path):
        new_path = x[0] + '/'
        for y in x:
            if isinstance(y, list) and len(y) >= 1:
                exif_data = bundle_file_data(y, new_path)
                return exif_data


def bundle_file_data(files, p):
    file_paths = []
    for item in files:
        file_paths.append(p + item)
    all_exif_data = read_exif(file_paths)
    write_exif_to_file(all_exif_data)
    return all_exif_data


def check_standard(x, standard_to_check):
    for data in x:
        good_check = []
        for okay in settings[int(utk_standard)][standard_to_check]:
            checked_standard = []
            for test_standard in definitions[standard_to_check][okay]:
                if test_standard in data:
                    checked_standard.append('{0}'.format(test_standard))
                    for q in definitions[standard_to_check][okay][test_standard]:
                        if data[test_standard] == q:
                            good_check.append("{0} - {1}".format(test_standard, data[test_standard]))
        if len(good_check) == 0:
            populate_affected_files(data['File:FileName'], standard_to_check)


def populate_affected_files(filename, standard):
    new_key = filename
    new_value = '{0} does not match standard.'.format(standard)
    if new_key in affected_files:
        affected_files[new_key].append(new_value)
    else:
        affected_files[new_key] = []
        affected_files[new_key].append(new_value)


def read_exif(x):
    try:
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata_batch(x)
        return metadata
    except:
        print("Could not read exif data.")
        pass


def write_exif_to_file(x):
    # This is here for testing only.  This function and it call can be removed once "complete."
    new_file = open('metadata.txt', 'w')
    new_file.write(str(x))
    new_file.close()


def append_file(file):
    output_file.write(file + '\n')


def print_dictionary(x):
    output_header = "Reviewing standards based on the following" \
                    " category:\n\t{0}\n\n---\n".format(settings[int(utk_standard)]['Title'][0])
    append_file(output_header)
    print("\tFound {0} files with problems. See badfiles.txt for more information.".format(len(x)))
    processed = 1
    for key, value in x.items():
        problems = ""
        for x in value:
            problems += "\n\t* {0}".format(x)
        problem = "{2}. {0}: {1}".format(key, problems, processed)
        append_file(problem)
        processed += 1


if __name__ == "__main__":
    print("Grabbing Exif Data \n")
    all_exif = choose_files()
    print("Checking Colorspace \n")
    check_standard(all_exif, "Colorspace")
    print("Checking File Format \n")
    check_standard(all_exif, "File_format")
    print("Checking Bit depth \n")
    check_standard(all_exif, "Bit_depth")
    print("Checking pixel dimensions\n")
    check_standard(all_exif, "Pixel_dimensions")
    if utk_standard == "8":
        check_standard(all_exif, "Long_side")
    print_dictionary(affected_files)
