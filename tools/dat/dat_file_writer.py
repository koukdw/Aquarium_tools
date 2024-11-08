import csv
import os
from . import ByteArrayHelper

class DatFileWriter(ByteArrayHelper):
    def __init__(self, file_path, encoding='utf-8', string_format='len_prefixed_nt'):
        super().__init__()
        self.file_path = file_path
        self.encoding = encoding
        self.string_format = string_format
        self.dat_file_path = os.path.splitext(file_path)[0] + '.datu8'  # Default extension

    def write_file(self):
        with open(self.file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the headers
            element_count = len(headers)
            self.write_u32(element_count)

            # Determine types from headers
            type_mapping = {
                'String': 1,
                'Int32': 2,
                'Int8': 3,
                'Int64': 4,
                'Int16': 5,
                'StringKey': 6
            }
            types = [type_mapping[header] for header in headers]
            for type_code in types:
                self.write_u32(type_code)

            # Read the rows and write the elements
            for row in reader:
                for value, type_code in zip(row, types):
                    if type_code == 1 or type_code == 6:
                        if self.string_format == 'len_prefixed_nt':
                            self.write_len_prefixed_nt_str(value, encoding=self.encoding)
                        elif self.string_format == 'nt':
                            self.write_nt_str(value, encoding=self.encoding)
                    elif type_code == 2:
                        self.write_i32(int(value))
                    elif type_code == 3:
                        self.write_i8(int(value))
                    elif type_code == 4:
                        self.write_i64(int(value))
                    elif type_code == 5:
                        self.write_i16(int(value))
                    else:
                        raise ValueError(f"Unknown type code: {type_code}")

        with open(self.dat_file_path, 'wb') as datfile:
            datfile.write(self.get_data())