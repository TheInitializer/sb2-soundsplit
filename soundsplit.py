#pylint:disable=C0103
"""
sb2-soundsplit
--------------
splits audio files into little bits and puts them in an sb2 file
so you can make a music player or something in scratch for whatever reason
idk I was bored

by __init__
jan 24 2017

thx blob8108/tjvr for the kurt library
it's really good
pydub is also really good

mit license because I like it
"""

import os
import argparse
import kurt
import PIL
from pydub import AudioSegment
from pydub.utils import make_chunks

if __name__ == "__main__":
    # get cmdline args
    parser = argparse.ArgumentParser()  # whaaaa there's a built in library for this
    parser.add_argument("audio_file", help="Path to audio file (wav)")
    parser.add_argument("time_ms", help="Time for each segment of the sound (ms)",
                        type=int)
    args = parser.parse_args()    # omg I barely even have to write code anymore

    # create kurt project
    project = kurt.Project()
    sprite = kurt.Sprite(project, "Player")

    # dummy costume
    pil_image = PIL.Image.new("RGBA", (480, 360))
    scratch_image = kurt.Image(pil_image)
    costume = kurt.Costume("Player", scratch_image)
    sprite.costumes.append(costume)

    # more stuff
    names = []

    # load audio file
    song = AudioSegment.from_wav(args.audio_file)
    length = len(song)

    # split into chunks
    # numtimes = -(-length // args.time_ms) # ceiling division hax
    # song_bits = []
    # for i in range(numtimes):
    #     time = args.time_ms * i
    #     song_bits.append(song[time-1:time])

    # I realized pydub has a built in method for this
    # of course, it's a python module, so everything's done for you
    # (plus the above code didn't exactly work)

    song_bits = make_chunks(song, args.time_ms)  # easy af

    # put in the scratch
    for j, i in enumerate(song_bits):
        # I tried to get kurt to accept the raw data but it didn't want to :(
        i.set_channels(1).export("temp/bit{0}.wav".format(j), format="wav", bitrate="177k") # scratch is weird
        scratch_sound = kurt.Sound.load("temp/bit{0}.wav".format(j))
        sprite.sounds.append(scratch_sound)
        names.append("bit{0}".format(j))

    scratch_names = kurt.List(items=names)
    sprite.lists["names"] = scratch_names

    project.sprites.append(sprite)
    project.save("project.sb2")
