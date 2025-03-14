---
myst:
   html_meta:
      "description": "ZEISS INSPECT 2025 App Python API Specification"
      "keywords": "Metrology, ZEISS INSPECT, Python API, GOM API, Scripting, Add-ons, Apps, Specification, Documentation"
    
   suppress_warnings:
      ['myst.header']
---

# ZEISS INSPECT App Python API documentation

Welcome to the ZEISS INSPECT Python API documentation. Here you can find a detailed documentation of a subset of the App programming specification. Please bear in mind, that recording commands with the script editor can be used to add new functions to your script.

```{note}
The module importing behavior changed with ZEISS INSPECT 2025. Previously, the API modules could be used without proper `import` statements due to their internal handling. Beginning with ZEISS INSPECT 2025, each module is a full featured native Python module and
must be properly imported before use!
```
## gom.api.addons

API for accessing the add-ons currently installed in the running software instance

This API enables access to the installed add-ons. Information about these add-ons can be
queried, add-on files and resources can be read and if the calling instance is a member of
one specific add-on, this specific add-on can be modified on-the-fly and during software
update processes.

### gom.api.addons.AddOn

Class representing a single add-on

This class represents a single add-on. Properties of that add-on can be queried from here.

#### gom.api.addons.AddOn.exists

```{py:function} gom.api.addons.AddOn.exists(path: str): bool

Check if the given file or directory exists in an add-on
:API version: 1
:param path: File path as retrieved by 'gom.api.addons.AddOn.get_file_list ()'
:type path: str
:return: 'true' if a file or directory with that name exists in the add-on
:rtype: bool
```

This function checks if the given file exists in the add-on

#### gom.api.addons.AddOn.get_content_list

```{py:function} gom.api.addons.AddOn.get_content_list(): list

Return the list of contents contained in the add-on
:API version: 1
:return: List of contents in that add-on (full path)
:rtype: list
```


#### gom.api.addons.AddOn.get_file

```{py:function} gom.api.addons.AddOn.get_file(): str

Return the installed add-on file
:API version: 1
:return: Add-on file path (path to the add-ons installed ZIP file) or add-on edit directory if the add-on is currently in edit mode.
:rtype: str
```

This function returns the installed ZIP file representing the add-on. The file might be
empty if the add-on has never been 'completed'. If the add-on is currently in edit mode,
instead the edit directory containing the unpacked add-on sources is returned. In any way,
this function returns the location the application uses, too, to access add-on content.

#### gom.api.addons.AddOn.get_file_list

```{py:function} gom.api.addons.AddOn.get_file_list(): list

Return the list of files contained in the add-on
:API version: 1
:return: List of files in that add-on (full path)
:rtype: list
```

This function returns the list of files and directories in an add-on. These path names can
be used to read or write/modify add-on content.

Please note that the list of files can only be obtained for add-ons which are currently not
in edit mode ! An add-on in edit mode is unzipped and the `get_file ()` function will return
the file system path to its directory in that case. That directory can then be browsed with
the standard file tools instead.

#### Example

```
for addon in gom.api.addons.get_installed_addons():
  # Edited add-ons are file system based and must be accessed via file system functions
  if addon.is_edited():
    for root, dirs, files in os.walk(addon.get_file ()):
      for file in files:
        print(os.path.join(root, file))

  # Finished add-ons can be accessed via this function
  else:
    for file in addon.get_file_list():
      print (file)
```

#### gom.api.addons.AddOn.get_id

```{py:function} gom.api.addons.AddOn.get_id(): UUID

Return the unique id (uuid) of this add-on
:API version: 1
:return: Add-on uuid
:rtype: UUID
```

This function returns the uuid associated with this add-on. The id can be used to
uniquely address the add-on.

#### gom.api.addons.AddOn.get_level

```{py:function} gom.api.addons.AddOn.get_level(): str

Return the level (system/shared/user) of the add-on
:API version: 1
:return: Level of the add-on
:rtype: str
```

This function returns the 'configuration level' of the add-on. This can be
* 'system' for pre installed add-on which are distributed together with the application
* 'shared' for add-ons in the public or shared folder configured in the application's preferences or
* 'user' for user level add-ons installed for the current user only.

#### gom.api.addons.AddOn.get_name

```{py:function} gom.api.addons.AddOn.get_name(): str

Return the displayable name of the add-on
:API version: 1
:return: Add-on name
:rtype: str
```

This function returns the displayable name of the add-on. This is the human
readable name which is displayed in the add-on manager and the add-on store.

#### gom.api.addons.AddOn.get_script_list

```{py:function} gom.api.addons.AddOn.get_script_list(): list

Return the list of scripts contained in the add-on
:API version: 1
:return: List of scripts in that add-on (full path)
:rtype: list
```


#### gom.api.addons.AddOn.get_tags

```{py:function} gom.api.addons.AddOn.get_tags(): str

Return the list of tags with which the add-on has been tagged
:API version: 1
:return: List of tags
:rtype: str
```

This function returns the list of tags in the addons `metainfo.json` file.

#### gom.api.addons.AddOn.has_license

```{py:function} gom.api.addons.AddOn.has_license(): bool

Return if the necessary licenses to use this add-on are present
:API version: 1
```

