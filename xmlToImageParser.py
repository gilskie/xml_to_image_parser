import sys
import configparser
import os
import xml.dom.minidom
import logging
import time


def main():
    config = configparser.ConfigParser()

    #config_location = sys.path[0] + '\configuration.ini'
    config_location = sys.executable.replace('xmlToImageParser.exe', 'configuration.ini')
    config.read(config_location)

    default_setting = config["DEFAULT"]
    input_folder_location = default_setting["input_folder_location"]
    log_file_location = default_setting["log_file_location"]
    # print(f"Info: Image location = {input_folder_location}")
    read_directory(input_folder_location, log_file_location)


def read_directory(input_folder_location, log_file_location):

    if os.path.isdir(input_folder_location):
        print("Info: Directory found! Processing...")

        folder_lists = os.listdir(input_folder_location)
        gather_xml_for_validation(input_folder_location, folder_lists, log_file_location)

    else:
        print("Error: Directory doesnt exists!")


def gather_xml_for_validation(input_folder_location, folder_lists, log_file_location):
    print(f"Info: folders inside = {len(folder_lists)}, {os.listdir(os.path.join(input_folder_location, folder_lists[0]))}")

    try:
        for folder in folder_lists:
            folder_location = os.path.join(input_folder_location, folder)
            get_image_and_xml = os.listdir(folder_location)

            xml_file_match = [s for s in get_image_and_xml if ".XML" in s]
            image_file_match = [s for s in get_image_and_xml if "Images" in s]

            if len(xml_file_match) > 1 or len(image_file_match) > 1:
                print(f"Error: Single .XML/Image must be provided only for {folder}!")
            else:
                xml_file_location = os.path.join(folder_location, xml_file_match[0])
                image_directory_location = os.path.join(folder_location, image_file_match[0])

                print(f"Info: location of xml = {xml_file_location},"
                      f"\r\nlocation of image = {image_directory_location}")

                doc = xml.dom.minidom.parse(xml_file_location)
                image_list = doc.getElementsByTagName("image")

                image_file_lists = os.listdir(image_directory_location)

                image_matched = []
                image_unmatched = []

                # print("Info: Extracted src attribute value from <image>:", end='')
                for image in image_list:
                    # print(image.getAttribute("src"), end=', ')
                    src_value = image.getAttribute("src")
                    if src_value in image_file_lists:
                        image_matched.append(src_value)
                    else:
                        image_unmatched.append(src_value)

                # print(f"\r\nInfo: Extracted image file from directory {image_directory_location}: {image_file_lists}")
                print(f"Info: matched = {image_matched} \r\nUnmatched = {image_unmatched}")
                print(f"Info: Done generating log file at {log_file_location}")
                logging.basicConfig(filename=log_file_location + '\\System.log',
                                    filemode='w',
                                    format='%(name)s - %(levelname)s - %(message)s')
                logging.warning(f"Jobname = {folder} | Match found {image_matched}, Unmatched = {image_unmatched}")
                time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)


main()
