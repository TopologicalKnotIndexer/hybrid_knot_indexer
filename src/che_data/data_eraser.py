import os
dirnow = os.path.dirname(os.path.abspath(__file__))

def erase_all_but_first_file(pathnow):
    assert os.path.isdir(pathnow)
    for file in os.listdir(pathnow):
        filepath = os.path.join(pathnow, file)
        if os.path.isfile(filepath) and not filepath.endswith("_1"):
            os.remove(filepath)

def main():
    for file in os.listdir(dirnow):
        filepath = os.path.join(dirnow, file)
        if os.path.isdir(filepath):
            erase_all_but_first_file(filepath)

if __name__ == "__main__":
    main()