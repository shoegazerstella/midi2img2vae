# source code: https://github.com/mathigatti/midi2img
from music21 import converter, instrument, note, chord
import os, sys, json
import numpy as np
from imageio import imwrite

def extractNote(element):
    return int(element.pitch.ps)

def extractDuration(element):
    return element.duration.quarterLength

def get_notes(notes_to_parse):

    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    durations = []
    notes = []
    start = []

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            if element.isRest:
                continue

            start.append(element.offset)
            notes.append(extractNote(element))
            durations.append(extractDuration(element))
                
        elif isinstance(element, chord.Chord):
            if element.isRest:
                continue
            for chord_note in element.notes:
                start.append(element.offset)
                durations.append(extractDuration(element))
                notes.append(extractNote(chord_note))

    return {"start":start, "pitch":notes, "dur":durations}

def midi2image(midi_path, save_img_path, save_as_image=False, mirror=False):
    mid = converter.parse(midi_path)

    instruments = instrument.partitionByInstrument(mid)

    data = {}

    try:
        i=0
        for instrument_i in instruments.parts:
            notes_to_parse = instrument_i.recurse()

            if instrument_i.partName is None:
                data["instrument_{}".format(i)] = get_notes(notes_to_parse)
                i+=1
            else:
                data[instrument_i.partName] = get_notes(notes_to_parse)

    except:
        notes_to_parse = mid.flat.notes
        data["instrument_0".format(i)] = get_notes(notes_to_parse)

    resolution = 0.25

    for instrument_name, values in data.items():
        # https://en.wikipedia.org/wiki/Scientific_pitch_notation#Similar_systems
        upperBoundNote = 127
        lowerBoundNote = 21
        maxSongLength = 100

        index = 0
        prev_index = 0
        repetitions = 0
        while repetitions < 1: #int(sys.argv[2]):
            if prev_index >= len(values["pitch"]):
                break

            matrix = np.zeros((upperBoundNote-lowerBoundNote,maxSongLength))

            pitchs = values["pitch"]
            durs = values["dur"]
            starts = values["start"]

            for i in range(prev_index,len(pitchs)):
                pitch = pitchs[i]

                dur = int(durs[i]/resolution)
                start = int(starts[i]/resolution)

                if dur+start - index*maxSongLength < maxSongLength:
                    for j in range(start,start+dur):
                        if j - index*maxSongLength >= 0:
                            matrix[pitch-lowerBoundNote,j - index*maxSongLength] = 255
                else:
                    prev_index = i
                    break
            
            if mirror is True:
                # flip the image
                matrix = np.flip(matrix, 1)
            
            if save_as_image is True:
                # convert img to uint8
                matrix = matrix.astype(np.uint8)

                if mirror is True:
                    savepath = os.path.join(save_img_path, midi_path.split("/")[-1].replace(".mid",f"_{instrument_name}_{index}_mir.png"))
                else:
                    savepath = os.path.join(save_img_path, midi_path.split("/")[-1].replace(".mid",f"_{instrument_name}_{index}.png"))
                
                imwrite(savepath, matrix)
                #imwrite(midi_path.split("/")[-1].replace(".mid",f"_{instrument_name}_{index}.png"),matrix)
            
            else:

                if mirror is True:
                    savepath = os.path.join(save_img_path, midi_path.split("/")[-1].replace(".mid",f"_{instrument_name}_{index}_mir.npy"))
                else:
                    savepath = os.path.join(save_img_path, midi_path.split("/")[-1].replace(".mid",f"_{instrument_name}_{index}.npy"))
                with open(savepath, 'wb') as f:
                    np.save(f, matrix)

            index += 1
            repetitions+=1

#import sys
#midi_path = sys.argv[1]
#midi2image(midi_path)
