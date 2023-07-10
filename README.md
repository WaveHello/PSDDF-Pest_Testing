# PSDDF-Pest_Testing
 Compilation of the jupyter notebooks required to automate running PSDDF and PSDDF coupled with PEST.
This section details the files required to run a PEST-PSDDF model. Table 1 and Table 2 contain the files required to run the PSDDF and PEST++ part of the model, respectively.
Table 1. Files required to run PSDDF
File Name	Purpose
Addamse.tmp	1)	Contains the name of the PSDDF to be executed (“Model_input” in the below input)
2)	Couples PSDDF with addamse
“Model_Input”.psi	Model inputs for PSDDF
PSDDF.exe	PSDDF program
PSDDF_input.txt	When running PSDDF, it requires a name for the output files. This file contains the output name. This is a user input

Table 2. Files required to run PEST
File Name	Purpose
“Template File”.tpl	PEST template file which controls which variables are read from the PSDDF input file.
“Instruction File”.ins	PEST Instruction file – Tells PEST how to read data from the specified output file
“Control File”.pst	PEST Control file – plays 2 major roles
1)	Defines which files are the template and instruction files for this model run and the corresponding PSDDF files
2)	Defines the parameters required for PEST’s iteration process (i.e. derivative type, error tolerance, objective function weights, etc.)
Run_PestPSDDF.bat	Batch file that runs PSDDF and cleans up the folder so that PEST is able to run
Pestpp-“model_Type”.exe	User chosen model from the pestpp suite. Refer to pestpp manual or link: https://github.com/usgs/pestpp for more infromation

