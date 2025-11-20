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

def cmd_to_bin (cmd, arg):
    match (cmd):
        case 63:
            argBits = 24
        case 13:
            argBits = 14
        case 36 | 29:
            argBits = 16
    if arg.bit_length() > argBits:
        raise OverflowError(f"Argument {arg} is to big")
    size = (5 + argBits) // 8 + 1
    b = arg << 6 | cmd
    return b.to_bytes(size, "little")

if __name__ == "__main__":
    args = parse_args()
    try:
        il = []
        with open(args.source) as f:
            for i, line in enumerate(f):
                cmd = parse_line(line.rstrip("\n"))
                if cmd: il.append(cmd)
        print(f'"{args.source}" parsed successfully')
        b = []
        for i, line in enumerate(il):
            b.append(cmd_to_bin(*line))
        b = b"".join(b)
            
        if args.output:
            with open(args.output, "wb") as f:
                f.write(b)
            print(f'"{args.source}" assembled into "{args.output}" ({len(b)} bytes)')
        if args.test:
            print("Binary assembly result:")
            for i in b:
                print(f"0x{i:0>2X}", end=" ")
            print()
            
    except SyntaxError as e:
        print(f"Syntax error at line {i+1}:")
        print("\t" + line.rstrip("\n"))
        print(e)
    except ValueError as e:
        print(f"Argument error at line {i+1}:")
        print("\t" + line.rstrip("\n"))
        print(e)
    except OverflowError as e:
        print(f"Overflow error at line {i+1}:")
        print(e)