This function returns if the necessary licenses to use the add-on are currently present.
Add-ons can either be free and commercial. Commercial add-ons require the presence of a
matching license via a license dongle or a license server.

#### gom.api.addons.AddOn.is_edited

```{py:function} gom.api.addons.AddOn.is_edited(): bool

Return if the add-on is currently edited
:API version: 1
:return: 'true' if the add-on is currently in edit mode
:rtype: bool
```

Usually, an add-on is simply a ZIP file which is included into the applications file system. When
an add-on is in edit mode, it will be temporarily unzipped and is then present on disk in a directory.

#### gom.api.addons.AddOn.is_protected

```{py:function} gom.api.addons.AddOn.is_protected(): bool

Return if the add-on is protected
:API version: 1
:return: Add-on protection state
:rtype: bool
```

The content of a protected add-on is encrypted. It can be listed, but not read. Protection
includes both 'IP protection' (content cannot be read) and 'copy protection' (content cannot be
copied, as far as possible)

#### gom.api.addons.AddOn.read

```{py:function} gom.api.addons.AddOn.read(path: str): bytes

Read file from add-on
:API version: 1
:param path: File path as retrieved by 'gom.api.addons.AddOn.get_file_list ()'
:type path: str
:return: Content of that file as a byte array
:rtype: bytes
```

This function reads the content of a file from the add-on. If the add-on is protected,
the file can still be read but will be AES encrypted.

**Example:** Print all add-on 'metainfo.json' files

```
import gom
import json

for a in gom.api.addons.get_installed_addons ():
  text = json.loads (a.read ('metainfo.json'))
  print (json.dumps (text, indent=4))
```

#### gom.api.addons.AddOn.write

```{py:function} gom.api.addons.AddOn.write(path: str, data: bytes): None

Write data into add-on file
:API version: 1
:param path: File path as retrieved by 'gom.api.addons.AddOn.get_file_list ()'
:type path: str
:param data: Data to be written into that file
:type data: bytes
```

This function writes data into a file into an add-ons file system. It can be used to update,
migrate or adapt the one add-on the API call originates from. Protected add-ons cannot be
modified at all.

```{important}
An add-on can modify only its own content ! Access to other add-ons is not permitted. Use this
function with care, as the result is permanent !
```

### gom.api.addons.get_addon

```{py:function} gom.api.addons.get_addon(id: UUID): gom.api.addons.AddOn

Return the add-on with the given id
:API version: 1
:param id: Id of the add-on to get
:type id: UUID
:return: Add-on with the given id
:rtype: gom.api.addons.AddOn
:throws: Exception if there is no add-on with that id
```

This function returns the add-on with the given id

**Example:**

```
addon = gom.api.addons.get_addon ('1127a8be-231f-44bf-b15e-56da4b510bf1')
print (addon.get_name ())
> 'AddOn #1'
```

### gom.api.addons.get_current_addon

```{py:function} gom.api.addons.get_current_addon(): gom.api.addons.AddOn

Return the current add-on
:API version: 1
:return: Add-on the caller is a member of or `None` if there is no such add-on
:rtype: gom.api.addons.AddOn
```

This function returns the add-on the caller is a member of

**Example:**

```
addon = gom.api.addons.get_current_addon ()
print (addon.get_id ())
> d04a082c-093e-4bb3-8714-8c36c7252fa0
```

### gom.api.addons.get_installed_addons

```{py:function} gom.api.addons.get_installed_addons(): list[gom.api.addons.AddOn]

Return a list of the installed add-ons
:API version: 1
:return: List of 'AddOn' objects. Each 'AddOn' object represents an add-on and can be used to query information about that specific add-on.
:rtype: list[gom.api.addons.AddOn]
```

This function can be used to query information of the add-ons which are currently
installed in the running instance.

**Example:**

```
for a in gom.api.addons.get_installed_addons ():
  print (a.get_id (), a.get_name ())
```

## gom.api.dialog

API for handling dialogs

This API is used to create and execute script based dialogs. The dialogs are defined in a
JSON based description format and can be executed server side in the native UI style.

### gom.api.dialog.create

```{py:function} gom.api.dialog.create(context: Any, url: str): Any

Create modal dialog, but do not execute it yet
:param context: Script execution context
:type context: Any
:param url: URL of the dialog definition (*.gdlg file)
:type url: str
:return: Dialog handle which can be used to set up the dialog before executing it
:rtype: Any
```

This function creates a dialog. The dialog is passed in an abstract JSON description defining its layout.
The dialog is created but not executed yet. The dialog can be executed later by calling the 'gom.api.dialog.show'
function. The purpose of this function is to create a dialog in advance and allow the user setting it up before

This function is part of the scripted contribution framework. It can be used in the scripts
'dialog' functions to pop up user input dialogs, e.g. for creation commands. Passing of the
contributions script context is mandatory for the function to work.

### gom.api.dialog.execute

```{py:function} gom.api.dialog.execute(context: Any, url: str): Any

Create and execute a modal dialog
:param context: Script execution context
:type context: Any
:param url: URL of the dialog definition (*.gdlg file)
:type url: str
:return: Dialog input field value map. The dictionary contains one entry per dialog widget with that widgets current value.
:rtype: Any
```

This function creates and executes a dialog. The dialog is passed in an abstract JSON
description and will be executed modal. The script will pause until the dialog is either
confirmed or cancelled.

