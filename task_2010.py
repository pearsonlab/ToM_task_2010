import sys
import json
from psychopy import visual, gui, event, core
import random
import numpy as np

from utils import flicker

class Stimuli:
	def __init__(self, win, timing):
		self.win = win
		self.timing = timing
		self.keymap = {'1': 1, '2': 2, '3': 3, '4': 4}

	def show_story(self, trial):
		story_start = core.getTime()
		text = self.text(trial.decode('utf-8'))
		self.win.flip()
		offset = flicker(self.win, 1)
		core.wait(self.timing['story'] - offset)
		text.autoDraw = False
		self.win.flip()
		self.win.flip()
		return story_start
		
	def show_question(self, trial):
		quest_start = core.getTime()
		text = self.text("How likely is it that...\n\n" + trial.decode('utf-8'))
		self.win.flip()
		offset = flicker(self.win, 4)
		key = event.waitKeys(
					maxWait=self.timing['question'] - offset, keyList=self.keymap.keys() + ['escape'])
		if key is None:
			text.autoDraw = False
			self.win.flip()
			self.win.flip()
			return(quest_start, 'timeout', 'timeout')
		elif key == 'escape':
			flicker(self.win, 0)
			core.quit()
		else:
			text.autoDraw = False
			self.win.flip()
			self.win.flip()
			time_of_resp = core.getTime()
			offset = flicker(self.win, 16)
			return (quest_start, self.keymap[key[0]], time_of_resp)		
		
	def text_and_stim_keypress(self, text, stim=None):
		if stim is not None:
			if type(stim) == list:
				map(lambda x: x.draw(), stim)
			else:
				stim.draw()
		display_text = visual.TextStim(self.win, text=text,
										font='Helvetica', alignHoriz='center',
										alignVert='center', units='norm',
										pos=(0, 0), height=0.1,
										color=[255, 255, 255], colorSpace='rgb255',
										wrapWidth=2)
		display_text.draw()
		self.win.flip()
		key = event.waitKeys()
		if key[0] == 'escape':
			flicker(self.win, 0)
			core.quit()
			self.win.flip()
		self.win.flip()
		
	def text(self, text):
		display_text = visual.TextStim(self.win, text=text,
                                       font='Helvetica', alignHoriz='center',
                                       alignVert='center', units='norm',
                                       pos=(0, 0), height=0.1,
                                       color=[255, 255, 255], colorSpace='rgb255',
                                       wrapWidth=2)
		display_text.autoDraw=True
                                       
		return display_text

def get_settings():
    dlg = gui.Dlg(title='Choose Settings')
    dlg.addField('Experiment Name:', 'ToM_Task_2010')
    dlg.addField('Subject ID:', '0')
    dlg.addField('Speed Factor:', 1.0)
    dlg.addField('Start Number:', 0)
    dlg.show()
    if dlg.OK:
        return dlg.data
    else:
        sys.exit()

def get_window():
    return visual.Window(
        winType='pyglet', monitor="testMonitor", units="pix", screen=1,
        fullscr=True, colorSpace='rgb255', color=(0, 0, 0))

def run():
	(expname, sid, speed, start_num) = get_settings()
	
	win = get_window()
	timing = {'fixation': 4.,
				'story': (6.*speed),
				'question': (6.*speed),
				'delay': 4.}
	
	win.mouseVisible = False
	
	stim = Stimuli(win, timing)
	
	stim.text_and_stim_keypress('You are going to be reading a number of stories about\n'+
								'different people and places.\n\n'+
								'Afterward, you will be asked a question about the likelihood\n'+
								'of each event.\n\n' +
								'(Press any key to continue)')
	stim.text_and_stim_keypress('      Rank the likelihood on a scale from 1 to 4.\n\n'+
								'       1         -         2         -         3         -         4 \n\n'+
								'(Very Unlikely)                                     (Very Likely)')
	stim.text_and_stim_keypress('Ready?\n\n'+
    							'Press any key to begin!')
    
	
	win.flip()
	core.wait(timing['fixation'])
	
	# Mental stories
	with open('text_files/mental_expected.txt') as f:
		mental_exp = f.readlines()
	with open('text_files/mental_unexpected.txt') as f:
		mental_unexp = f.readlines()
	with open('text_files/mental_questions.txt') as f:
		mental_quest = f.readlines()
	
	# Physical stories	
	with open('text_files/physical_expected.txt') as f:
		physical_exp = f.readlines()
	with open('text_files/physical_unexpected.txt') as f:
		physical_unexp = f.readlines()
	with open('text_files/physical_questions.txt') as f:
		physical_quest = f.readlines()
		
	# Two random arrays of 0s and 1s as counters
	condition = np.random.randint(0, 2, 48) # expected (0) or unexpected (1)
	state = np.random.randint(0, 2, 48) # mental (0) or physical (1)
	
	line_counter = start_num
	
	while line_counter < 48:
		trial_dict = {}
		trial_dict['trial_num'] = line_counter+1
	
		if condition[line_counter] == 0:
			trial_dict['condition'] = 'expected'
			
			if state[line_counter] == 0:
				trial_dict['state'] = 'mental'
				story_start = stim.show_story(mental_exp[line_counter])
				quest_start, resp, time_resp = stim.show_question(mental_quest[line_counter])
			else:
				trial_dict['state'] = 'physical'
				story_start = stim.show_story(physical_exp[line_counter])
				quest_start, resp, time_resp = stim.show_question(physical_quest[line_counter])
		
		else:
			trial_dict['condition'] = 'unexpected'
			
			if state[line_counter] == 0:
				trial_dict['state'] = 'mental'
				story_start = stim.show_story(mental_unexp[line_counter])
				quest_start, resp, time_resp = stim.show_question(mental_quest[line_counter])
			else:
				trial_dict['state'] = 'physical'
				story_start = stim.show_story(physical_unexp[line_counter])
				quest_start, resp, time_resp = stim.show_question(physical_quest[line_counter])
			
		trial_dict['story_start'] = story_start
		trial_dict['quest_start'] = quest_start
		trial_dict['response'] = resp
		trial_dict['time_of_response'] = time_resp
		
		if time_resp != 'timeout':
			trial_dict['response_time'] = time_resp - quest_start
		else:
			trial_dict['response_time'] = 'timeout'

		if not os.path.exists('behavioral/'):
			os.makedirs('behavioral')
	
		with open('behavioral/' + expname + '_' + str(sid)+ '.json', 'a') as f:
			f.write(json.dumps(trial_dict))
			f.write('\n')
		
		core.wait(timing['delay'])
		line_counter += 1
	
	text = stim.text('Congratulations! You\'ve finished!')
	win.flip()
	core.wait(timing['delay'])			
	core.quit()



if __name__ == '__main__':
	run()