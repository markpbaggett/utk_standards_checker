import exiftool
import os
import argparse
import mimetypes
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
                    print(new_path + item)
                all_exif = read_exif(files)
                write_exif_to_file(all_exif)
                # all_mimes = grab_mime_types(files)
                check_color_space(all_exif)
    print_dictionary(affected_files)

def check_color_space(x):
    processed = 0
    for data in x:
        # print("Processing {0}".format(data['File:FileName']))
        # print("\t{0}".format(data))
        good_colorspace = []
        for okay in settings[int(utk_standard)]['Colorspace']:
            checked_standard = []
            # print("\t\tLooking at {0}.".format(okay))
            for test_standard in definitions['Colorspace'][okay]:
                if test_standard in data:
                    checked_standard.append('{0}'.format(test_standard))
                    # print("{0}: {1}".format(test_standard,data[test_standard]))
                    if data[test_standard] == definitions['Colorspace'][okay][test_standard][0]:
                        good_colorspace.append("{0} - {1}".format(test_standard, data[test_standard]))
            # print(str(checked_standard))
        print("{0}: {1}".format(data['File:FileName'], good_colorspace))
        if len(good_colorspace) == 0:
            new_key = data['File:FileName']
            new_value = 'Colorspace does not match standard.'
            affected_files[new_key] = new_value
            # print("{0} does not meet colorspace requirements.".format(data['File:FileName']))
                        # print("\t\t\t{0}: {1}".format(test_standard, data[test_standard]))
            #         if test_standard not in settings[int(utk_standard)]['Colorspace']:
            #             print(test_standard)
            #             # print("\t{0} is in the while.".format(data['File:FileName']))
            #             new_key = data['File:FileName']
            #             new_value = 'Colorspace is wrong: {0}'.format(test_standard)
            #             # print("{0} -- {1}".format(new_key, new_value))
            #             affected_files[new_key] = new_value
        # if 'ICC_Profile:ProfileDescription' in data:
        #     print(data['ICC_Profile:ProfileDescription'])
        #     print(settings[int(utk_standard)]['Colorspace'])
        #     if data['ICC_Profile:ProfileDescription'] not in settings[int(utk_standard)]['Colorspace']:
        #         # print("\t{0} is in the while.".format(data['File:FileName']))
        #         new_key = data['File:FileName']
        #         new_value = 'Colorspace is wrong: {0}'.format(data['ICC_Profile:ProfileDescription'])
        #         print("{0} -- {1}".format(new_key, new_value))
        #         affected_files[new_key] = new_value
        # else:
        #     new_key = str(data['File:FileName'])
        #     new_value = 'Missing colorspace!'
        #     affected_files[new_key] = new_value
        # processed += 1


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


def grab_mime_types(x):
    file_types = {}
    for item in x:
        mimetypes.types_map[item]


def append_file(file):
    output_file.write(file + '\n')


def print_dictionary(x):
    print(x)
    for key, value in x.items():
        problem = "{0}: {1}".format(key, value)
        append_file(problem)


if __name__ == "__main__":
    choose_files()