import argparse
from configurations import Configuration

def make_parser():
    parser = argparse.ArgumentParser(description="Add serialized object code to objects.py")

    parser.add_argument("--name", "-n", default=None, type=str, help="The configuration name. This could be a file path or a name from the lexicon")
    parser.add_argument("--object-name", "-o", type=str, help="The object name to use in the code.")

    return parser

def main():
    args = make_parser().parse_args()

    name = args.name
    oname = args.object_name

    c = Configuration()
    c.load(name)
    c.shift_to_origin()

    with open("./objects.py", "a") as f:
        arr = ",\n        ".join(f"({cell[0]}, {cell[1]})" for cell in sorted(c.alive_cells))
        s = f"""


@GOL_Object
def {oname}():
    return [
        {arr}
    ]"""
        f.write(s)
        

if __name__ == "__main__":
    main()

