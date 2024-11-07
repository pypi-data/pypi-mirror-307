class DatFileError(Exception):
    pass

class RecordIndexError(DatFileError):
    pass

class NoDataInObjectError(DatFileError):
    pass

class NoColumnError(DatFileError):
    pass

class InvalidColumnError(DatFileError):
    pass


class DatFile(object):
    """
    Class for represent *.dat files
    """

    def __init__(self) -> None:
        '''
        DatFile constructor
        '''
        self.columns_names = []
        self.data_list_of_records = []

    def __del__(self) -> None:
        '''
        DatFile deconstruction
        '''
        pass # TODO

    @staticmethod
    def parse_record_from_line(line: str, reject_columns: list=[]) -> list:
        '''
        Parse record from line.
        '''
        line_list = []

        for idx, val in enumerate(line.split('\t')):
            if idx not in reject_columns:
                line_list.append(val.replace("\n", ""))
        
        return line_list
    
    @staticmethod
    def record_to_float(record: list) -> list:
        '''
        Convert record which stores is string format to float format
        '''
        result = list()

        for val in record:
            if type(val) != float:
                result.append(float(val))
            else:
                result.append(val)

        return result
    
    @staticmethod
    def record_to_str(record: list) -> list:
        '''
        Convert record from float or int representation to string representation of values
        '''

        result = list()

        for val in record:
            if type(val) != str:
                result.append(str(val))
            else:
                result.append(val)
        
        return result
    
    @staticmethod
    def build_line_from_record(record : list) -> str:
        '''
        Build line for *.dat file from record
        '''
        out_str = ""

        for val in record:
            out_str += val
            out_str += '\t'

        out_str = out_str[:-1]
        out_str += '\n'

        return out_str
    
    @staticmethod
    def calc_avg_for_records(records: list) -> list:
        '''
        Calc average for list of records

        Return 
        '''
        if len(records) == 0:
            raise NoDataInObjectError("No records in list for averaging")

        result = list()
        for _ in records[0]:
            result.append(0.0)

        for record in records:
            record_in_floats = DatFile.record_to_float(record)
            for idx, val in enumerate(record_in_floats):
                result[idx] += val

        for idx, _ in enumerate(result):
            result[idx] /= len(records)

        return DatFile.record_to_str(result)
    
    @staticmethod
    def float_from_str(val_in_str: str) -> float:
        '''
        Convert string to float
        '''
        return float(val_in_str)
    

    def get_columns_count(self) -> int:
        '''
        Get columns count.
        '''
        if len(self.data_list_of_records) == 0:
            return 0
        
        return len(self.data_list_of_records[0])

    def get_columns_names(self) -> list:
        '''
        Get columns names.
        '''
        return self.columns_names.copy()

    def set_columns_names(self, names: list) -> None:
        '''
        Set column names.
        '''
        if self.get_columns_count() != len(names) and len(names) != 0:
            raise InvalidColumnError("Invalid column count")

        self.columns_names = names.copy()

    def get_records_count(self) -> int:
        '''
        Get records count.
        '''
        return len(self.data_list_of_records)

    def get_records(self) -> list:
        '''
        Get all records.
        '''
        return self.data_list_of_records

    def get_record(self, index: int) -> list:
        '''
        Get record by index.
        '''
        if index >= len(self.data_list_of_records):
            raise RecordIndexError("Index out of range")
        
        return self.data_list_of_records[index].copy()
    
    def add_record(self, record: list) -> None:
        '''
        Add record to DatFile object instance
        '''
        if self.get_columns_count() == 0:
            pass
        else:
            if len(record) != self.get_columns_count():
                raise InvalidColumnError("Invalid column count")
        
        self.data_list_of_records.append(record.copy())


    def add_records(self, records: list) -> None:
        '''
        Add records to DatFile object instance
        '''
        for record in records:
            self.add_record(record)


    def read(self, filepath: str, has_header: bool=False, reject_columns: list=[]) -> None:
        '''
        Parse *.dat file into Datfile instance
        '''

        lines = None
        try:
            with open(filepath, "r", encoding='utf-8-sig') as input_file:
                lines = input_file.readlines()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='utf-16') as input_file:
                lines = input_file.readlines()
        except:
            raise DatFileError("Cannot open file")

        column_names = None
        for idx, line in enumerate(lines):
            if has_header and idx == 0:
                column_names = DatFile.parse_record_from_line(line, reject_columns)
                continue

            line_list = DatFile.parse_record_from_line(line, reject_columns)
            self.data_list_of_records.append(line_list)
        
        if has_header:
            self.set_columns_names(column_names)

    def write(self, filepath: str, is_include_header: str = False) -> None:
        '''
        Write records of Datfile instance to *.dat file
        '''
        if self.get_records_count() == 0:
            raise NoDataInObjectError("No data in object for writing in file")
        
        header = None
        if is_include_header:
            header = self.get_columns_names()

        with open(filepath, 'w', encoding='utf-8') as out_f:
            if header is not None:
                out_f.write(DatFile.build_line_from_record(header))
        
            for record in self.get_records():
                out_f.write(DatFile.build_line_from_record(record))

    def avg(self, period:  int, start_idx: int = None, end_idx: int = None) -> 'DatFile':
        '''
        Calculate average for records.

        Using half-period notation [start_idx ; end_idx)
        
        Warning: all records which cannot be calculated by period at the end will be left
        '''
        if period == 0:
            raise ValueError("Period cannot be 0")
        
        if period > self.get_records_count():
            raise RecordIndexError("Period exceeds records count")
        
        if (start_idx != None) and (start_idx > self.get_records_count() - 1):
            raise RecordIndexError("Start index exceeds records count")
        
        if (end_idx != None) and (end_idx > self.get_records_count()):
            raise RecordIndexError("End index exceeds records count")

        if (start_idx != None) and (end_idx != None) and (start_idx > end_idx):
            raise RecordIndexError("Start index exceeds end index")

        remain_count = self.get_records_count()
        start_idx = 0 if start_idx == None else start_idx
        curr_idx = start_idx
        end_idx = self.get_records_count() if end_idx == None else end_idx

        avg_datfile = DatFile()

        while ((remain_count >= period) and ((curr_idx + period) <= end_idx)):
            avg_record = DatFile.calc_avg_for_records(self.get_records()[curr_idx : curr_idx + period])
            avg_datfile.add_record(avg_record)

            remain_count -= period
            curr_idx += period

        return avg_datfile
    
    def filter(self, column_idx: int, min_val:float=None, max_val:float=None) -> 'DatFile':
        '''
        Filter records by column value and return new DatFile object.
        '''
        if column_idx >= self.get_columns_count() - 1 or column_idx < 0:
            raise NoColumnError("Column index exceeds columns count")
        
        filtered = DatFile()
        
        for record in self.get_records():
            if (min_val != None) and (DatFile.float_from_str(record[column_idx]) < min_val):
                continue
            
            if (max_val != None) and (DatFile.float_from_str(record[column_idx]) > max_val):
                continue

            filtered.add_record(record)
        
        return filtered
    
    def reverse(self) -> 'DatFile':
        '''
        Reverse records order and return new DatFile object.
        '''
        reversed_datfile = DatFile()
        reversed_datfile.data_list_of_records = self.data_list_of_records[::-1]

        reversed_datfile.set_columns_names(self.get_columns_names())

        return reversed_datfile
        
            
            
            

