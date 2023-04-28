import argparse
from configurations import Configuration

def make_parser():
    parser = argparse.ArgumentParser(description="Add serialized object code to objects.py")

    parser.add_argument("--file-name", "-f", default=None, type=str, help="The serialized object file.")
    parser.add_argument("--lexicon-name", "-l", default=None, type=str, help="The name of the object from the lexicon")
    parser.add_argument("--object-name", "-o", type=str, help="The object name to use in the code.")

    return parser

def main():
    args = make_parser().parse_args()

    fname = args.file_name
    lname = args.lexicon_name
    oname = args.object_name

    c = Configuration()
    if fname is not None:
        c.load(fname)
    else:
        c.load_from_lexicon(lname)
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

