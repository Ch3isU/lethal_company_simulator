def log_warning(text):
    print(f"Warning: {text}")

def read_bool(question):
    answer = ""
    while answer != "yes" and answer != "no":
        answer = input(question).lower()
    if answer == "yes":
        return True
    elif answer == "no":
        return False
    else:
        log_warning("I fucked up somehow (yes or no is maybe)")
        return False
    
def read_items_from_file():
    filename = "src/items.txt"
    item_file = open(filename, 'r')
    items = []
    for line in item_file:
        if line.startswith("#"):
            continue
        elems = line.split(", ")
        if len(elems) != 3:
            log_warning(f"a line containing playerinformation in file {filename} is not formatted correctly")
            continue
        try:
            items.append([elems[0], int(elems[1]), int(elems[2])])
        except:
            log_warning(f"a line containing playerinformation in file {filename} is not formatted correctly")
    return items
