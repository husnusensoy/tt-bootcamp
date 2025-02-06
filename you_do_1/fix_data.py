import csv
class fixer():
    def __init__(self,input_file,output_file,EXPECTED_COLUMNS):
        self.input_file = input_file
        self.output_file = output_file
        self.EXPECTED_COLUMNS = EXPECTED_COLUMNS
        
    def fix_comma_problem(self):
        with open(self.input_file, "r", encoding="latin1") as infile, \
            open(self.output_file, "w", newline="", encoding="utf-8") as outfile:

            writer = csv.writer(outfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)

            for line in infile:
                parts = line.strip().split(",")
                
                if len(parts) > self.EXPECTED_COLUMNS:
                    merged_field = ",".join(parts[self.EXPECTED_COLUMNS-1:])
                    new_row = parts[:self.EXPECTED_COLUMNS-1] + [merged_field]
                    writer.writerow(new_row)
                else:
                    writer.writerow(parts)