This function is part of the scripted contribution framework. It can be used in the scripts
'dialog' functions to pop up user input dialogs, e.g. for creation commands. Passing of the
contributions script context is mandatory for the function to work.

### gom.api.dialog.show

```{py:function} gom.api.dialog.show(context: Any, dialog: Any): Any

Show previously created and configured dialog
:param context: Script execution context
:type context: Any
:param dialog: Handle of the previously created dialog
:type dialog: Any
:return: Dialog input field value map. The dictionary contains one entry per dialog widget with that widgets current value.
:rtype: Any
```

This function shows and executes previously created an configured dialog. The combination of
'create' and 'show' in effect is the same as calling 'execute' directly.

## gom.api.imaging

Image point/pixel related functions

Image related functions can be used to query images from the measurements of a project. This is not done directly,
but via an ‘image acquisition’ object which acts as a proxy between the image storing data structure and the
functions which can be used to process the image data.

Terminology:
- 'point': 3D coordinate in the project.
- 'pixel': 2D coordinate in an image.

### gom.api.imaging.Acquisition

Class representing a single acquisition

An acquisition describes a camera position and viewing direction of a measurement.

#### gom.api.imaging.Acquisition.get_angle

```{py:function} gom.api.imaging.Acquisition.get_angle(): gom.Vec3d

Return viewing angles of the camera during the measurement
```


#### gom.api.imaging.Acquisition.get_coordinate

```{py:function} gom.api.imaging.Acquisition.get_coordinate(): gom.Vec3d

Return 3d coordinate of the camera during the measurement
```


### gom.api.imaging.compute_epipolar_line

```{py:function} gom.api.imaging.compute_epipolar_line(source: gom.api.imaging.Acquisition, traces: list[tuple[gom.Vec2d, gom.Object]], max_distance: float): list[list[gom.Vec2d]]

Compute epipolar line coordinates
:API version: 1
:param source: Handle of the image acquisition the epipolar line should be found in.
:type source: gom.api.imaging.Acquisition
:param traces: List of pairs where each entry describes a pixel image coordinate plus the image acquisition object which should be used to compute the matching point. The image acquisition object here is the “other” acquisition providing the pixels used to find the matching epipolar lines in the `sources` object.
:type traces: list[tuple[gom.Vec2d, gom.Object]]
:param max_distance: Maximum search distance in mm.
:type max_distance: float
:return: List of matching points
:rtype: list[list[gom.Vec2d]]
```

This function computes the parametrics of an epipolar line from pixels projected into images.

**Example**

```
stage = gom.app.project.stages['Stage 1']
point = gom.app.project.actual_elements['Point 1'].coordinate

left = gom.api.project.get_image_acquisition (measurement, 'left camera', [stage.index])[0]
right = gom.api.project.get_image_acquisition (measurement, 'right camera', [stage.index])[0]

l = gom.api.imaging.compute_epipolar_line (left, [(gom.Vec2d (1617, 819), right)], 10.0)

print (l)
```

```
[[gom.Vec2d (4.752311764226988, 813.7915394509045), gom.Vec2d (10.749371580282741, 813.748887458453), gom.Vec2d
(16.73347976996274, 813.706352662515), ...]]
```

### gom.api.imaging.compute_pixels_from_point

```{py:function} gom.api.imaging.compute_pixels_from_point(point_and_image_acquisitions: list[tuple[gom.Vec3d, gom.Object]]): list[gom.Vec2d]

Compute pixel coordinates from point coordinates
:API version: 1
:param point_and_image_acquisitions: List of (point, acquisition) tuples
:type point_and_image_acquisitions: list[tuple[gom.Vec3d, gom.Object]]
:return: List of matching points
:rtype: list[gom.Vec2d]
```

This function is used to compute the location of a 3d point in a 2d image. This is a photogrammetric
operation which will return a precise result. The input parameter is a list of tupels where each tuple consists
of a 3d point and and acquisition object. The acquisition object is then used to compute the location of the
3d point in the referenced image. This might lead to multiple pixels as a result, so the return value is again
a list containing 0 to n entries of pixel matches.

**Example**

```
measurement = gom.app.project.measurement_series['Deformation series'].measurements['D1']
stage = gom.app.project.stages['Stage 1']
point = gom.app.project.actual_elements['Point 1'].coordinate

left = gom.api.project.get_image_acquisition (measurement, 'left camera', [stage.index])[0]
right = gom.api.project.get_image_acquisition (measurement, 'right camera', [stage.index])[0]

p = gom.api.imaging.compute_pixels_from_point ([(point, left), (point, right)])

print (p)
```

```
[gom.Vec2d (1031.582008690226, 1232.4155555222544), gom.Vec2d (1139.886626169376, 1217.975608783256)]
```

### gom.api.imaging.compute_point_from_pixels

```{py:function} gom.api.imaging.compute_point_from_pixels(pixel_and_image_acquisitions: [list], use_calibration: bool): [list]

Compute 3d point coordinates from pixels in images
:API version: 1
:param pixel_and_image_acquisitions: List of (pixel, acquisition) tuples
:type pixel_and_image_acquisitions: [list]
:param use_calibration: If set, the information from the calibration is used to compute the point. Project must provide a calibration for that case.
:type use_calibration: bool
:return: List of matching pixels and residuums
:rtype: [list]
```

