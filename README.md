# POETS
This implementation is meant to run on POETS (Partially Order Event Triggered Systems), and event-based massively parallel computing computing technique.
As such, the C implementation is stripped down and doesn't implement all C functions and capabilities. It also must be generated into an massive XML format describing every node state and functions.
This was done in the context of a thesis (cut short) about graph placement algorithms/strategies for POETS.

## generating code
To generate the appropriate XML for your code and specific starting state, run `./generator/generate.py`:
```
python generate.py [empty|gliders|<coords>] <width> <height> <max-gen> <output-cycle> [0|1]
    [empty|gliders|coords]:
      -empty: generate an empty grid
      -gliders: generate a looping grid of "gliders", great for benchmarking
      -<coords>: generate a starting state by spefying coordinates in a file, specify file path in <coords>
    <width>: width of the grid
    <height>: height of the grid
    <max_gen>: the total amount of generations to run before stopping the simulation
    <output-cycle>: every "output-cycle", cells send their state to the supervisor. Higher values lead to a smoother output, but run against the idea of decentralized memory and will perform poorly
    [0|1]:
      -1: include the first generation in the output
      -0: exclude the first generation from the output
```

## running the application
To run the application run the POETS orchestrator after connecting to a POETS box through `./orchestrate.sh` and run the following commands:

```
load /app = +"gol.xml"
tlink /app = *
place /tfill = *
compose /app = *
deploy /app = *
initialize /app = *
run /app = *
```

Alternatively, you can write all these commands to a text file and run the program through `./orchestrate -b path/of/file`

## interpreting output
`interpreter/interpret.py` uses ffmpeg to generate a video output from the specified output/log file.
```
python interpret.py <input> <output> [<gen>|v|f] <framerate(optional)>
    <input>: the input file to be interpreted
    <output>: name of output file, name of output directory if generating a video or all frame
    [<gen>|v|f]:
      -<gen>: specific generation to render to picture
      -v: generate video out of every generation
      -f: generate picture for all generations
    <framerate>: framerate of generated video
```
