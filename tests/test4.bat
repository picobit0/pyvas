@echo off
py ../assembler.py -s sign-test.pvs -o sign-test.bin
py ../interpreter.py -c sign-test.bin -d dump.csv -r 0-3
pause