import argparse
import os
import glob
from dat import DatFileReader, DatFileWriter

def convert_file(file_path, to_csv, encoding, string_format, target_extension):
    if to_csv:
        file_reader = DatFileReader(file_path, encoding=encoding, string_format=string_format)
        file_reader.export_to_csv()
    else:
        file_writer = DatFileWriter(file_path, encoding=encoding, string_format=string_format)
        file_writer.dat_file_path = os.path.splitext(file_path)[0] + target_extension
        file_writer.write_file()

def main():
    parser = argparse.ArgumentParser(description="Convert between CSV and Dat/Datu8 file formats.")
    parser.add_argument('path', help="The path to the input file or folder.")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--to-csv', action='store_true', help="Convert Dat/Datu8 to CSV.")
    group.add_argument('-b', '--to-binary', action='store_true', help="Convert CSV to Dat/Datu8.")
    
    parser.add_argument('-p', '--preset', choices=['dat', 'datu8', 'dat_new'], required=True, 
                        help="Preset settings for dat, datu8, or dat_new(After Aquarium PC) files.")

    args = parser.parse_args()
    path = args.path

    # Set defaults based on preset
    if args.preset == 'dat':
        encoding = 'shift-jis'
        string_format = 'nt'
        target_extension = '.dat'
    elif args.preset == 'datu8':
        encoding = 'utf-8'
        string_format = 'len_prefixed_nt'
        target_extension = '.datu8'
    elif args.preset == 'dat_new':
        encoding = 'utf-8'
        string_format = 'nt'
        target_extension = '.dat'

    if os.path.isfile(path):
        # Single file conversion
        file_extension = os.path.splitext(path)[1].lower()
        if args.to_csv and file_extension != target_extension:
            print(f"Error: -c/--to-csv requires a {target_extension} file as input.")
            return
        elif args.to_binary and file_extension != '.csv':
            print("Error: -b/--to-binary requires a .csv file as input.")
            return

        convert_file(path, args.to_csv, encoding, string_format, target_extension)

    elif os.path.isdir(path):
        # Folder conversion
        if args.to_csv:
            files = glob.glob(os.path.join(path, f'*{target_extension}'))
        elif args.to_binary:
            files = glob.glob(os.path.join(path, '*.csv'))

        if not files:
            print(f"No files found in the directory: {path}")
            return

        for file in files:
            convert_file(file, args.to_csv, encoding, string_format, target_extension)
    else:
        print("Error: The specified path is neither a file nor a folder.")

if __name__ == "__main__":
    main()