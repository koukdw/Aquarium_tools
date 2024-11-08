import csv
import os
from . import ByteArrayHelper

class DatFileReader(ByteArrayHelper):
    def __init__(self, file_path, encoding='utf-8', string_format='len_prefixed_nt'):
        super().__init__()
        self.file_path = file_path
        self.encoding = encoding
        self.string_format = string_format
        self.csv_file_path = os.path.splitext(self.file_path)[0] + '.csv'

    def read_header(self):
        self.element_count = self.read_u32()
        # print(f"Element Count: {self.element_count}")

    def read_types(self):
        self.types = []
        for _ in range(self.element_count):
            type_code = self.read_u32()
            self.types.append(type_code)
        # print(f"Types: {self.types}")

    def read_elements(self):
        elements = []
        while self.tell() < len(self.get_data()):
            row = []
            for type_code in self.types:
                if type_code == 1:
                    if self.string_format == 'len_prefixed_nt':
                        value = self.read_len_prefixed_nt_str(encoding=self.encoding)
                    elif self.string_format == 'nt':
                        value = self.read_nt_str(encoding=self.encoding)
                    row.append(value)
                elif type_code == 2:
                    value = self.read_i32()
                    row.append(value)
                elif type_code == 3:
                    value = self.read_i8()
                    row.append(value)
                elif type_code == 4:
                    value = self.read_i64()
                    row.append(value)
                elif type_code == 5:
                    value = self.read_i16()
                    row.append(value)
                elif type_code == 6:
                    if self.string_format == 'len_prefixed_nt':
                        value = self.read_len_prefixed_nt_str(encoding=self.encoding)
                    elif self.string_format == 'nt':
                        value = self.read_nt_str(encoding=self.encoding)
                    row.append(value)
                else:
                    raise ValueError(f"Unknown type code: {type_code}")
            elements.append(row)
        return elements

    def export_to_csv(self):
        self.seek(0)
        with open(self.file_path, 'rb') as datfile:
            self.set_data(datfile.read())
        self.read_header()
        self.read_types()
        elements = self.read_elements()
        type_mapping = {
            1: 'String',
            2: 'Int32',
            3: 'Int8',
            4: 'Int64',
            5: 'Int16',
            6: 'StringKey'
        }
        headers = [type_mapping[type_code] for type_code in self.types]

        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(headers)
            for row in elements:
                writer.writerow(row)