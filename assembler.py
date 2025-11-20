from argparse import ArgumentParser

commands = {
    "ld": 63,
    "rd": 13,
    "wr": 36,
    "sg": 29
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-s", "--source", required=True)
    parser.add_argument("-o", "--output")
    parser.add_argument("-t", "--test", action="store_true")
    return parser.parse_args()

def parse_line (line):
    if ":" in line:
        line = line[:line.find(":")].strip()
    if not line: return
    
    command, *args = line.split()
    command = command.lower()
    if command not in commands:
        raise SyntaxError("Unknown command: " + command)
    if len(args) > 1:
        raise ValueError(f"Too many arguments (expected {len(args)}): {', '.join(args)}")
    if len(args) < 1:
        raise ValueError(f"Expected 1 argument, 0 found")
    arg = int(args[0])
    return commands[command], arg
    
if __name__ == "__main__":
    args = parse_args()
    try:
        il = []
        with open(args.source) as f:
            for i, line in enumerate(f):
                cmd = parse_line(line.rstrip("\n"))
                if cmd: il.append(cmd)
        print(f'"{args.source}" parsed successfully')
        if args.test:
            print("Intermediate representation:")
            for cmd in il:
                print(cmd)
    except SyntaxError as e:
        print(f"Syntax error at line {i+1}:")
        print("\t" + line.rstrip("\n"))
        print(e)
    except ValueError as e:
        print(f"Argument error at line {i+1}:")
        print("\t" + line.rstrip("\n"))
        print(e)
