#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.2.3),
    on Tue Dec 19 12:41:07 2023
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# Run 'Before Experiment' code from dialogue1
import time

#defaults
blockLength = 20
numBlocks = 5
nullPeriod = 0
condition = 'left'

params = {
        'blockLength': blockLength,
        'numBlocks': numBlocks,
        'nullPeriod': nullPeriod,
        'condition':['left', 'right', 'left_no_touch', 'right_no_touch']
        }

tip = {
        'blockLength': 'length of on/off cycle',
        'numBlocks': 'number of blocks to run',
        'nullPeriod': 'initial rest period after trigger recieve',
        'condition': 'left / right hand finger taps or left / right taps without touch'
        }

params['timeStr']= time.strftime("%Y_%b_%d_%H%M", time.localtime())

# create dialogue box and save changed parameters
dlg = gui.DlgFromDict(
    dictionary=params,
    title="Finger Tapping",
    fixed=['timeStr'],
    sortKeys=True,
    tip=tip)

print(""); print(""); print(params); print("") # print to screen
# Run 'Before Experiment' code from dlg_values
blockLength = dlg.dictionary['blockLength']
numBlocks = dlg.dictionary['numBlocks']
nullPeriod = float(dlg.dictionary['nullPeriod'])
condition = dlg.dictionary['condition']

if condition == 'left':
    condition = 'movies/lefttaps.avi'
elif condition == 'right':
    condition = 'movies/righttaps.avi'
elif condition == 'left_no_touch':
    condition = 'movies/lefttaps_almost.avi'
else: 
    condition = 'movies/righttaps_almost.avi'

print("condition was: " + condition); print("")
# Run 'Before Experiment' code from nestedlist
nestedlist = []
# Run 'Before Experiment' code from nestedrestlist
nestedrestlist = []
# --- Setup global variables (available in all functions) ---
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'fingertaps'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 99):06.0f}",
    'session': '001',
    'date': data.getDateStr(),  # add a simple timestamp
    'expName': expName,
    'psychopyVersion': psychopyVersion,
}


def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # temporarily remove keys which the dialog doesn't need to show
    poppedKeys = {
        'date': expInfo.pop('date', data.getDateStr()),
        'expName': expInfo.pop('expName', expName),
        'psychopyVersion': expInfo.pop('psychopyVersion', psychopyVersion),
    }
    # show participant info dialog
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # restore hidden keys
    expInfo.update(poppedKeys)
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/torrisi/Desktop/NCIRE.VA.UCSF/flex_finger_from_github_for_cspine/flex_finger_tap_d4_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # this outputs to the screen, not a file
    logging.console.setLevel(logging.ERROR)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.ERROR)
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1440, 900], fullscr=True, screen=0,
            winType='pyglet', allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height'
        )
        if expInfo is not None:
            # store frame rate of monitor if we can measure it
            expInfo['frameRate'] = win.getActualFrameRate()
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    win.mouseVisible = False
    win.hideMessage()
    return win


def setupInputs(expInfo, thisExp, win):
    """
    Setup whatever inputs are available (mouse, keyboard, eyetracker, etc.)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    dict
        Dictionary of input devices by name.
    """
    # --- Setup input devices ---
    inputs = {}
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='ptb')
    # return inputs dict
    return {
        'ioServer': ioServer,
        'defaultKeyboard': defaultKeyboard,
        'eyetracker': eyetracker,
    }