This function is used to compute 3d points matching to 2d points in a set of images. The input parameter is a list
containing a list of tuples where each tuple consists of a 2d pixel and the matching acquisition object. The
acquisition object is then used to compute the location of the 3d point from the pixels in the referenced images.
Usually at least two tuples with matching pixels from different images are needed to compute a 3d point. An exception
are projects with 2d deformation measurement series. Only there it is sufficient to pass one tuple per point to the
function.

The user has to make sure that the pixels from different tuples are matching, which means they correspond to the same
location on the specimen. You can use the function gom.api.imaging.compute_epipolar_line() as a helper.

The returned value is a list of (point, residuum) where each entry is the result of intersecting rays cast from the
camera positions through the given pixels. The pixel coordinate system center is located in the upper left corner.

**Example**

```
measurement = gom.app.project.measurement_series['Deformation 1'].measurements['D1']
stage = gom.app.project.stages[0]

img_left = gom.api.project.get_image_acquisition (measurement, 'left camera', [stage.index])[0]
img_right = gom.api.project.get_image_acquisition (measurement, 'right camera', [stage.index])[0]

pixel_pair_0 = [(gom.Vec2d(1587.74, 793.76), img_left), (gom.Vec2d(2040.22, 789.53), img_right)]
pixel_pair_1 = [(gom.Vec2d(1617.47, 819.67), img_left), (gom.Vec2d(2069.42, 804.69), img_right)]

tuples = [pixel_pair_0, pixel_pair_1]
points = gom.api.imaging.compute_point_from_pixels(tuples, False)

print (points)
```

```
[[gom.Vec3d (-702.53, 1690.84, -22.37), 0.121], [gom.Vec3d (-638.25, 1627.62, -27.13), 0.137]]
```

## gom.api.interpreter

API for accessing python script interpreter properties

This API can access properties and states of the python script interpreters. It is used
mainly for internal debugging and introspection scenarios.

### gom.api.interpreter.get_info

```{py:function} gom.api.interpreter.get_info(): dict

Query internal interpreter state for debugging purposed
:return: JSON formatted string containing various information about the running interpreters
:rtype: dict
```

```{caution}
This function is for debugging purposes only ! Its content format may change arbitrarily !
```

### gom.api.interpreter.get_pid

```{py:function} gom.api.interpreter.get_pid(): int

Return the process id (PID) of the API handling application
:return: Application process id
:rtype: int
```

This function returns the process id of the application the script is connected with.

## gom.api.introspection

Introspection API for accessing the available API modules, functions and classes

This API enables access to the API structure in general. It is meant to be mainly for debugging and
testing purposes.

### gom.api.introspection.Class

Introspection interface for a class

This interface can be used to query various information about a class definition

#### gom.api.introspection.Class.description

```{py:function} gom.api.introspection.Class.description(): str

Returns and optional class description
:API version: 1
:return: Class description
:rtype: str
```


#### gom.api.introspection.Class.methods

```{py:function} gom.api.introspection.Class.methods(): list[gom.api.introspection.Method]

Returns all class methods
:API version: 1
:return: List of class methods
:rtype: list[gom.api.introspection.Method]
```


#### gom.api.introspection.Class.name

```{py:function} gom.api.introspection.Class.name(): str

Returns the name of the class
:API version: 1
:return: Class name
:rtype: str
```


#### gom.api.introspection.Class.type

```{py:function} gom.api.introspection.Class.type(): str

Returns the unique internal type name of the class
:API version: 1
:return: Type name
:rtype: str
```


### gom.api.introspection.Function

Introspection interface for a function

This interface can be used to query various information about a function

#### gom.api.introspection.Function.arguments

```{py:function} gom.api.introspection.Function.arguments(): list[[str, str, str]]

Returns detailed information about the function arguments
:API version: 1
:return: Function arguments information
:rtype: list[[str, str, str]]
```


#### gom.api.introspection.Function.descripion

```{py:function} gom.api.introspection.Function.descripion(): str

Returns the optional function description
:API version: 1
:return: Function description
:rtype: str
```


#### gom.api.introspection.Function.name

```{py:function} gom.api.introspection.Function.name(): str

Returns the name of the function
:API version: 1
:return: Function name
:rtype: str
```


#### gom.api.introspection.Function.returns

```{py:function} gom.api.introspection.Function.returns(): [str, str]

Returns detailed information about the function returned value
:API version: 1
:return: Function returned value information
:rtype: [str, str]
```


#### gom.api.introspection.Function.signature

```{py:function} gom.api.introspection.Function.signature(): list[str]

Returns the function signature
:API version: 1
:return: Function signature
:rtype: list[str]
```

The first type in the returned list is the function return value.

### gom.api.introspection.Method

Introspection interface for a method

This interface can be used to query various information about a method

#### gom.api.introspection.Method.arguments

```{py:function} gom.api.introspection.Method.arguments(): list[[str, str, str]]

Returns detailed information about the method arguments
:API version: 1
:return: Method argument information
:rtype: list[[str, str, str]]
```


#### gom.api.introspection.Method.description

```{py:function} gom.api.introspection.Method.description(): str

Returns the optional method description
:API version: 1
:return: Method description
:rtype: str
```


