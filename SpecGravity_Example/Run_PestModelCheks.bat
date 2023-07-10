@echo off

echo ----------Checking the template file--------------
echo.

tempchek FindGs_inTempl.tpl

echo.
echo ----------Template Check Complete--------------
echo.

echo.
echo ----------Checking the instruction file--------------
echo.

echo (Note: The PSDDF the instructions read from are required to be in the current directory.
echo if the console is stuck check to make sure the PSDDF file is there)

inschek FindGs_Instruc.ins Gs_finder_Rs.psp

echo.
echo ----------Instruction File Complete--------------
echo.

echo.
echo ----------Running PESTChek--------------
echo.

pestchek FindGs_Control

echo.
echo ----------PESTChek Complete--------------
echo.

@Pause