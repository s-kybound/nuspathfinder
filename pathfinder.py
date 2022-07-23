from lib import *

print("""
NUSpathfinder v0.0
Hello! Please select your course:
1. Computer Science(no 2nd Degree/Major/Minor)
2. Custom
""")
x = int(input("Option: "))
modules = set()
if x == 1:
    # Foundation modules for CS, non-negotiable
    computerscience = [
        "CS1101S",
        "ES2660",
        "IS1108",
        "CS1231S",
        "CS2030S",
        "CS2040S",
        "CS2100",
        "CS2101",
        "CS2103T",
        "CS2106",
        "CS2109S",
        "CS3230"
    ]
    modules.update(computerscience)

    
    math = [
        "MA2001",
        "MA1521",
        "ST2334"
    ]
    modules.update(math)
    print("""
The 'Data Literacy' pillar allows for various options. Which one do you intend to take?
1. GEA1000
2. BT1101
3. ST1131
4. DSE1101
""")
    while True:
        x = int(input("Option: "))
        match x:
            case 1:
                modules.add("GEA1000")
                break
            case 2:
                modules.add("BT1101")
                break
            case 3:
                modules.add("ST1131")
                break
            case 4:
                modules.add("DSE1101")
                break
elif x == 2:
    print("Custom mode selected.")
    modules.update(add_modules("Add all foundation modules not including GE/RC modules."))
else:
    print("Not supported. Sorry!")
    sys.exit(1)
modules.update(add_modules("Add all 4-MC modules in your specialisation/track(s) that you intend to take."))
modules.update(add_modules("Add all remaining 4-MC modules, such as remaining GE/RC4 modules"))
mcs = len(modules) * 4
viable = "VIABLE" if mcs <= 160 else "NOT VIABLE"
print(f"{mcs}/160 MCs used. {viable}")