#### gom.api.introspection.Method.name

```{py:function} gom.api.introspection.Method.name(): str

Returns the name of the method
:API version: 1
:return: Method name
:rtype: str
```


#### gom.api.introspection.Method.returns

```{py:function} gom.api.introspection.Method.returns(): [str, str]

Returns detailed information about the return value
:API version: 1
:return: Return value information
:rtype: [str, str]
```


#### gom.api.introspection.Method.signature

```{py:function} gom.api.introspection.Method.signature(): list[str]

Returns the method signature
:API version: 1
:return: Method signature in form of list
:rtype: list[str]
```

This function returns the signature. The first type in the list is the expected return value

### gom.api.introspection.Module

Introspection interface for a module

This interface can be used to query various information about a module

#### gom.api.introspection.Module.description

```{py:function} gom.api.introspection.Module.description(): str

Returns the optional module description
:API version: 1
:return: Module description
:rtype: str
```


#### gom.api.introspection.Module.functions

```{py:function} gom.api.introspection.Module.functions(): list[gom.api.introspection.Function]

Returns all available function of the module
:API version: 1
:return: Module functions
:rtype: list[gom.api.introspection.Function]
```


#### gom.api.introspection.Module.name

```{py:function} gom.api.introspection.Module.name(): str

Returns the name of the module
:API version: 1
:return: Module name
:rtype: str
```


#### gom.api.introspection.Module.tags

```{py:function} gom.api.introspection.Module.tags(): list[str]

Returns the tags of the module
:API version: 1
:return: Module tags
:rtype: list[str]
```

Each module can have a set of tags classifying it or its properties.

#### gom.api.introspection.Module.version

```{py:function} gom.api.introspection.Module.version(): int

Returns the version of the module
:API version: 1
:return: Module version
:rtype: int
```


### gom.api.introspection.classes

```{py:function} gom.api.introspection.classes(): gom.api.introspection.Class

Return introspection interface for a class instance
:API version: 1
:param instance: 'Class' instance to inspect
:return: Introspection object
:rtype: gom.api.introspection.Class
```


### gom.api.introspection.modules

```{py:function} gom.api.introspection.modules(): list[gom.api.introspection.Module]

Return a list of available modules
:API version: 1
:return: List of 'Module' objects.
:rtype: list[gom.api.introspection.Module]
```

This function can be used to query the modules of the API

**Example:**

```
for m in gom.api.introspection.modules ():
  print (m.name ())
```

## gom.api.progress

API for accessing the progress bar in the main window

This API provides basic access to the progress bar in the main window

### gom.api.progress.ProgressBar

Class representing the ProgressBar

This class is meant to be used with the Python 'with' statement

#### Example

```
import gom.api.progress

with gom.api.progress.ProgressBar() as bar:
    bar.set_message('Calculation in progress')
    for i in range(100):
        # Do some calculations
        foo()
        # Increase the progress
        bar.set_progress(i)    

# Progress bar entry gets removed automatically after leaving the 'with' statement
```

#### gom.api.progress.ProgressBar.finish_progress

```{py:function} gom.api.progress.ProgressBar.finish_progress(self: any): None

Finishes the progress and removes this from the progress bar
:API version: 1
:return: nothing
:rtype: None
```

This object CANNOT be used for further progress reporting after calling this method

Can be used if the progress bar should disappear but the with statement cannot be left yet

#### gom.api.progress.ProgressBar.set_message

```{py:function} gom.api.progress.ProgressBar.set_message(self: any, message: str): None

Sets a message in the main window progress bar
:API version: 1
:param message: the message to display
:type message: str
:return: nothing
:rtype: None
```


#### gom.api.progress.ProgressBar.set_progress

```{py:function} gom.api.progress.ProgressBar.set_progress(self: any, progress: int): None

Sets the progress in the main window progress bar
:API version: 1
:param progress: in percent, given as an integer from 0 to 100
:type progress: int
:return: nothing
:rtype: None
```


## gom.api.project

Access to project relevant structures

This module contains functions for accessing project relevant data

### gom.api.project.ProgressInformation

:deprecated: Please use gom.api.progress.ProgressBar instead

Auxillary class allowing to set progress information

This class is used to access the progress bar and progress message widgets of the application.

#### gom.api.project.ProgressInformation.set_message

```{py:function} gom.api.project.ProgressInformation.set_message(text: str): None

:deprecated: Please use gom.api.progress.ProgressBar instead

Set progress message
:API version: 1
:param text: Message to be displayed in the progress displaying widget
:type text: str
```


#### gom.api.project.ProgressInformation.set_percent

```{py:function} gom.api.project.ProgressInformation.set_percent(percent: float): None

:deprecated: Please use gom.api.progress.ProgressBar instead

Set progress value from 0 to 100 percent
:API version: 1
:param percent: Progress bar value in percent (0...100)
:type percent: float
```


### gom.api.project.create_progress_information

```{py:function} gom.api.project.create_progress_information(): gom.api.project.ProgressInformation

:deprecated: Please use gom.api.progress.ProgressBar instead

Retrieve a progress information object which can be used to query/control progress status information
:API version: 1
:return: Progress information object
:rtype: gom.api.project.ProgressInformation
```

This function returns an internal object which can be used to query/control the progress status widget of the
main application window. It can be used to display progress information of long running processes.

