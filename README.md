# ToM_task_2010

Adapted from stimuli provided by Saxe Lab at MIT

http://saxelab.mit.edu/resources/stimuli/Young,%20Dodell-Feder,%20&%20Saxe,%202010_Stimuli.pdf

http://www.sciencedirect.com/science/article/pii/S0028393210001934

Files:

- task_2010.py runs in PsychoPy, using stimuli in 'text_files/' directory, saving behavioral data to 'behavioral' directory
- behav_process_loc.py takes behavioral .json files and converts them into .csv files for easier analysis
- data_analysis_2010.py takes .csv files and imports them (either into iPython notebook for interactive work) or outputs image files of barplots comparing conditions of experiment (similar to behavioral analysis in intial paper).

Requirements:

- create directories 'behavioral', 'data', and 'data/images' as destinations for behavioral data and files processed after.
