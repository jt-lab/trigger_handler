<img src="https://github.com/jeti182/trigger_handler/blob/main/logo.svg?raw=true" width="200" />


# trigger_handler

In the wake of the COVID-19 pandemic, many experimental psychology and neuroscience labs have shifted their experiments to browser-based online experiments. These are typically implemented in JavaScript-based frameworks such as [jsPsych](https://www.jspsych.org/) or [OSWeb](https://osdoc.cogsci.nl/3.2/manual/osweb/#osweb). When researchers move back into the lab, they might want to use their new stock of browser-based experiments to run them in the lab or base new experiments on these implementations. In principle, they can easily be brought back to the lab because JavaScript-based experiments can be executed locally on any PC with a modern web browser. However, many lab use cases include interaction with other lab equipment. For instance, one might want to conduct a former online experiment in the lab now with eye tracking. This requires sending synchronisation triggers to the eye tracking setup, which runs on another PC and records corresponding markers in its log file. Such triggering is typically handled via the parallel port, which cannot be accessed from the browser. ```trigger_handler``` provides a workaround for this: A small Python script opens a (local) webserver. Then the 'local online' experiment can sent a special request to the server, which then sends a corresponding trigger via the parallel port.

## Setup

```trigger_hadnler``` is a single brief Python script: [trigger_handler.py](trigger_handler.py). 

Requirements:

* Python: If you don't have a Python environment on the PC on which you want to run the experiment (and if this is a Windows machine), you can use the portable Python installation (ẀinPython) https://winpython.github.io/. It contains everything that is needed for ```trigger_handler``` can be easily copied to lab-PCs, and can be used without installation. 

* Parallel port DLL: For accessing the parallel port, ```trigger_handler``` needs the DLL ```inpoutx64.dll``` (on a 64-bit system). If you are running a 32-bit Python, you need ```inpout32.dll``` (and you need to make the respective change in [trigger_handler.py](trigger_handler.py)). Copy these DLLs into the same folder as [trigger_handler.py](trigger_handler.py). Try to find these DLLs in your systems DLL directories or search for them on the web and download them. If you want to use ```trigger_handler``` on a Linux or Mac system, you will need to replace the loading and the calls of the ```inpout``` DLLs with that of a system-specific parallel port library. 

## Configuration

For convenience, the configuration of ```trigger_handler``` can be adjusted directly in [trigger_handler.py](trigger_handler.py)):

Adjust the following constants:

```LPT_INTERFACE = 0xA060```: Provide the address of the parallel port device as a hexadecimal number (here 0xA060). You can find the parallel port card address (on a Windows PC) by opening the device manager in the system control center and navigating to the parallel port card. 

```HOST = '127.0.0.1'```: The IP address of the trigger_handler server. If you run it on the same PC as the experiment, this should stay '127.0.0.1'. If you run the handler on another PC in the network, enter its IP address here.

```PORT = 8000```: The port on which the server listens. If you change the port (and/or the HOST constant), you will have to adjust the calls in the examples below accordingly.

## Starting the trigger_handler

When you start the trigger_handler in a terminal (i.e. ```python trigger_handler.py```), you will see some output: 
```
[Fail] Could not load Windows parallel port interface.
 * Serving Flask app "trigger_handler" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
```
This is mainly information from the Flask web server, but the first line tells you whether or not the parallel port interface was successfully opened. In the example above, this was not the case (I just ran it on my laptop that has no parallel port, hence the error). If you see this error, one source of it might be the wrong port address in the configuration section (see above). Check whether you really entered the correct port address. Also note, that it needs to be a hexadecimal number (starting with 0X) as an integer (don't put string quotes around it). If there is no ```[Fail]``` but ```[Success]``` in the first line, then trigger_handler is happily running, waiting to get requests for sending triggers.

## Testing trigger_handler & demo

In the following, I will outline some ways to test trigger_handler and to demonstrate how it works. To really appreciate the following examples, you need some device at the other end that is connected to your parallel port, and that will display whether or not triggers arrive. Here are some options:

* Install a program on the receiving PC that monitors the parallel port. There are plenty of these. Which one is best might depend on your operating system. If you google for phrases like "parallel port monitor windows", you will surely find something usable. 

* If the receiving PC controls an eye tracking setup, you can run the recording software to see if triggers are received. For instance, with SE Research EyeLink 1000 Plus, little numbers are displayed above the SR logo, which reflect the received triggers.

* If the receiving PC controls an EEG setup: Run the recording software. Typically markers will be inserted into the waveform display when triggers are received. Note: JavaScript-based experiments and trigger_handler will most likely not have the timing precision required for EEG experiments.

All the tests and demos described below require that the configuration is correct (see above), that the  PCs are linked properly with the parallel port cable, and you have started trigger_handler on the same PC from which you run the tests.

### Testing by manually calling the trigger URL:

To test whether the trigger is submitted between the stimulus PC and the receiving PC, you can try the following: When the trigger server is running, you can enter ```http://127.0.0.1:8000/trigger/X``` (with ```X``` being a number that identifies the trigger) into the address bar of your browser. You should then see the trigger (e.g. by the means described above) on the receiving PC.

### Testing triggers with test_triggers.html:

[test_triggers.html](test_triggers.html) is a small HTML file that can be used to test sending triggers. Just open ```test_triggers.html``` and click the buttons to send triggers. 

### Example with jsPsych: 
[demo_3_triggers.html](demo_3_triggers.html) is a modified version of the flanker task demo that comes with [jsPsych](https://www.jspsych.org/). Just copy the file into the ```examples/demos``` folder of your jsPsych installation and run it (e.g. via a local [JATOS](https://www.jatos.org). If you look at the source code, you can see that a function (calling ```fetch('http://127.0.0.1:8000/trigger/X')```) is assigned to the ```on_start``` callback of the trials so that a trigger is sent whenever a new trial starts.


## Integration of triggers in your JavaScript-based experiments

The tests and demos described above show how sending triggers can be integrated into your JavaScript-based experiments. In essence, you need to call ```fetch('http://127.0.0.1:8000/trigger/X')``` (with ```X``` being a number that identifies the trigger) at time/event for which you would like to execute the trigger.

## Important note: 

```trigger_handler``` was not thoroughly tested yet. Also, you will likely have to make changes to [trigger_handler.py](trigger_handler.py) to adjust it for your needs. Sending triggers in this way relies on the event handling inside the browser and the handling of network traffic on the PC. Consequently, the temporal precision will be rather low (compared to a genuine lab implementation of an experiment), and it still has to be tested how good or bad the timing actually is. Nevertheless, ```trigger_handler``` can hopefully be a starting point for developing specific solutions for several use cases.
