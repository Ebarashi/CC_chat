class File_handler:
    def __init__(self, file_name, MAX_BYTES):
        self.file_name = file_name
        self.max_bytes = MAX_BYTES
        print(self.file_name)
        self.file = open(self.file_name, 'rb')

    def get_next_chunk(self):
        byte_array = []
        for i in range(self.max_bytes):
            byte_s = self.file.read(1)
            if not byte_s:
                break
            byte_array.append(byte_s)
        if len(byte_array) == 0:
            return None
        return byte_array
