# Analysis_Codes
Various analysis and plotting codes for 17F(p, a)20Ne experiments


General notes:
______________________________________

File Beam_Current.py calculates (p,a) cross section using Fernandez paper differential cross section values (Doesn't include normalization factors at the moment)
File cross_section.py calculates (p,a) cross section from recorded beam current and timing schemes in Elog (Not to be used for final calculations, mostly just acted as a preliminary check)

SiliconCSV.cpp and Si_map.py work in conjunction with one another

Make_Cuts.cpp should be run in order to make appropriate TAC and Front Back cuts (although I am not using the FB cut at the moment)

Cuts_Analysis.cpp provides visuals for all cut data

DataFit.cpp is an automated fitting function. Will need to run Beam_Elastics_Counts.cpp first to generate histos on low energy regions from high-B field runs with and without TAC cut. Notes for how to use DataFit.cpp are in file. To use, just run .x DataFit.cpp in ROOT environment.

PAlpha_Counts.cpp is a very rudimentary script to retrieve alpha counts in specified energy regions. Uses Tac cut data and takes all counts within specified energy regions, rings are grouped together as specified by user and then energy regions are specified and applied to user defined ring groups. 

sortGW.sh is a sorting code to turn raw binary files into ROOT Files. At the moment I believer you need tobe connected to ANL servers to run.

5/17/24
__________________________________________________

Added a couple files with similar names. First:

BeamCurrentAvg.py

This file calculates the average beam current over several rings by calculating beam currents for Fernandez differential cross sections in a small energy range. It calculate the average for a group of rings and it also calculates the beam current measure by individual rings.

Second:

Raw_DataFit.cpp

Very similar to DataFit.cpp, but this uses a slightly different integration scheme and adds a couple extra columns of data to the output spreadsheet.

5/21/24
___________________________________________________

Uploaded a more appropriately names cross section calculation file name:

4/18/25
___________________________________________________

In desperate need of updating and cleaning. This is just an upload of a class file I have made to organize everything. Most other Python files are obsolete, this is really the only one in here that matters anymore.

CrossSectionCalc.py

This uses the new integration scheme we have for the Fernandez data and has just some general updates over the old file. USE THIS FILE, NOT THE OLD ONE!