### gom.api.project.get_image_acquisition

```{py:function} gom.api.project.get_image_acquisition(measurement: object, camera: str, stage: int): object

Generate an of image acquisition object which can be used to query images from the application
:API version: 1
:param measurement: Measurement the image is to be queried from.
:type measurement: object
:param camera: Identifier for the camera which contributed to the measurement. See above for valid values.
:type camera: str
:param stage: Id of the stage for which the image acquisition object will access.
:type stage: int
:return: Image acquisition object which can be used to fetch the images.
:rtype: object
```

This function returns an image acquisition object, which in turn can then be used to query the application for
various image variants.

Valid valid for the `camera` parameter are:
- `left camera`: Left camera in a two camera system or the only existing camera in a single camera system
- `right camera`: Right camera in a two camera system
- `photogrammetry`: Photogrammetry (TRITOP) camera

**Example**

```
measurement = gom.app.project.measurement_series['Deformation series'].measurements['D1']
stage = gom.app.project.stages['Stage 1']

left = gom.api.project.get_image_acquisition (measurement, 'left camera', [stage.index])[0]
right = gom.api.project.get_image_acquisition (measurement, 'right camera', [stage.index])[0]
```

### gom.api.project.get_image_acquisitions

```{py:function} gom.api.project.get_image_acquisitions(measurement_list: object, camera: str, stage: int): object

Generate a list of image acquisition objects which can be used to query images from the application
:API version: 1
:param measurement: Measurement the image is to be queried from.
:param camera: Identifier for the camera which contributed to the measurement. See above for valid values.
:type camera: str
:param stage: Id of the stage for which the image acquisition object will access.
:type stage: int
:return: Image acquisition object which can be used to fetch the images.
:rtype: object
```

This function returns a list of  image acquisition objects, which in turn can then be used to query the application
for various image variants.

Valid valid for the `camera` parameter are:
- `left camera`: Left camera in a two camera system or the only existing camera in a single camera system
- `right camera`: Right camera in a two camera system
- `photogrammetry`: Photogrammetry (TRITOP) camera

**Example**

```
measurements = list (gom.app.project.measurement_series['Deformation series'].measurements)
stage = gom.app.project.stages['Stage 1']
point = gom.app.project.actual_elements['Point 1'].coordinate

all_left_images = gom.api.project.get_image_acquisitions (measurements, 'left camera', [stage.index])
all_right_images = gom.api.project.get_image_acquisitions (measurements, 'right camera', [stage.index])
```

## gom.api.script_resources

API for the ResourceDataLoader


### gom.api.script_resources.create

```{py:function} gom.api.script_resources.create(path: str): bool

Create a new resource under the root folder of a given script, if not already present.
:param path: Resource path
:type path: str
:return: `true` if a valid resource was found or created.
:rtype: bool
```


### gom.api.script_resources.exists

```{py:function} gom.api.script_resources.exists(path: str): bool

Check if the resource with the given path exists
:param path: Resource path
:type path: str
:return: 'True' if a resource with that path exists
:rtype: bool
```


### gom.api.script_resources.list

```{py:function} gom.api.script_resources.list(): list[str]

Return the list of existing resources
:return: List of existing resources
:rtype: list[str]
```


### gom.api.script_resources.load

```{py:function} gom.api.script_resources.load(path: str, size: int): str

Load resource into shared memory
:param path: Resource path
:type path: str
:param size: Buffer size
:type size: int
:return: Shared memory key of the loaded resource
:rtype: str
```


### gom.api.script_resources.mem_size

```{py:function} gom.api.script_resources.mem_size(path: str): int

Return size of the resource shared memory segment
:param path: Resource path
:type path: str
:return: Shared memory segment size
:rtype: int
```


### gom.api.script_resources.save

```{py:function} gom.api.script_resources.save(path: str, size: int): bool

Save resource changes from shared memory
:param path: Resource path
:type path: str
:param size: Buffer size
:type size: int
:return: 'True' if the data could be written
:rtype: bool
```


### gom.api.script_resources.save_as

```{py:function} gom.api.script_resources.save_as(old_path: str, new_path: str, overwrite: bool): bool

Save resource changes from shared memory at new path
:param old_path: Old resource path
:type old_path: str
:param new_path: New resource path
:type new_path: str
:param size: Buffer size
:return: 'True' if the data could be written
:rtype: bool
```


### gom.api.script_resources.unload

```{py:function} gom.api.script_resources.unload(path: str): bool

Unload resource from shared memory
:param path: Resource path
:type path: str
:return: 'True' if the unloading succeeded
:rtype: bool
```


## gom.api.scripted_checks_util

Tool functions for scripted checks


### gom.api.scripted_checks_util.is_curve_checkable

```{py:function} gom.api.scripted_checks_util.is_curve_checkable(element: gom.Object): bool

Checks if the referenced element is suitable for inspection with a curve check
:API version: 1
:param element: Element reference to check
:type element: gom.Object
:return: 'true' if the element is checkable like a curve
:rtype: bool
```

This function checks if the given element can be inspected like a curve in the context of scripted
elements. Please see the scripted element documentation for details about the underlying scheme.

### gom.api.scripted_checks_util.is_scalar_checkable

