Quick start
-----------


.. raw:: html

   <script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
   <script>
     kofiWidgetOverlay.draw('mrzahaki', {
       'type': 'floating-chat',
       'floating-chat.donateButton.text': 'Support me',
       'floating-chat.donateButton.background-color': '#2980b9',
       'floating-chat.donateButton.text-color': '#fff'
     });
   </script>



Audio playback
^^^^^^^^^^^^^^

.. code-block:: python

    import sudio

    su = sudio.Master()
    su.add('baroon.mp3')
    su.echo('baroon')

The record with the name of baroon will be played on the stdout audio stream.

Audio Manipulation
^^^^^^^^^^^^^^^^^^

Time Domain Slicing
"""""""""""""""""""

You can easily slice audio files to play specific segments:

.. code-block:: python

    su = sudio.Master()
    song = su.add('baroon.mp3')
    su.echo(song[12: 27.66])

    # Play from 30 seconds to the end
    su.echo(song[30:])

    # Play the first 15 seconds
    su.echo(song[:15])

Combining Audio Segments
""""""""""""""""""""""""

You can join multiple segments of audio:

.. code-block:: python

    su = sudio.Master()
    rec = su.add('baroon.mp3')

    # method 1
    su.echo(rec[12: 27.66, 65: 90])

    # method 2
    result = rec[12: 27.66].join(rec[65: 90])

    # Combine multiple segments
    medley = song[10:20].join(song[40:50], song[70:80])
    su.echo(medley)

The audio record is split into two parts, the first one 12-27.66 seconds, and the last one 65-90 seconds, then the sliced records are merged and played in the stream.

Audio Basic Effects
^^^^^^^^^^^^^^^^^^^

Volume Adjustment
"""""""""""""""""

Adjust the volume of an audio segment:

.. code-block:: python

    su = sudio.Master()
    song = su.add('song.mp3')

    # Double the volume
    loud_segment = song[10:20] * 2

    # Halve the volume
    quiet_segment = song[30:40] / 2

    su.echo(loud_segment.join(quiet_segment))

Applying Filters
""""""""""""""""

Apply frequency filters to audio:

.. code-block:: python

    su = sudio.Master()
    song = su.add('song.mp3')

    # Apply a low-pass filter (keep frequencies below 1000 Hz)
    low_pass = song[:'1000']

    # Apply a high-pass filter (keep frequencies above 500 Hz)
    high_pass = song['500':]

    # Apply a band-pass filter (keep frequencies between 500 Hz and 2000 Hz)
    band_pass = song['500':'2000']

    su.echo(low_pass.join(high_pass, band_pass))

