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
output_file = open('badfiles.txt', 'w')


def choose_files():
    for x in os.walk(path):
        new_path = x[0] + '/'
        for y in x:
            if isinstance(y, (list)) and len(y) >= 1:
                files = []
                for item in y:
                    files.append(new_path + item)
                all_exif = read_exif(files)
                write_exif_to_file(all_exif)
                check_standard(all_exif, "Colorspace")
                check_standard(all_exif, "File_format")
    print_dictionary(affected_files)


def check_color_space(x):
    # processed = 0
    for data in x:
        print("Checking {0}'s colorspace.".format(data['File:FileName']))
        good_colorspace = []
        for okay in settings[int(utk_standard)]['Colorspace']:
            checked_standard = []
            for test_standard in definitions['Colorspace'][okay]:
                if test_standard in data:
                    checked_standard.append('{0}'.format(test_standard))
                    if data[test_standard] == definitions['Colorspace'][okay][test_standard][0]:
                        good_colorspace.append("{0} - {1}".format(test_standard, data[test_standard]))
        if len(good_colorspace) == 0:
            print("\t{0} failed colorspace check.".format(data['File:FileName']))
            new_key = data['File:FileName']
            new_value = 'Colorspace does not match standard.'
            if new_key in affected_files:
                affected_files[new_key].append(new_value)
            else:
                affected_files[new_key] = []
                affected_files[new_key].append(new_value)


def check_standard(x, standard_to_check):
    # processed = 0
    for data in x:
        print("Checking {0}'s {1}.".format(data['File:FileName'], standard_to_check.lower()))
        good_check = []
        for okay in settings[int(utk_standard)][standard_to_check]:
            checked_standard = []
            for test_standard in definitions[standard_to_check][okay]:
                if test_standard in data:
                    checked_standard.append('{0}'.format(test_standard))
                    if data[test_standard] == definitions[standard_to_check][okay][test_standard][0]:
                        good_check.append("{0} - {1}".format(test_standard, data[test_standard]))
        if len(good_check) == 0:
            print("\t{0} failed {1} check.".format(data['File:FileName'], standard_to_check.lower()))
            new_key = data['File:FileName']
            new_value = '{0} does not match standard.'.format(standard_to_check)
            "test".lower()
            if new_key in affected_files:
                affected_files[new_key].append(new_value)
            else:
                affected_files[new_key] = []
                affected_files[new_key].append(new_value)


# def check_bit_depth_level(x):
#     for data in x:
#         return


def read_exif(x):
    try:
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata_batch(x)
        return(metadata)
    except:
        pass


def write_exif_to_file(x):
    # This is here for testing only.  This function and it call can be removed once "complete."
    new_file = open('metadata.txt', 'w')
    new_file.write(str(x))
    new_file.close()


def check_file_formats(x):
    for data in x:
        print("Checking {0}'s file format.".format(data['File:FileName']))
        good_check = []
        for okay in settings[int(utk_standard)]['File_format']:
            checked_standard = []
            for test_standard in definitions['File_format'][okay]:
                if test_standard in data:
                    checked_standard.append('{0}'.format(test_standard))
                    if data[test_standard] == definitions['File_format'][okay][test_standard][0]:
                        good_check.append("{0} - {1}".format(test_standard, data[test_standard]))
        if len(good_check) == 0:
            print("\t{0} failed file format check.".format(data['File:FileName']))
            new_key = data['File:FileName']
            new_value = 'File format does not match standard.'
            # new_key = data['File:FileName']
            # new_value = 'File format does not match standard.'
            if new_key in affected_files:
                affected_files[new_key].append(new_value)
            else:
                affected_files[new_key] = []
                affected_files[new_key].append(new_value)

# def grab_mime_types(x):
#     file_types = {}
#     for item in x:
#         mimetypes.types_map[item]


def append_file(file):
    output_file.write(file + '\n')


def print_dictionary(x):
    print(x)
    for key, value in x.items():
        problems = ""
        for x in value:
            problems += "\n\t{0}".format(x)
        problem = "{0}: {1}".format(key, problems)
        append_file(problem)


if __name__ == "__main__":
    choose_files()