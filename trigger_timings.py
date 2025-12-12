#!/usr/bin/env python

# 20251211 Ver 1.0, S Torrisi, UCSF

from psychopy import visual, core, event
from datetime import datetime
import statistics, csv

# Create window (required for event capture)
win = visual.Window([800, 600], color='black', units='pix')
text = visual.TextStim(win, text='Waiting for triggers...\n\nPress ESC to quit and save', 
                       color='white', height=25)
# Initialize
clock = core.Clock()
triggers = []
print("Waiting for triggers... Press 'escape' to quit and save.")

while True:
    text.draw()
    win.flip()
    
    # usual scanner triggers through a Current Designs interface
    keys = event.getKeys(keyList=['t', '5', 'escape'], timeStamped=clock)
    
    for key, timestamp in keys:
        if key == 'escape':
            # inter-trigger intervals (TRs)
            trs = []
            if len(triggers) >= 2:
                for i in range(1, len(triggers)):
                    tr = triggers[i][1] - triggers[i-1][1]
                    trs.append(tr)  # Keep full precision for calculations
            
            # quick summary stats
            if trs:
                mean_tr = statistics.mean(trs)
                stdev_tr = statistics.stdev(trs) if len(trs) > 1 else 0
            else:
                mean_tr = 0
                stdev_tr = 0
            
            # save CSV
            filename = f"trigger_timings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Trigger', 'Timestamp', 'TR (seconds)'])
                for i, trigger in enumerate(triggers):
                    if i == 0:
                        writer.writerow([trigger[0], trigger[1], ''])
                    else:
                        writer.writerow([trigger[0], trigger[1], round(trs[i-1], 5)])
                
                # save summary stats
                writer.writerow([])
                writer.writerow(['Mean TR', round(mean_tr, 5)])
                writer.writerow(['StDev TR', round(stdev_tr, 5)])
                writer.writerow(['Number of Triggers', len(triggers)])
            
            print(f"\nSaved {len(triggers)} triggers to {filename}")
            print(f"Mean TR: {mean_tr:.5f}s")
            print(f"StDev TR: {stdev_tr:.5f}s")
            win.close()
            core.quit()
        else:
            triggers.append([key, round(timestamp, 5)])
            print(f"Trigger '{key}' at {timestamp:.5f}s")
            text.text = f'Triggers received: {len(triggers)}\n\nLast: "{key}" at {timestamp:.5f}s\n\nPress ESC to quit and save'
    
    core.wait(0.001)  # Small wait to prevent CPU overload
