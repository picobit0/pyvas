@echo off
echo == Test 5-1 == 
py ../assembler.py -s test5-1.pvs -o test5.bin
py ../interpreter.py -c test5.bin -d test5-1.csv -r 0-5

echo.
echo == Test 5-2 ==
py ../assembler.py -s test5-2.pvs -o test5.bin
py ../interpreter.py -c test5.bin -d test5-2.csv -r 0-5

echo.
echo == Test 5-3 ==
py ../assembler.py -s test5-3.pvs -o test5.bin
py ../interpreter.py -c test5.bin -d test5-3.csv -r 0-5

pause