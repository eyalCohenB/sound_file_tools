# plotWavApp_v1.py

This script is designed to conveniently display `.wav` files with one or more channels of input.
It supports a simple user friendly interface.

## How it works

1. run `plotWavApp_v1.py` at your local ide or cmd
2. Click the `Upload`Button.
   - choose the  `.wav` file you want to view.

3. Click `View Data` Button.

# signal_generator.py

This script is designed to conviniently create `.wav` files (currently cmd version).
The user may choose from 3 types of signals:
- chirp - A normal chirp (single or repetative)
- cw - Continuous wave (single or repetative)
- cwinc - Continuous wave that increments frequency every x pulses (currently only step of incrementation available is +1khz)

## How it works

1. Run `signal_generator.py` in your local IDE or command line.
2. Follow the on-screen instructions:
   - Enter the sample rate (in kHz).
   - Input the starting frequency (in kHz).
   - Input the ending frequency (in kHz).
   - Specify the signal duration (in seconds).
   - Specify the silence duration between signals (in seconds).
   - Set the repeat value (an integer for the number of times the signal is repeated at each frequency).
   
3. After all the parameters are entered, the script will generate the `.wav` file based on your inputs. The type of signal (chirp, continuous wave, or incrementing continuous wave) will be created as specified, and saved to your working directory.
