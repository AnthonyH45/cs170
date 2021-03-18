from main import *
import time

print()
print("SMALL BE")
start = time.time()
be(parse(open('CS170_SMALLtestdata__72.txt')))
end = time.time()
print("Seconds elapsed:",end-start)

print()
print("SMALL FS")
start = time.time()
fs(parse(open('CS170_SMALLtestdata__72.txt')))
end = time.time()
print("Seconds elapsed:",end-start)

print()
print("LARGE FS")
start = time.time()
fs(parse(open('CS170_largetestdata__9.txt')))
end = time.time()
print("Seconds elapsed:",end-start)
print()

print()
print("LARGE BE")
start = time.time()
be(parse(open('CS170_largetestdata__9.txt')))
end = time.time()
print("Seconds elapsed:",end-start)