@echo off
py ../assembler.py -s array-copy.pvs -o array-copy.bin
py ../interpreter.py -c array-copy.bin -d dump.csv -r 0-16
pause