```{py:function} gom.api.scripted_checks_util.is_scalar_checkable(element: gom.Object): bool

Checks if the referenced element is suitable for inspection with a scalar check
:API version: 1
:param element: Element reference to check
:type element: gom.Object
:return: 'true' if the element is checkable like a scalar value
:rtype: bool
```

This function checks if the given element can be inspected like a scalar value in the context of scripted
elements. Please see the scripted element documentation for details about the underlying scheme.

### gom.api.scripted_checks_util.is_surface_checkable

```{py:function} gom.api.scripted_checks_util.is_surface_checkable(element: gom.Object): bool

Checks if the referenced element is suitable for inspection with a surface check
:API version: 1
:param element: Element reference to check
:type element: gom.Object
:return: 'true' if the element is checkable like a surface
:rtype: bool
```

This function checks if the given element can be inspected like a surface in the context of scripted
elements. Please see the scripted element documentation for details about the underlying scheme.

## gom.api.scriptedelements

API for handling scripted elements

This API defines various functions for handling scripted elements (actuals, checks, nominal, diagrams, ...)
It is used mostly internal by the scripted element framework.

### gom.api.scriptedelements.get_inspection_definition

```{py:function} gom.api.scriptedelements.get_inspection_definition(typename: str): Any

Return information about the given scripted element type
:param type_name: Type name of the check to query
:return: Dictionary with relevant type information or and empty dictionary if the type is unknown
:rtype: Any
```

This function queries in internal 'scalar registry' database for information about the
check with the given type.

## gom.api.services

API for accessing the script based API extensions (services)

This API enables access to the script based API endpoint implementations, called 'services'.
Each service is a script which is started in a server mode and adds various functions and
endpoints to the ZEISS Inspect API.

### gom.api.services.Service

Class representing a single API service

This class represents an API service. The properties of that service can be read and
the service can be administered (started, stopped, ...) via that handle.

#### gom.api.services.Service.get_autostart

```{py:function} gom.api.services.Service.get_autostart(): bool

Return autostart status of the service
:return: 'true' if the service is started automatically at application startup
:rtype: bool
```

This function returns if the service is started automatically at application startup. This
status can only be set manually by the user either during service installation or afterwards in
the service management dialog.

#### gom.api.services.Service.get_endpoint

```{py:function} gom.api.services.Service.get_endpoint(): str

Return the API endpoint name of this service
:API version: 1
:return: Service endpoint if the service is initialized
:rtype: str
```

This function returns the endpoint identifier this service is covering, like 'gom.api.services'.

#### gom.api.services.Service.get_name

```{py:function} gom.api.services.Service.get_name(): str

Return the human readable name of this service
:API version: 1
:return: Service name if the service is initialized
:rtype: str
```


#### gom.api.services.Service.get_number_of_instances

```{py:function} gom.api.services.Service.get_number_of_instances(): int

Get the number of API instances (processes) the service runs in parallel
:return: Number of API instances which are run in parallel when the service is started.
:rtype: int
```

Return the number of API processes instances which are running in parallel. A service can
be configured to start more than one API process for parallelization.

#### gom.api.services.Service.get_status

```{py:function} gom.api.services.Service.get_status(): str

Return the current service status
:API version: 1
:return: Service status
:rtype: str
```

This function returns the status the service is currently in. Possible values are

- STOPPED: Service is not running.
- STARTED: Service has been started and is currently initializing. This can include both the general
service process startup or running the global service initialization code (model loading, ...).
- RUNNING: Service is running and ready to process API requests. If there are multiple service instances configured
per service, the service counts as RUNNING not before all of these instances have been initialized !
- STOPPING: Service is currently shutting down,

#### gom.api.services.Service.start

```{py:function} gom.api.services.Service.start(): None

Start service
:API version: 1
```

This function will start a script interpreter executing the service script as an API endpoint.

```{caution}
The function will return immediately, the service instances are starting in the background afterwards.
The `get_status ()` function can be used to poll the status until the service has been started.
```

#### gom.api.services.Service.stop

```{py:function} gom.api.services.Service.stop(): None

Stop service
:API version: 1
```

Stop service. The service can be restarted afterwards via the 'start ()' function
if needed.

```{caution}
The function will return immediately, the service instances will be stopped asynchronously.
The 'get_status ()' function can be used to poll the service status until all service instances
have been stopped.
```

### gom.api.services.get_services

```{py:function} gom.api.services.get_services(): [gom.api.services.Service]

Return the list of all running and not running services
:API version: 1
:return: The list of all registered services
:rtype: [gom.api.services.Service]
```

This function returns the listof registered services

**Example:**

```
for s in gom.api.services.get_services ():
  print (s.get_name ())
> 'Advanced fitting algorithms'
> 'Tube inspection diagrams'
> ...
```

## gom.api.settings

API for storing add-on related settings persistently

This API allows reading/writing values into the application configuration permantly. The
configuration is persistant and will survive application restarts. Also, it can be accessed
via the applications preferences dialog.

The configuration entries must be defined in the add-ons `metainfo.json` file. This configuration
defined the available keys, the entry types and the entry properties. If the entry type can be
represented by some widget, the setting entry will also be present in the applications 'preferences'
dialog and can be adapted interactively there.

### Example

