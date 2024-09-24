import adsk.core, adsk.fusion, adsk.cam, traceback, math


#SETTINGS
#number of spline vertices per tooth - can get laggy with more, worse gear performance with less
pointsPerTooth=12
#0-1 rounds gear profile - worse performance but can  be usd for asthetic reasons
rounding = 0.0

#app.log("basic gear script started")

# Define the golden ratio (phi)
phi = (1 + math.sqrt(5)) / 2 * (1-rounding)

# Squarish sin wave gear profile function
def sqSin(x):
    return math.sin(x) / (math.sin(x)**2 + 1)

# Square cos wave function
def sqCos(x):
    return sqSin(x+math.pi/2)
    #return math.cos(x) / (math.cos(x)**2 + 1)

# Function to calculate the polar radius 'r'
def calculate_r(theta, n, R):
    # Calculate 'a' using the provided equation
    a = (phi / n) * R * 2 *(1-rounding)
    
    # Calculate the inner expression that compensates for arc length
    theta_comp = theta * n - sqSin(theta * n) * (-a / R)
    
    # Calculate r using the Teeth Profile
    r = a * sqCos(theta_comp) + R
    
    return r

def create_simple_sinusoidal_gear(r, z):
    # Access the application and user interface
    app = adsk.core.Application.get()
    ui = app.userInterface

    # Create a new sketch
    design = app.activeProduct
    rootComp = design.rootComponent
    sketches = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    # Gear profile points
    points = adsk.core.ObjectCollection.create()
    num_points=z*pointsPerTooth

    #optimal value for a the teeth amplitude
    a = (phi / z) *r * 2

    for i in range(num_points):
        #calculate angle for new point
        theta = 2 * math.pi * i / num_points
    
        # Calculate the inner expression that compensates for arc length
        theta_comp = theta * z - sqSin(theta * z) * (-a / r)
    
        # Calculate distance from center using the sqare teeth profile
        R = a * sqCos(theta_comp) + r

        #calculate x and y from distance, angle
        x = R * math.cos(theta)
        y = R * math.sin(theta)

        # Create the gear profile
        point = adsk.core.Point3D.create(x, y, 0)
        points.add(point)
        # Create the spline curve
    spline = sketch.sketchCurves.sketchFittedSplines.add(points)
    #completes the spline loopp
    spline.isClosed =True


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Create a new command definition
        cmdDef = ui.commandDefinitions.itemById('gearUI')
        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition('gearUI', 'Gear Generator', 'Generates a simple gear')

        # Connect to the command created event
        onCommandCreated = GearUICmdCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Execute the command
        cmdDef.execute()

        # Keep the script running
        adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class GearUICmdCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            inputs = cmd.commandInputs

            # Create inputs for radius and number of teeth
            radiusInput = inputs.addValueInput('module', 'Module', 'cm', adsk.core.ValueInput.createByReal(10))
            radiusInput.tooltip = 'Pitch Diameter = Module * # of teeth. Gears must have the same modulus to mesh properly'
            inputs.addIntegerSpinnerCommandInput('numTeeth', 'Number of Teeth', 1, 1000, 1, 24)

            # Connect to the execute event
            onExecute = GearUICmdExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)

            #Connects the event to end this script when done
            onDestroy = GearCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            handlers.append(onDestroy)
        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class GearUICmdExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            inputs = cmd.commandInputs

            # Get the values of the inputs
            m = inputs.itemById('module').value
            z = inputs.itemById('numTeeth').value

            if (m==0):
                ui.messageBox('script failed: module should not be zero')
            else:
                #calculate radius
                r=m*z/2

                # Pass the input values to the gear generation function
                create_simple_sinusoidal_gear(r,z)

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class GearCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)

            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

handlers = []
