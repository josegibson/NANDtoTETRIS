
comp_dict = {
    "0"  : "0101010",
    "1"  : "0111111",
    "-1" : "0111010",
    "D"  : "0001100",
    "A"  : "0110000",
    "!D" : "0001101",
    "!A" : "0110001",
    "-D" : "0001111",
    "-A" : "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M"  : "1110000",
    "!M" : "1110001",
    "-M" : "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest_dict = {
    "" : "000",
    "M"  : "001",
    "D"  : "010",
    "MD" : "011",
    "A"  : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD": "111"
}

jump_dict = {
    "" : "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


class Convert:
    def __init__(self, symbol_mgr):
        self.symbol_mgr = symbol_mgr

    def replace_symbols(self, parsed_tuples):
        parsed_tuples_second_pass = []

        for parsed_line in parsed_tuples:
            if parsed_line[0] == 'A':
                value = self.symbol_mgr.decode(parsed_line[1])
                if value is None:
                    # means, it is a variable symbol
                    self.symbol_mgr.add(parsed_line[1])
                parsed_tuples_second_pass.append(tuple(('A', value)))
            else:
                parsed_tuples_second_pass.append(parsed_line)

        return parsed_tuples_second_pass
    
    def convert_binary(self, final_asm):
        final_bin = []
        for line in final_asm:
            machine_code = ''
            if line[0] == 'A':
                machine_code += '0' + format(line[1], '015b')
            else:
                c_values = line[1]
                machine_code += '111'
                machine_code += comp_dict[c_values[1]]
                machine_code += dest_dict[c_values[0]]
                machine_code += jump_dict[c_values[2]]

            # print(line, '\t\t\t', machine_code)
            final_bin.append(machine_code)

        return final_bin
