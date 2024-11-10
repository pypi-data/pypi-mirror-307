import math 
import struct 
import logging 
import logging 

logger = logging.getLogger(__name__)

class ZipInfo:       
    @staticmethod
    def get_offset(offset: int) -> int:
        return int(math.floor(offset / (1024 * 1024)) / 1024 * 1024)

    @staticmethod
    def find_central_directory(data: bytes):
        EOCD_MIN_SIZE = 22
        eocd_signature = b'\x50\x4b\x05\x06'
        for i in range(len(data) - EOCD_MIN_SIZE, -1, -1):
            if data[i:i+4] == eocd_signature:
                logger.debug("Found EOCD at offset", i)
                central_dir_offset, central_dir_size, total_entries = ZipInfo.parse_eocd(data[i:i+EOCD_MIN_SIZE])
                return central_dir_offset, central_dir_size, total_entries 
        return None, None, None

    @staticmethod
    def parse_eocd(eocd_data):
        if len(eocd_data) < 22:
            raise Exception("Incomplete EOCD record")
        (
            signature,
            disk_number,
            start_disk_number,
            total_entries_disk,
            total_entries,
            central_dir_size,
            central_dir_offset,
            comment_length
        ) = struct.unpack('<IHHHHIIH', eocd_data)
        return central_dir_offset, central_dir_size, total_entries

    @staticmethod
    def parse_central_directory(data: bytes, data_offset: int, total_records: int):
        CDR_SIGNATURE = b'\x50\x4b\x01\x02'
        file_info_list = []
        if data[data_offset:data_offset+4] != CDR_SIGNATURE:
            logger.warning("Central Directory Record signature not found at index {}.".format(data_offset))
            return file_info_list

        logger.debug("Found central directory at offset", data_offset)

        for _ in range(total_records):
            fields = struct.unpack('<4s2H2H2H3I5H2I', data[data_offset:data_offset+46])
            signature = fields[0]
            version_made_by = fields[1]
            version_needed_to_extract = fields[2]
            general_purpose_bit_flag = fields[3]
            compression_method = fields[4]
            last_mod_file_time = fields[5]
            last_mod_file_date = fields[6]
            crc32 = fields[7]
            compressed_size = fields[8]
            uncompressed_size = fields[9]
            filename_length = fields[10]
            extra_field_length = fields[11]
            file_comment_length = fields[12]
            disk_number_start = fields[13]
            internal_file_attributes = fields[14]
            external_file_attributes = fields[15]
            header_offset = fields[16]
            filename_bytes = data[data_offset+46:data_offset+46+filename_length]
            filename = filename_bytes.decode()
            local_header_size = 30
            start_byte = header_offset + local_header_size + filename_length + extra_field_length

            if compressed_size == 0:
                end_byte = start_byte
            else:
                end_byte = start_byte + compressed_size - 1

            file_info_list.append({
                'filename': filename,
                'start_byte': start_byte,
                'end_byte': end_byte
            })
            data_offset += 46 + filename_length + extra_field_length + file_comment_length

        return file_info_list
