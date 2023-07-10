@echo off

rem Specify the file that the filename for the PSDDF outputs should be read from
PSDDF < PSDDF_input.txt

rem !!!! Important: Make sure the text file that the name is being read from has a carrirage return after the name
rem The format of the "InputFileName".text should be the name then an enter so the cursor goes to the start of the next line
rem This is necessary as it acts as an enter in the PSDDF fortran code

rem Clean up temporary files
rem del input.txt

@Pause