```
{
  "title": "Settings API example",
  "description": "Example add-on demonstrating usage of the settings API",
  "uuid": "3b515488-aa7b-4035-85e1-b9509db8af4f",
  "version": "1.0.2",
  "settings": [
   {
      "name": "dialog",
      "description": "Dialog configuration"
   },
   {
     "name": "dialog.size",
     "description": "Size of the dialog"
   },
   {
     "name": "dialog.size.width",
     "description": "Dialog width",
     "value": 640,
     "digits": 0
   },
   {
     "name": "dialog.size.height",
     "description": "Dialog height",
     "value": 480,
     "digits": 0
   },
   {
     "name": "dialog.threshold",
     "description": "Threshold",
     "value": 1.0,
     "minimum": 0.0,
     "maximum": 10.0,
     "digits": 2,
     "step": 0.01
   },
   {
     "name": "dialog.magic",
     "description": "Magic Key",
     "value": "Default text",
     "visible": false
   },
   {
     "name": "enable",
     "description": "Enable size storage",
     "value": true,
     "visible": true
   },
   {
     "name": "dialog.file",
     "description": "Selected file",
     "value": "",
     "type": "file",
     "mode": "any",
     "visible": true
   }
  ]
 }
```

This will lead to configuration entries in the applications preferences. Given that the `metainfo.json` is
part of an add-on called 'Settings API Example', the application preferences will contain the following items
(visible setting entries only):

![Settings level 1](images/settings_api_preferences_1.png)

![Settings level 2](images/settings_api_preferences_2.png)

### Types

See the examples above for how to configure the different settings type. Usually, the `value` field determines the
type of the setting. For example, a `23` indicates that an integer is requested. A `23.0` with `digits` greater than
0 will lead to a float settings type.

Special non basic types are specified via the `type` field explicitly. For example, the file selector is configured
if the `type` field has been set to `file`.

#### File selector

The file selector provides a `mode` attribute in addition to the standard settings entry attributes. The `mode`
attribute determines what kind of files or directories can be selected.

- `any`: Any file
- `new`: Any file not yet existing in a writable directory
- `load_file`: Existing file with reading permissions
- `load_files`: Multi existing files with reading permissions
- `save_file`: Existing or new file with writing permissions
- `load_dir`: Existing directory with reading permissions
- `save_dir`: Existing directory with writing permissions
- `exec`: Existing executable file

### gom.api.settings.get

```{py:function} gom.api.settings.get(key: str): Any

Read value from application settings
:API version: 1
:param key: Configuration key. Must be a key as defined in the add-ons `metainfo.json` file.
:type key: str
:return: Configuration value for that key
:rtype: Any
```

This function reads a value from the application settings. The value is referenced by a key. Supported value types
are integer, double, string and bool.

**Example**

```
w = gom.api.settings.get ('dialog.width')
h = gom.api.settings.get ('dialog.height')
```

### gom.api.settings.list

```{py:function} gom.api.settings.list(): list[str]

List all available keys for the current add-on
:API version: 1
:return: List of all the keys in the settings which belong to the current add-on
:rtype: list[str]
```

This function returns a list of all available keys in the settings for the current add-on.
These keys are the same configuration keys are used in the `metainfo.json` file of that add-on.

### gom.api.settings.set

```{py:function} gom.api.settings.set(key: str, value: Any): None

Write value into application settings
:API version: 1
:param key: Configuration key. Must be a key as defined in the add-ons `metainfo.json` file.
:type key: str
:param value: Value to be written
:type value: Any
```

This function writes a value into the application settings. The value is referenced by a key. Supported value types
are integer, double, string and bool.

**Example**

```
gom.api.settings.set ('dialog.width', 640)
gom.api.settings.set ('dialog.height', 480)
```

## gom.api.testing

API with testing and verification functions

This API provides various functions which can be of use when testing and developing
API features.

### gom.api.testing.TestObject

Simple object which can be passed around the API for testing purpose

This object is used by various test setups to test object handling in the API

#### gom.api.testing.TestObject.get_id

```{py:function} gom.api.testing.TestObject.get_id(): UUID

Return the unique id (uuid) of this object
:API version: 1
:return: Object uuid
:rtype: UUID
```

This function returns the uuid associated with this object. The id is generated
randomly when the object is generated.

#### gom.api.testing.TestObject.get_name

```{py:function} gom.api.testing.TestObject.get_name(): str

Return the name of this object
:API version: 1
:return: Object name
:rtype: str
```

This function returns the name of this object.

### gom.api.testing.generate_test_object

```{py:function} gom.api.testing.generate_test_object(content: str): gom.api.testing.TestObject

Generate test object
:API version: 1
:param name: Name of the test object
:return: Test object instance
:rtype: gom.api.testing.TestObject
```

This function is used for API testing. It generates a simple test object which can then
be passed around the API.

**Example:**

```
obj = gom.api.testing.generate_test_object('test1')
```

### gom.api.testing.reflect

```{py:function} gom.api.testing.reflect(content: Any): Any

Send value to the API and return an echo
:API version: 1
:param content: The value to be reflected
:type content: Any
:return: Reflected value
:rtype: Any
```

This function is used for API testing. It just reflects the given value, so some conversions
back and forth will be performed.

**Example:**

```
result = gom.api.testing.reflect ({'a': [1, 2, 3], 'b':('foo', 'bar')})
```

