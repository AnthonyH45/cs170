from main import *

print()
print("SMALL BE")
be(parse(open('CS170_SMALLtestdata__72.txt')))
print()
print("LARGE BE")
be(parse(open('CS170_largetestdata__9.txt')))

print()
print("SMALL FS")
fs(parse(open('CS170_SMALLtestdata__72.txt')))
print()
print("LARGE FS")
fs(parse(open('CS170_largetestdata__9.txt')))
print()