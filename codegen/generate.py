import csv
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def parse_pattern(pattern):
    bits = pattern.replace(" ", "")
    if len(bits) == 32:
        # 16 bits suffice to recognize 32 bit opcode
        bits = bits[:16]
        
    if len(bits) != 16:
        print(f'Warning: Expected 16 or 32 bit opcode, actual length is {len(bits)} bits')
        return None, None

    mask = 0
    value = 0

    for i, ch in enumerate(bits):
        bit_position = 15 - i 
        
        if ch == '0':
            mask |= (1 << bit_position)
            
        elif ch == '1':
            mask |= (1 << bit_position)
            value |= (1 << bit_position)
        
    return mask, value


def load_instructions(csv_file):
    instructions = []
    try:
        with open(csv_file, newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if len(row) < 2:  # need at least name and opcode, other columns are ignored
                    continue
                    
                name = row[0].strip()
                pattern = row[1].strip()

                mask, value = parse_pattern(pattern)
                
                if mask is None:
                    continue

                instructions.append({'name': name, 'pattern': pattern, 'mask': mask, 'value': value })

    except FileNotFoundError:
        print(f'Error: csv file {csv_file} not found')
        exit(1)

    return instructions


def build_table(instructions):
    table = [None] * 65536

    for opcode in range(65536):
        for ins in instructions:
            if (opcode & ins["mask"]) == ins["value"]:
                table[opcode] = ins["name"]
                break

        if table[opcode] is None:
            table[opcode] = "UNDEFINED"

    return table


def write_file_if_changed(filename, new_content):
    try:
        with open(filename, 'r') as f:
            existing_content = f.read()

        if existing_content == new_content:
            print(f'{filename} is unchanged, not writing')
            return

    except FileNotFoundError:
        print(f'{filename} not found, creating new file')

    with open(filename, "w") as f:
        f.write(new_content)
        print(f"{filename} written")


def populate_template(template_name, output_dir, env, instructions, table):
    template = env.get_template(template_name)
    output = template.render(
        instructions=instructions,
        table=table
    )
    write_file_if_changed(output_dir, output)


def main():
    # directories
    codegen_dir = Path(__file__).parent.resolve()
    template_dir = codegen_dir / 'templates'
    output_dir = codegen_dir.parent / 'build' / 'generated'

    # create output_dir if it does not exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Jinja setup
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # build instruction table
    instructions = load_instructions("instructions.csv")
    table = build_table(instructions)

    # code generation
    populate_template('instructions_fallback.c.j2', output_dir / 'instructions_fallback.c', env, instructions, table)
    populate_template('instructions.h.j2', output_dir / 'instructions.h', env, instructions, table)


if __name__ == "__main__":
    main()