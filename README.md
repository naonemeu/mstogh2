# mstogh2 - "Naonemeu Version"
Changse to them main version
* Converts "directly" from .chart, using raynebc's chart2mid and adding missing stuff with "adapt_chart2mid.py"
* Changed lots of "if msg.note == [note]" because chart2mid handles it differently from Moonscraper **(why?!?!)**
* Expanded fretmapping to 18 notes to be used with a "fremapping helper" tool soon(tm).

Made with much gambiarra

***
# mstogh2
MID tool using Python and Mido to convert Moonscraper RB2 export to GH2 MID, adding animations, lights, and fret mapping

This supports most of gh2 animations, lights, keyframes and fret mapping. Still doesn't have face-off sections and fret mapping for bass.

# What do I need to use this?
First you need to install Python and add it to %PATH%. Install mido with the command "pip install mido" in CMD or Windows Powershell and install Reaper for bugfixes*

Drop your mid file from moonscraper in the same folder the files are. Rename it to "notes.mid" and you are done to use it.
You can open "run.bat". This will give you some choices of what you want in your mid file or not, after this it will generate "notes_gh2.mid" that will contain all the animations converted. There is a bug that the mid is not "formatted" correctly, so you need to export it in reaper first to get all the things working in game.

# How to chart animations?
coming soon, for now, I have this doc:
https://docs.google.com/document/d/16MzEoC7JfNOcvqn8wyBBf4oiipJbx0h_/edit?usp=sharing&ouid=116981090282877738182&rtpof=true&sd=true
