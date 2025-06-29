Instructions:
>>for 3DSlicer user:
- In 3DSlicer create two 'markup splines' from one end of specimen to the other with the splines fitting as close to edges of bisected segmented bone as possible and one fiducial 'markup control point'. Export the 3 markups from 3DSlicer; .json of spline should be exported from slicer as .json (not .mrk.json) as with the fiducial control point. The python seraliser has been configured to pull control points from 3DSlicer 5.6.2 exported .json not .mrk.json... (it may work on future 3DSlicer releases but this is not garunteed - give it a go)
- To get best results, the fiducial used should be after the last sectioning histology plane (i.e. there should not have been histology cuts taken either side of the fiducial in the laboratory). It should have been physically prohibitive for this to happen but we are noting that the code does not have allowance for this...

>>Running code:
This repo has a venv but if you can't make this work download the scripts and run in your own venv
For this you will need to pip install:
-     numpy
-     matplotlib
-     scipy
-     Other ones I have forgot to mention...?

>> Execute b_RunScript.py
- GUI allows input of the filepath to spline_ma & mb (the splines you createdin 3DSlicer previous which should roughly intersect with the location that elucdian measurements in the lab went to) and f_ref from 3DSlicer to variables fileS1, fildS2 and fileF1 variables respectively.
- input for where output file should go
- input of what the suffix of the bisection is
- labrotory offset measurements (this is the total sum of tissue shaved off the blockface before reaching that used in the histology slide). Set as 0 if there was no/minimal shaving
 

>> Customisation:
GUI inputs can be bypassed by commenting and uncommenting lines in 'testing' for adequately filling the variables required

>> Intended use of planes from this script:
- Drag or import created .json planes into 3DSlicer scene where original splines (and fiducial) control point came from. 
- Constrain each histology image you import to the corresponding plane from this script, continue the histology co-location process as described in XXXXXXXXXXXXX 

***********
>> Future Development opportunities:
- Integration of script into 3DSlicer extension (Or plug into something like RAPSODI, but will need reword to cope with non-serial slicing)


Youtube guide:
#######  url  ##############
