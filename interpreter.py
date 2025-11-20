from argparse import ArgumentParser

def stack_pop():
    if not stack:
        raise ValueError("Attempted to read from empty stack")
    return stack.pop()

def load(value):
    stack.append(value)

def read(offset):
    address = stack_pop() + offset
    value = memory[address]
    stack.append(value)

def write(address):
    value = stack_pop()
    memory[address] = value

def sign(address):
    value = stack_pop()
    value = (abs(value) // value) if value else 0
    memory[address] = value

def parse_range(s):
    try:
        st, end = map(int, s.split("-"))
        return slice(st, end + 1)
    except:
        return None

def parse_args ():
    parser = ArgumentParser()
    parser.add_argument("-c", "--code", required=True)
    parser.add_argument("-d", "--dump")
    parser.add_argument("-r", "--range", type=parse_range)
    return parser.parse_args()

def read_cmd(f):
    b = f.read(1)
    cmd = int.from_bytes(b) & 0b111111
    if not cmd:
        return
    if cmd not in commands:
        raise SyntaxError(f"Unknown command id: {cmd}")
    
    size = 4 if cmd == 63 else 3
    b += f.read(size - 1)
    arg = int.from_bytes(b, "little", signed=cmd==63) >> 6
    return cmd, arg

def save_dump(path, memory):
    with open(path, "w") as f:
        f.write(",".join(map(str, memory)))

commands = {
    63: load,
    13: read,
    36: write,
    29: sign
}

commandAliases = {
    63: "LD",
    13: "RD",
    36: "WR",
    29: "SG"
}

stack = []
memory = [0] * 2**16

if __name__ == "__main__":
    try:
        args = parse_args()
        with open(args.code, "rb") as f:
            cmds = []
            while True:
                cmd = read_cmd(f)
                if not cmd: break
                cmds.append(cmd)
        print(f'"{args.code}" read successfully, starting execution')
        for i, (cmd, arg) in enumerate(cmds):
            commands[cmd](arg)
        print("Execution finished successfully")
        if args.dump:
            print(f'Saving memory dump to "{args.dump}"')
            if not args.range:
                save_dump(args.dump, memory)
            else:
                save_dump(args.dump, memory[args.range])
            print("Memory dump saved")
        
    except SyntaxError as e:
        print("Binary read error:")
        print(e)
    except ValueError as e:
        print(f"Runtime error at operation {i}:")
        print(f"\t{commandAliases[cmd]} {arg}")
        print(e)
    except IndexError as e:
        print(f"Runtime error at operation {i}:")
        print(f"\t{commandAliases[cmd]} {arg}")
        print("Memory address out of range")
