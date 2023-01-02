import sys
import struct

def read_config():
    global chants_start_address, chants_table_size, chants_data_size
    # we use try and except it will try to do the stuff inside this block, if it fails we return a message with the error and false
    try:
        # first we try to open the file
        config_file = open(config_filename, "r")

        # now we iterate on each line
        for line in config_file.readlines():
            # if the line start with our key work and it contains 2 values returned by split then we continue
            if line.startswith("start.address") and len(line.split("=")) == 2:
                # here we take the part after the = and use strip to remove spaces, then we use int to convert into a number
                # because all data read from a text file is consider a text
                chants_start_address = int(line.split("=")[1].strip())
                continue
            elif line.startswith("table.size") and len(line.split("=")) == 2:
                chants_table_size = int(line.split("=")[1].strip())
                continue
            elif line.startswith("data.size") and len(line.split("=")) == 2:
                chants_data_size = int(line.split("=")[1].strip())
                continue
        # and now we close the file! always important to do it!
        config_file.close()
        return True
    except Exception as e:
        input("Error while reading %s, code error: %s\nPress enter to continue" % (config_filename, e))
        return False


def get_afs_name_by_id(idx: int):
    return AFS_NAMES[idx]


def read_chants():
    global slxx_filename, chants_start_address, total_teams, chants_data_size
    try:
        slxx_file = open(slxx_filename, "rb")
        slxx_file.seek(chants_start_address, 0)
        chants_list = []
        for team_id in range(0, total_teams, 1):
            offset = slxx_file.tell()
            file_id, afs_id = struct.unpack(
                "<2H", slxx_file.read(chants_data_size))
            chants_list.append([team_id, file_id, get_afs_name_by_id(afs_id), offset])
        slxx_file.close()
        return chants_list
    except Exception as e:
        input("Error while reading %s, code error: %s\nPress enter to continue" % (slxx_filename, e))
        return []

def calculate_offset(team_idx:int):
    return chants_start_address + team_idx * chants_data_size

def export_to_csv(chants:list):
    try:
        csv_file = open("chants_export.csv", "w")
        csv_file.write(",".join(str(header) for header in CSV_HEADERS) + "\n")
        for chant in chants:
            csv_file.write(",".join(str(data) for data in chant) + "\n")
        csv_file.close()
    except Exception as e:
        input("Error while creating csv_file code error: %s\nPress enter to continue" % (e))

def import_from_csv(csv_filename):
    try:
        csv_file = open(csv_filename, "r")
        slxx_file = open(slxx_filename, "r+b")
        for i, line in enumerate(csv_file.readlines()):
            if i == 0: continue # here we skip the headers
            if len(line.split(","))!=4:
                print("error while reading line %d, less data provided" % i)
            team_id, file_id, afs_name, offset = line.split(",")
            team_id = int(team_id)
            file_id = int(file_id)
            afs_id = AFS_NAMES.index(afs_name)
            offset = int(offset) 
            if calculate_offset(team_id) == offset:
                offset = offset
            else:
                offset = calculate_offset(team_id)
            slxx_file.seek(offset, 0)
            slxx_file.write(struct.pack("<2H", file_id, afs_id))
        csv_file.close()
        slxx_file.close()
    except Exception as e:
        input("Error while import %s code error: %s\nPress enter to continue" % (csv_filename, e))

def main():
    global total_teams, slxx_filename
    # first thing we do is try to read the config file if we don't found it then we exit the program
    if not read_config(): sys.exit()
    total_teams = int(chants_table_size/chants_data_size)
    # now we ask the user for the slxx file to be read
    slxx_filename = input("Please write the name of your SLXX file and press enter: ")
    
    option_selected = int(input("Select one of the options below\n1 - Export chants to csv\n2 - Import chants from csv\n"))
    
    if 1 > option_selected > 2:
        input("Option selected is out of range")
        sys.exit()
    
    if option_selected == 1:
        chants_list = read_chants()
        if chants_list == []:
            sys.exit()
        export_to_csv(chants_list)
        input("chants exported successfully press enter to exit")
    elif option_selected == 2:
        csv_filename = input("Please write the name of your csv file and press enter: ")
        import_from_csv(csv_filename)
        input("chants imported successfully press enter to exit")

if __name__=="__main__":
    AFS_NAMES = [
        "0_SOUND.AFS",
        "0_TEXT.AFS",
        "X_SOUND.AFS",
        "X_TEXT.AFS",
        ]
    CSV_HEADERS = [
        "TEAM ID",
        "FILE ID",
        "AFS FILE",
        "OFFSET",
        ]

    # declaration of global variables, those who are gonna be use along the whole program
    config_filename = "config.txt"
    chants_start_address = 0
    chants_table_size = 0
    chants_data_size = 0
    total_teams = 0
    slxx_filename = ""
    
    # after the declarations we start the main function
    main()