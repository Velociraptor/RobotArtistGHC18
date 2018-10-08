# Quickstart
You can view the SVG file used to produce the chassis used in the workshop
[here](chassis.svg). It should be rendered at 72 pts/inch - red lines indicate
cuts in the material (by e.g. a laser cutter).

# Modifying
The [chassis design](chassis.svg) was produced by
[a python script](designs/chassis.py)! To run the script, first install the
dependencies in your python 2.7 compatible python environment via
`pip install -r requirements.txt`, and the run `python -m designs.chassis`. Most
aspects of the design are parameterized at the start of the file.
