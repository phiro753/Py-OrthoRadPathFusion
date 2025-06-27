Instructions:
>>for 3DSlicer user:
- If using M1 and M2 create 2 'markup splines' in 3DSlicer from one end of specimen to the other with the splines fitting as close to the edges of bisected segmented bone as possible and one fiducial 'markup control point'. 
If using method 3, create a third markup spline that runs along the crest of the segmented bone. Export the markups from 3DSlicer; .json of spline should be exported from slicer as .json (not .mrk.json) as with the fiducial control point. The python seraliser has been configured to pull control points from 3DSlicer 5.6.2 exported .json not .mrk.json... (it may work on future 3DSlicer releases but this is not guaranteed - give it a go)
- To get best results, the fiducial used should be after the last sectioning histology plane (i.e. there should not have been histology cuts taken either side of the fiducial in the laboratory). It should have been physically prohibitive for this to happen but we are noting that the code does not have allowance for this...

>>Running code:
This repo has a venv but if you can't make this work download the scripts and run in your own venv
For this you will need to pip install:
-     numpy
-     matplotlib
-     scipy
-     tkinter
-     json
-     math
-     Other modules when prompted

>>Details on file names and therefore types:
- Main.py file is the main run file that calls other subfiles
- files with prefix "a_" use seralisers and read functions for reading from .JSON markup files in a schema of markup object '.json' export from 3DSlicer
- files with prefix "b_" are called to execute computations 
- files with prefix "c_" use seralisers and write functions to write .jcon markup files in a schema for importing plane objects into 3DSlicer
- files with prefix "d_" are calculation methods that perform quantitative analysis on plane orientation and difference - usage is unnecessary
- files with prefix "e_" were one-off usage for report writing and visualization

>> Execute b_Main.py
- GUI allows input of the filepath to spline_ma, mb, and mc (the splines you createdin 3DSlicer previous which should roughly intersect with the location that euclidean measurements in the lab went to) and F_ref from 3DSlicer to variables fileS1, fileS2, fileS3, and fileF1 variables respectively.
- Input the euclidean measurements taken in the lab
- Input the output folder directory
- Input the bisection suffix for the folder
- Input laboratory offset measurements (this is the total sum of tissue shaved off the blockface before reaching that used in the histology slide). Set as 0 if there was no/minimal shaving
 
>> Customisation:
GUI inputs can be bypassed by commenting and uncommenting boolean variables at the top of the file, these are named inputUI and writeOn, set to False accordingly and then comment in "from b_Specimens" if you want to manually input data as shown in b_Specimens

>> Intended use of planes from this script:
- Drag or import created .json planes into 3DSlicer scene where original splines (and fiducial) control point came from
- Constrain each histology image you import to the corresponding plane from this script, continue the histology co-location process as described in XXXXXXXXXXXXX 

***********
>> Future Development opportunities:
- Integration of script into 3DSlicer extension (Or plug into something like RAPSODI, but will need reword to cope with non-serial slicing)


Youtube guide:
#######  url  ##############