def pauseExperiment(thisExp, inputs=None, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # make sure we have a keyboard
        if inputs is None:
            inputs = {
                'defaultKeyboard': keyboard.Keyboard(backend='PsychToolbox')
            }
        # check for quit (typically the Esc key)
        if inputs['defaultKeyboard'].getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win, inputs=inputs)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, inputs=inputs, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, inputs, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    inputs : dict
        Dictionary of input devices by name.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = inputs['ioServer']
    defaultKeyboard = inputs['defaultKeyboard']
    eyetracker = inputs['eyetracker']
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "dialogue" ---
    # Run 'Begin Experiment' code from dialogue1
    thisExp.addData('exp parameters', params)
    
    # --- Initialize components for Routine "instructions" ---
    tapping_instructions = visual.TextStim(win=win, name='tapping_instructions',
        text='Please press the button box with your index finger whenever the fingers in the video touch.',
        font='Open Sans',
        pos=(0, 0), height=0.06, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    scan_trigger = keyboard.Keyboard()
    preload_period = clock.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='preload_period')
    
    # --- Initialize components for Routine "null" ---
    nullCrosshair = visual.TextStim(win=win, name='nullCrosshair',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.06, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "movie" ---
    key_resp = keyboard.Keyboard()
    
    # --- Initialize components for Routine "rest" ---
    crosshair = visual.TextStim(win=win, name='crosshair',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.06, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_rest = keyboard.Keyboard()
    
    # --- Initialize components for Routine "thanks" ---
    goodbye = visual.TextStim(win=win, name='goodbye',
        text="That's it!\n\nThanks!",
        font='Open Sans',
        pos=(0, 0), height=0.06, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    if globalClock is None:
        globalClock = core.Clock()  # to track the time since experiment started
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6)
    
    # --- Prepare to start Routine "dialogue" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    dialogueComponents = []
    for thisComponent in dialogueComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "dialogue" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in dialogueComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "dialogue" ---
    for thisComponent in dialogueComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "dialogue" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "instructions" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instructions.started', globalClock.getTime())
    scan_trigger.keys = []
    scan_trigger.rt = []
    _scan_trigger_allKeys = []
    # keep track of which components have finished
    instructionsComponents = [tapping_instructions, scan_trigger, preload_period]
    for thisComponent in instructionsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instructions" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *tapping_instructions* updates
        
        # if tapping_instructions is starting this frame...
        if tapping_instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            tapping_instructions.frameNStart = frameN  # exact frame index
            tapping_instructions.tStart = t  # local t and not account for scr refresh
            tapping_instructions.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(tapping_instructions, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'tapping_instructions.started')
            # update status
            tapping_instructions.status = STARTED
            tapping_instructions.setAutoDraw(True)
        
        # if tapping_instructions is active this frame...
        if tapping_instructions.status == STARTED:
            # update params
            pass
        
        # *scan_trigger* updates
        waitOnFlip = False
        
        # if scan_trigger is starting this frame...
        if scan_trigger.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            scan_trigger.frameNStart = frameN  # exact frame index
            scan_trigger.tStart = t  # local t and not account for scr refresh
            scan_trigger.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(scan_trigger, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'scan_trigger.started')
            # update status
            scan_trigger.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(scan_trigger.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(scan_trigger.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if scan_trigger.status == STARTED and not waitOnFlip:
            theseKeys = scan_trigger.getKeys(keyList=['t','5'], ignoreKeys=["escape"], waitRelease=False)
            _scan_trigger_allKeys.extend(theseKeys)
            if len(_scan_trigger_allKeys):
                scan_trigger.keys = _scan_trigger_allKeys[-1].name  # just the last key pressed
                scan_trigger.rt = _scan_trigger_allKeys[-1].rt
                scan_trigger.duration = _scan_trigger_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        # *preload_period* period
        
        # if preload_period is starting this frame...
        if preload_period.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            preload_period.frameNStart = frameN  # exact frame index
            preload_period.tStart = t  # local t and not account for scr refresh
            preload_period.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(preload_period, 'tStartRefresh')  # time at next scr refresh
            # update status
            preload_period.status = STARTED
            preload_period.start(1)
        elif preload_period.status == STARTED:  # one frame should pass before updating params and completing
            # Updating other components during *preload_period*
            taps = visual.MovieStim3(
                win=win, name='taps', units='pix',
                noAudio = False,
                filename=condition,
                ori=0.0, pos=(0, 0), opacity=None,
                loop=True, anchor='center',
                depth=-3.0,
                )
            # Component updates done
            preload_period.complete()  # finish the static period
            preload_period.tStop = preload_period.tStart + 1  # record stop time
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructionsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions" ---
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('instructions.stopped', globalClock.getTime())
    # check responses
    if scan_trigger.keys in ['', [], None]:  # No response was made
        scan_trigger.keys = None
    thisExp.addData('scan_trigger.keys',scan_trigger.keys)
    if scan_trigger.keys != None:  # we had a response
        thisExp.addData('scan_trigger.rt', scan_trigger.rt)
        thisExp.addData('scan_trigger.duration', scan_trigger.duration)
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "null" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('null.started', globalClock.getTime())
    # keep track of which components have finished
    nullComponents = [nullCrosshair]
    for thisComponent in nullComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "null" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *nullCrosshair* updates
        
        # if nullCrosshair is starting this frame...
        if nullCrosshair.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            nullCrosshair.frameNStart = frameN  # exact frame index
            nullCrosshair.tStart = t  # local t and not account for scr refresh
            nullCrosshair.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(nullCrosshair, 'tStartRefresh')  # time at next scr refresh
            # update status
            nullCrosshair.status = STARTED
            nullCrosshair.setAutoDraw(True)
        
        # if nullCrosshair is active this frame...
        if nullCrosshair.status == STARTED:
            # update params
            pass
        
        # if nullCrosshair is stopping this frame...
        if nullCrosshair.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > nullCrosshair.tStartRefresh + nullPeriod-frameTolerance:
                # keep track of stop time/frame for later
                nullCrosshair.tStop = t  # not accounting for scr refresh
                nullCrosshair.frameNStop = frameN  # exact frame index
                # update status
                nullCrosshair.status = FINISHED
                nullCrosshair.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in nullComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "null" ---
    for thisComponent in nullComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('null.stopped', globalClock.getTime())
    # the Routine "null" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    blocks = data.TrialHandler(nReps=numBlocks, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='blocks')
    thisExp.addLoop(blocks)  # add the loop to the experiment
    thisBlock = blocks.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            globals()[paramName] = thisBlock[paramName]
    
    for thisBlock in blocks:
        currentLoop = blocks
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                inputs=inputs, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
        if thisBlock != None:
            for paramName in thisBlock:
                globals()[paramName] = thisBlock[paramName]
        
        # --- Prepare to start Routine "movie" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('movie.started', globalClock.getTime())
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # Run 'Begin Routine' code from nestedlist
        win.mouseVisible = False
        # keep track of which components have finished
        movieComponents = [taps, key_resp]
        for thisComponent in movieComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "movie" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *taps* updates
            
            # if taps is starting this frame...
            if taps.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                taps.frameNStart = frameN  # exact frame index
                taps.tStart = t  # local t and not account for scr refresh
                taps.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(taps, 'tStartRefresh')  # time at next scr refresh
                # update status
                taps.status = STARTED
                taps.setAutoDraw(True)
            
            # if taps is stopping this frame...
            if taps.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > taps.tStartRefresh + blockLength-frameTolerance:
                    # keep track of stop time/frame for later
                    taps.tStop = t  # not accounting for scr refresh
                    taps.frameNStop = frameN  # exact frame index
                    # update status
                    taps.status = FINISHED
                    taps.setAutoDraw(False)
            
            # *key_resp* updates
            waitOnFlip = False
            
            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if key_resp is stopping this frame...
            if key_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp.tStartRefresh + blockLength-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp.tStop = t  # not accounting for scr refresh
                    key_resp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp.stopped')
                    # update status
                    key_resp.status = FINISHED
                    key_resp.status = FINISHED
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['1'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = [key.name for key in _key_resp_allKeys]  # storing all keys
                    key_resp.rt = [key.rt for key in _key_resp_allKeys]
                    key_resp.duration = [key.duration for key in _key_resp_allKeys]
                    # was this correct?
                    if (key_resp.keys == str("'1'")) or (key_resp.keys == "'1'"):
                        key_resp.corr = 1
                    else:
                        key_resp.corr = 0
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in movieComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "movie" ---
        for thisComponent in movieComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('movie.stopped', globalClock.getTime())
        taps.stop()  # ensure movie has stopped at end of Routine
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
            # was no response the correct answer?!
            if str("'1'").lower() == 'none':
               key_resp.corr = 1;  # correct non-response
            else:
               key_resp.corr = 0;  # failed to respond (incorrectly)
        # store data for blocks (TrialHandler)
        blocks.addData('key_resp.keys',key_resp.keys)
        blocks.addData('key_resp.corr', key_resp.corr)
        if key_resp.keys != None:  # we had a response
            blocks.addData('key_resp.rt', key_resp.rt)
            blocks.addData('key_resp.duration', key_resp.duration)
        # Run 'End Routine' code from nestedlist
        win.mouseVisible = False
        # the Routine "movie" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "rest" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('rest.started', globalClock.getTime())
        key_resp_rest.keys = []
        key_resp_rest.rt = []
        _key_resp_rest_allKeys = []
        # Run 'Begin Routine' code from appendResponses
        if not key_resp.keys:
            nestedlist.append([])
        else:
            nestedlist.append(key_resp.keys)
        # keep track of which components have finished
        restComponents = [crosshair, key_resp_rest]
        for thisComponent in restComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "rest" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *crosshair* updates
            
            # if crosshair is starting this frame...
            if crosshair.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                crosshair.frameNStart = frameN  # exact frame index
                crosshair.tStart = t  # local t and not account for scr refresh
                crosshair.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(crosshair, 'tStartRefresh')  # time at next scr refresh
                # update status
                crosshair.status = STARTED
                crosshair.setAutoDraw(True)
            
            # if crosshair is active this frame...
            if crosshair.status == STARTED:
                # update params
                pass
            
            # if crosshair is stopping this frame...
            if crosshair.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > crosshair.tStartRefresh + blockLength-frameTolerance:
                    # keep track of stop time/frame for later
                    crosshair.tStop = t  # not accounting for scr refresh
                    crosshair.frameNStop = frameN  # exact frame index
                    # update status
                    crosshair.status = FINISHED
                    crosshair.setAutoDraw(False)
            
            # *key_resp_rest* updates
            waitOnFlip = False
            
            # if key_resp_rest is starting this frame...
            if key_resp_rest.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_rest.frameNStart = frameN  # exact frame index
                key_resp_rest.tStart = t  # local t and not account for scr refresh
                key_resp_rest.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_rest, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_rest.started')
                # update status
                key_resp_rest.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_rest.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_rest.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if key_resp_rest is stopping this frame...
            if key_resp_rest.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp_rest.tStartRefresh + blockLength-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp_rest.tStop = t  # not accounting for scr refresh
                    key_resp_rest.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp_rest.stopped')
                    # update status
                    key_resp_rest.status = FINISHED
                    key_resp_rest.status = FINISHED
            if key_resp_rest.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_rest.getKeys(keyList=['1'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_rest_allKeys.extend(theseKeys)
                if len(_key_resp_rest_allKeys):
                    key_resp_rest.keys = [key.name for key in _key_resp_rest_allKeys]  # storing all keys
                    key_resp_rest.rt = [key.rt for key in _key_resp_rest_allKeys]
                    key_resp_rest.duration = [key.duration for key in _key_resp_rest_allKeys]
                    # was this correct?
                    if (key_resp_rest.keys == str("'1'")) or (key_resp_rest.keys == "'1'"):
                        key_resp_rest.corr = 1
                    else:
                        key_resp_rest.corr = 0
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in restComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "rest" ---
        for thisComponent in restComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('rest.stopped', globalClock.getTime())
        # check responses
        if key_resp_rest.keys in ['', [], None]:  # No response was made
            key_resp_rest.keys = None
            # was no response the correct answer?!
            if str("'1'").lower() == 'none':
               key_resp_rest.corr = 1;  # correct non-response
            else:
               key_resp_rest.corr = 0;  # failed to respond (incorrectly)
        # store data for blocks (TrialHandler)
        blocks.addData('key_resp_rest.keys',key_resp_rest.keys)
        blocks.addData('key_resp_rest.corr', key_resp_rest.corr)
        if key_resp_rest.keys != None:  # we had a response
            blocks.addData('key_resp_rest.rt', key_resp_rest.rt)
            blocks.addData('key_resp_rest.duration', key_resp_rest.duration)
        # Run 'End Routine' code from appendResponses
        if not key_resp_rest.keys:
            nestedrestlist.append([])
        else:
            nestedrestlist.append(key_resp_rest.keys)
        # the Routine "rest" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed numBlocks repeats of 'blocks'
    
    
    # --- Prepare to start Routine "thanks" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('thanks.started', globalClock.getTime())
    # keep track of which components have finished
    thanksComponents = [goodbye]
    for thisComponent in thanksComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "thanks" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 2.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *goodbye* updates
        
        # if goodbye is starting this frame...
        if goodbye.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            goodbye.frameNStart = frameN  # exact frame index
            goodbye.tStart = t  # local t and not account for scr refresh
            goodbye.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(goodbye, 'tStartRefresh')  # time at next scr refresh
            # update status
            goodbye.status = STARTED
            goodbye.setAutoDraw(True)
        
        # if goodbye is active this frame...
        if goodbye.status == STARTED:
            # update params
            pass
        
        # if goodbye is stopping this frame...
        if goodbye.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > goodbye.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                goodbye.tStop = t  # not accounting for scr refresh
                goodbye.frameNStop = frameN  # exact frame index
                # update status
                goodbye.status = FINISHED
                goodbye.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in thanksComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "thanks" ---
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('thanks.stopped', globalClock.getTime())
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-2.000000)
    # Run 'End Experiment' code from feedback_to_experimenter
    print("number of taps per block:")
    for index, item in enumerate(nestedlist):
        print("block "+ str(index+1), ": " + str(len(item)))
        
    print("")
    
    print("number of taps per REST block:")
    for index, item in enumerate(nestedrestlist):
        print("block "+ str(index+1), ": " + str(len(item)))
        
    print("")
    
    # mark experiment as finished
    endExperiment(thisExp, win=win, inputs=inputs)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, inputs=None, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()


def quit(thisExp, win=None, inputs=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    inputs : dict
        Dictionary of input devices by name.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    inputs = setupInputs(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win, 
        inputs=inputs
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win, inputs=inputs)