Complex Slicing
"""""""""""""""

.. code-block:: python

    su = sudio.Master()
    baroon = su.add('baroon.mp3')
    su.echo(baroon[5:10, :'1000', 10: 20, '1000': '5000'])

In the example above, a low-pass filter with a cutoff frequency of 1 kHz is applied to the record from 5 to 10 seconds, then a band-pass filter is applied from 10 to 20 seconds, and finally they are merged.

Custom Fade-In and Mixing
"""""""""""""""""""""""""

.. code-block:: python

    import sudio
    from sudio.types import SampleFormat
    import numpy as np

    su = sudio.Master()
    song = su.add('example.mp3')

    fade_length = int(song.get_sample_rate() * 5)  # 5-second fade
    fade_in = np.linspace(0, 1, fade_length)

    with song.unpack(astype=SampleFormat.FLOAT32) as data:
        data[:, :fade_length] *= fade_in
        song.set_data(data)

    gain_duration = song.get_duration() / 2
    song += song[:gain_duration, :'100'] * .3
    su.echo(song)
    su.export(song, 'modified_song.ogg')

This example shows how you can tweak audio using the sudio library. 
We start with a simple 5-second fade-in by gradually increasing the volume from 0 to full over that time. 
The audio data is unpacked in FLOAT32 for more accurate processing, and after applying the fade, we pack it back. 
Next, we take the first half of the track, apply a low-pass filter to keep only the lower frequencies, 
reduce its volume by 70%, and mix it back into the original. 
The modified track is then played with echo() and saved as an .ogg file. 
This example highlights how sudio lets you easily combine time-based edits (like fades) with frequency-based tweaks 
for creative audio manipulation.

Audio Analysis
^^^^^^^^^^^^^^

Perform simple analysis on audio files:

.. code-block:: python

    su = sudio.Master()
    song = su.add('song.mp3')

    # Get audio duration
    duration = song.get_duration()
    print(f"Song duration: {duration} seconds")

    # Get sample rate
    sample_rate = song.get_sample_rate()
    print(f"Sample rate: {sample_rate} Hz")

    # Get number of channels
    channels = song.get_nchannels()
    print(f"Number of channels: {channels}")


Audio Format Conversion and Encoding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's explore how sudio handles different audio formats. We'll convert between MP3, WAV, FLAC, and OGG, and throw in some audio tweaks along the way.

.. code-block:: python

    import sudio
    from sudio.types import FileFormat

    su = sudio.Master()

    # Load any audio file - MP3, WAV, OGG, or FLAC
    record = su.add('original_song.mp3')

    # Slice and save as WAV
    su.export(record[10.5: 30], 'cool_snippet.wav')

    # Quiet it down and save as high-quality FLAC
    su.export(record / 2, format=FileFormat.FLAC, quality=0.8)

    # Convert to medium-quality OGG
    su.export(record, 'medium_quality.ogg', quality=0.5)

    # Convert to medium-quality mp3
    su.export(record, 'medium_quality.mp3', quality=0.5, bitrate=64)

Pro tip: The second export creates a file named after the original, but with a .flac extension.

Remember, converting between lossy formats (like MP3 to OGG) might not sound great. For best results, start with high-quality or lossless files when possible.



Mixing and Shifting Tracks
^^^^^^^^^^^^^^^^^^^^^^^^^^

When adding two Wrap objects, the combined audio will be as long as the longer one, mixing overlapping parts. Adding a constant shifts the waveform up while keeping the original duration. This allows for flexible audio mixing and simple DC offset adjustments.

.. code-block:: python

    import sudio
    import numpy as np

    su = sudio.Master()

    # Add two audio files
    song1 = su.add('song1.mp3') 
    song2 = su.add('song2.mp3') 

    # Add the two songs
    combined = song1 + song2

    # Play the combined audio
    su.echo(combined)

    # Add a constant value to shift the audio
    shifted = song1 + 0.1

    # Play the shifted audio
    su.echo(shifted)

    # Print durations
    print(f"Song1 duration: {song1.get_duration()} seconds")
    print(f"Song2 duration: {song2.get_duration()} seconds")
    print(f"Combined duration: {combined.get_duration()} seconds")
    print(f"Shifted duration: {shifted.get_duration()} seconds")

Audio Streaming
^^^^^^^^^^^^^^^

Basic Streaming with Pause and Resume
"""""""""""""""""""""""""""""""""""""

This example demonstrates how to control audio playback using the sudio library, including starting, pausing, resuming, and stopping a stream.

.. code-block:: python

    import sudio
    import time

    # Initialize the audio master
    su = sudio.Master()
    su.start()

    # Add an audio file to the master
    record = su.add('example.mp3')
    stream = su.stream(record)

    # Enable stdout echo
    su.echo()

    # Start the audio stream
    stream.start()
    print(f"Current playback time: {stream.time} seconds")

    # Pause the playback after 5 seconds
    time.sleep(5)
    stream.pause()
    print("Paused playback")

    # Resume playback after 2 seconds
    time.sleep(2)
    stream.resume()
    print("Resumed playback")

    # Stop playback after 5 more seconds
    time.sleep(5)
    stream.stop()
    print("Stopped playback")

This script showcases basic audio control operations, allowing you to manage playback with precise timing.

Basic Streaming with Jumping to Specific Times in the Audio
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This example illustrates how to start playback and jump to a specific time in an audio file.

.. code-block:: python

    import sudio
    import time

    # Initialize the audio master
    su = sudio.Master()
    su.start()

    # Add a long audio file to the master
    record = su.add('long_audio.mp3')
    stream = su.stream(record)

    # Enable stdout echo
    su.echo()

    # Start the audio stream
    stream.start()
    print(f"Starting playback at: {stream.time} seconds")

    # Jump to 30 seconds into the audio after 5 seconds of playback
    time.sleep(5)
    stream.time = 30
    print(f"Jumped to: {stream.time} seconds")

    # Continue playback for 10 more seconds
    time.sleep(10)
    print(f"Current playback time: {stream.time} seconds")

    # Stop the audio stream
    stream.stop()

This script demonstrates how to navigate within an audio file, which is useful for long audio content or when specific sections need to be accessed quickly.

Streaming with Volume Control
"""""""""""""""""""""""""""""

This example shows how to dynamically control the volume of an audio stream using a custom pipeline.

.. code-block:: python

    import sudio
    import time
    import sudio.types

    # Initialize the audio master with a specific input device
    su = sudio.Master(std_input_dev_id=2)
    su.start()

    # Add an audio file to the master
    record = su.add('example.mp3')
    stream = su.stream(record)

    # Define a function to adjust the volume
    def adjust_volume(data, args):
        return data * args['volume']

    # Create a pipeline and append the volume adjustment function
    pip = sudio.Pipeline()
    pip.append(adjust_volume, args={'volume': 1.0})

    # Start the pipeline
    pip.start()

    # Add the pipeline to the master
    pipeline_id = su.add_pipeline(pip, process_type=sudio.types.PipelineProcessType.MAIN)
    su.set_pipeline(pipeline_id)

    # Enable stdout echo
    su.echo()

    # Start the audio stream
    stream.start()
    print("Playing at normal volume")
    time.sleep(10)

    # Adjust the volume to 50%
    pip.update_args(adjust_volume, {'volume': 0.5})
    print("Reduced volume to 50%")
    time.sleep(10)

    # Restore the volume to normal
    pip.update_args(adjust_volume, {'volume': 1.0})
    print("Restored normal volume")
    time.sleep(10)

    # Stop the audio stream
    stream.stop()

This example introduces a more complex setup using a custom pipeline to dynamically adjust the audio volume during playback. It's particularly useful for applications requiring real-time audio processing or user-controlled volume adjustments.
