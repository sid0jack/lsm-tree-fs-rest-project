from collections import OrderedDict

class Memtable:
    def __init__(self):
        self.table = OrderedDict()

    def write(self, key, value):
        self.table[key] = value

    def read(self, key):
        return self.table.get(key, None)

    def flush(self):
        # This method will be used to flush the memtable to an SSTable
        data = self.table.copy()
        self.table.clear()
        return data


def create_sstable(data, sstable_path):
    with open(sstable_path, 'w') as file:
        for key, value in sorted(data.items()):
            file.write(f'{key}:{value}\n')

def read_from_sstable(key, sstable_path):
    with open(sstable_path, 'r') as file:
        for line in file:
            k, v = line.strip().split(':', 1)
            if k == key:
                return v
    return None

class LSMTree:
    def __init__(self, memtable_size_threshold):
        self.memtable = Memtable()
        self.memtable_size_threshold = memtable_size_threshold
        self.sstable_paths = []

    def write(self, key, value):
        self.memtable.write(key, value)
        if len(self.memtable.table) >= self.memtable_size_threshold:
            self.flush_memtable()

    def flush_memtable(self):
        data = self.memtable.flush()
        sstable_path = f'sstable_{len(self.sstable_paths)}.dat'
        create_sstable(data, sstable_path)
        self.sstable_paths.append(sstable_path)
    
    def read(self, key):
        # Check in memtable first
        value = self.memtable.read(key)
        if value is not None:
            # Search in SSTables
            for sstable_path in reversed(self.sstable_paths):
                value = read_from_sstable(key, sstable_path)
                if value is not None:
                    break
        return value
