# Workflow assistant

> Abstract:  A workflow assistant helps you to find the most important functions for a specific measuring or inspection tasks. A workflow assistant can help you to access the most frequently used functions faster. By default, you find the tab **Workflow Assistant** in the right docking area next to the tab **Properties** (see [Tech Guide &ndash; Workflow Assistant](https://techguide.zeiss.com/en/zeiss-inspect-2025/article/view_workflow_assistant.html)).

## User interface

A workflow assistant can be composed of the following UI elements:

1. [Pages](#pages) &ndash; A page is a container for other Workflow Assistant elements.

   There are three different page types:
   
   * [MenuPage](#menupage) &ndash; Shows a list of [Menu Entries](#menu-entries).
   * [WizardPage](#wizardpage) &ndash; Contains a list of [WizardSteps](#wizard-steps), which are executed sequentially.
   * [EmbeddedCommandPage](#embeddedcommandpage) &ndash; Contains an embedded command dialog.

2. [Menu Entries](#menu-entries)

   There are four different types:

   * [NextPageEntry](#nextpageentry) &ndash; Leads to a new page.
   * [CommandEntry](#commandentry) &ndash; Execute a command, usually without a dialog.
   * [EmbeddedCommandEntry](#embeddedcommandentry) &ndash; Execute a command with its dialog embedded in the menu page.
   * [AccordionEntry](#accordionentry) &ndash; Contains a list of menu entries which can be collapsed and expanded.

```{note}
![Breacrumbs](assets/breadcrumbs.png)

The "breadcrumbs" at the top of the workflow assistant show the current position in the menu structure.
```

```{note}
The initial appearance of CommandEntry, EmbeddedCommandPage and WizardPage is identical, but differs during execution.\
The appearance of the NextPageEntry depends on its target's type.
```

### Example

The ZEISS INSPECT built-in workflow of the **Inspection** workspace is used as an example.

#### 1. Menu page

```{figure} assets/menupage.png
:alt: Menu page
:class: bordered-figure

Inspection Workspace Workflow Assistant &ndash; Menu page
```

This Menu page consists of the items "First steps" (Accordion entry), "Inspection" (Menu page) and "Reports" (Accordion entry).

#### 2. Wizard page

```{figure} assets/inspection_digitize-inspection.png
:alt: Menu page
:class: bordered-figure

Select "Inspection"
```

```{figure} assets/inspection-basic_inspections-diameter_inspections.png
:alt: Menu page
:class: bordered-figure

"Inspection" menu page &ndash; Select Basic Inspections ► Diameter Inspections
```

```{figure} assets/wizard1-construct.png
:alt: Menu page
:class: bordered-figure

Wizard page, Wizard step 1 &ndash; "Construct Cylinder or Circle"
```

```{figure} assets/wizard2-check.png
:alt: Menu page
:class: bordered-figure

Wizard page, Wizard step 2 &ndash; "Check Diameter"
```

Selecting "Basic Inspections" leads to "Diameter Inspections", "Distance Inspections" and "Angle Inspections". Starting "Diameter Inspections" shows a Wizard page with two steps:

1. Construct Cylinder or Circle
2. Check Diameter

```{note}
The wizard lets you continue to the next step only after you have completed the current step!
```

#### 3. Embedded command page

```{figure} assets/embedded_command_page-distance_inspections.png
:alt: Menu page
:class: bordered-figure

Embedded command page &ndash; "Distance Quick Creation"
```

Starting "Distance Inspections" from the "Basic Inspections" menu page calls the internal command `inspection.distance_quick_creation`. This is the same as running Construct ► Distance ► Distance Quick Creation... from the main menu, but this way the dialog window is embedded in the workflow assistant.

## Creating a Workflow Assistant

Create a JSON file `workflow_assistant/<assistant_name>/<assistant_name>.json` in your App's folder.

```{note}
A new JSON file cannot be created in the App Explorer yet. Go to your App folder in `%APPDATA%/gom/<inspect_version>/gom_edited_addons` and create the JSON file using an external editor instead.
```

```{hint}
* To update the App Explorer, run `gom.script.sys.update_addon_database()` from a Python script.
* To update the Workflow Assistant view, switch to a different workspace and back again.
```

## Minimal example

The minimal example demonstrates the basic concept of creating a Workflow Assistant menu structure referencing built-in commands.

```{note}
See [App Examples &ndash; WorkflowAssistants](https://github.com/ZEISS/zeiss-inspect-app-examples/tree/main/AppExamples/misc/WorkflowAssistants) for complete source code.
```

The basic building blocks for the menu structure are:

1. [MenuPage](#menupage)
   * A menu page with multiple entries that can be shown in the Workflow Assistant view.
2. [NextPageEntry](#nextpageentry)
   * A menu entry that allows the user to navigate to another menu or wizard page
   * Uses 'name', 'icon' and 'description' of referenced page if not given explicitly.
3. [EmbeddedCommandPage](#embeddedcommandentry)
   * This is used to display a single command in the Workflow Assistant.
4. [WizardPage](#wizardpage)
   * A page to show multiple commands as a sequence in a wizard layout.
   * An [EmbeddedCommandStep](#embeddedcommandstep) is used to represent each step

```{code-block} json
:caption: minimal.json &ndash; top level
:linenos:

{
  "id": "8d7724f7-5cf3-4262-b39a-7228d69952e8",
  "name": "Minimal example",
  "using": [
    {
      "name": "inspect",
      "id": "bd0ec39e-4155-4d7d-9771-9ed0d5f86e59"
    }
  ],
  "objects": [
    // ...
  ]
}
```

At the top level, each Workflow Assistant must have a unique ID (UUID) (line 2) and a name 
(line 3). With `"using"`, an alias for an object's UUID can be defined to improve readability (l. 4..8).
The element `"objects"` (l. 10) contains a list of objects, which are the building blocks of this Workflow Assistant.

```{code-block} json
:caption: minimal.json &ndash; MenuPage "homepage"
:linenos:

{
  // ...
  "objects": [
    {
      "type": "MenuPage",
      "id": "homepage",
      "name": "a minimal homepage",
      "entries": [
        {
          "type": "NextPageEntry",
          "page": "create_diameter"
        },
        {
          "type": "EmbeddedCommandPage",
          "description": "Custom description for command",
          "command": "comparison.create_multiple_surface_comparison_on_cad"
        }
      ]
    },
    // ...  
  ]
}
```

The [MenuPage](#menupage) `"homepage"` provides two menu entries:
1. A [NextPageEntry](#nextpageentry) to the page `"create_diameter"`
2. An [EmbeddedCommandPage](#embeddedcommandpage) for execution of the ZEISS INSPECT command `comparison.create_multiple_surface_comparison_on_cad`.

```{code-block} json
:caption: minimal.json &ndash; NextPageEntry
:linenos:

{
  // ...
  "objects": [
    // ...
    {
      "type": "NextPageEntry",
      "name": "Minimal example",
      "description": "hook for example assistant",
      "page": "homepage",
      "id": "hook_for_inspect",
      "position": {
        "insert": "inspect/inspection_home",
        "before": ""
      }
    },
    // ...
  ]
}
```

```{figure} assets/minimal_example-1.png
:alt: NextPageEntry "hook_for_inspect"
:class: bordered-figure

NextPageEntry "hook_for_inspect"
```

A [NextPageEntry](#nextpageentry) with its elements `"name"`, `"description"` and `"page"` is defined (l. 6..8).

To actually make a workflow element visible, its `"position"` has to be defined by inserting it as a menu entry at the desired location. In the example above, the entry is inserted after the `"inspect"` Workflow's `"inspection_home"` page.

(The `"inspect"` workflow is part of the ZEISS INSPECT System Apps. The alias we previously defined with `"using"` allows to reference it by name instead of ID.)

```{figure} assets/minimal_example-2.png
:alt: MenuPage "homepage"
:class: bordered-figure

MenuPage "homepage"
```

Clicking the NextPageEntry `"Minimal example"` leads to the MenuPage `"homepage"`.

```{code-block} json
:caption: minimal.json &ndash; WizardPage "create_diameter"
:linenos:

{
  // ...
  "objects": [
    // ...
    {
      "type": "WizardPage",
      "id": "create_diameter",
      "name": "(Page name) Diameter Inspections",
      "description": "(Page description) Create diameter checks",
      "icon": "cmd_inspect_diameter",
      "steps": [
        {
          "type": "EmbeddedCommandStep",
          "command": "primitive.cylinder_circle_quick_creation_draft",
          "info": "Each step in a wizard references a command. An additional info box can be provided. The info box is separate for each command and may be omitted in each step (see next step)."
        },
        {
          "type": "EmbeddedCommandStep",
          "command": "internal.check_scalar_diameter"
        }
      ]
    }
  ]
}
```

```{figure} assets/minimal_example-3.png
:alt: WizardPage "create_diameter" &ndash; Step 1
:class: bordered-figure

WizardPage "create_diameter" &ndash; Step 1
```
```{figure} assets/minimal_example-4.png
:alt: WizardPage "create_diameter" &ndash; Step 2
:class: bordered-figure

WizardPage "create_diameter" &ndash; Step 2
```

The last object of our "Minimal example" is the [WizardPage](#wizardpage) `"create_diameter"`. This page contains two subsequent wizard steps, both of which are [EmbeddedCommandSteps](#embeddedcommandstep). The first step allows to create a cylinder or circle while the second step allows to check the diameter of the newly created element. The next step can only be selected when the current step has been completed.

```{hint}
As an alternative to the `"position"` element, a workflow assistant can be made visible by adding a reference to one of its pages to a workspace definition.

See [AppExamples &ndash; WorkflowAssistants/workspaces/assistant/assistant.json](https://github.com/ZEISS/zeiss-inspect-app-examples/blob/main/AppExamples/misc/WorkflowAssistants/workspaces/assistant/assistant.json) for an example.
```

## Workflow assistant JSON format

```{note}
Optional parameters are marked with '**\***'.
```

### Top level elements

The following JSON elements are used at the Workflow assistant's top level.

id	(string)
: UUID for unique identification of the Workflow assistant definition

name (string)
:	Display name of the definition

using	(List of Objects)
:	Shorthands for definition IDs for easier usage

objects (List of Objects)
:	List of all elements provided by this workflow definition. Each entry is a JSON object describing a single element.

Example:

```
{
  "id": "8d7724f7-5cf3-4262-b39a-7228d69952e8",
  "name": "Minimal example",
  "using": [
    {
      "name": "inspect",
      "id": "bd0ec39e-4155-4d7d-9771-9ed0d5f86e59"
    }
  ],
  "objects": [
    ...
  ]
}
```

### Common workflow assistant object attributes

These attributes are common for all Workflow assistant elements listed in the following sections.

type (String)
: Workflow assistant element type identifier\
Examples: `"type": "MenuPage"`, `"type": "NextPageEntry"`

id* (string)
: Reference ID of this object\
Example: `"id": "label_menu"`

name* ([String-like](#string-like-entry))	
: General name of element, default: `"<Default name>"`
Example: `"name": "element 1"` 

description* ([String-like](#string-like-entry))
: General description of the element\
Example: `"decription": "this does something"`

icon* ([Icon-like](#icon-like-entry))
: Icon to be displayed\
Example: `"icon":"surface_section_menu"`

position*	(Object)
: Insert the element at a specific position in an existing Workflow assistant structure

* "insert" (id): Element to insert into
* "before" (id): Position hint, i.e. insert before this element (may be empty)

Example:
```
{
  "insert" = "inspection_home",
  "before" = "inspection_menu"
}
```

### Pages

#### MenuPage

Basic type of page which displays elements in form of a list.

entries (List of MenuEntries)
: List of [Menu entries](#menu-entries). Each entry must be a valid JSON object describing a Menu entry element.\
Example: `[ { entryA }, { entryB } ]`.


#### WizardPage

Page which displays multiple consecutive steps as a list of accordions with navigation buttons between them.

steps (List of WizardSteps)
: List of [WizardSteps](#wizard-steps), each entry should be a valid json object describing a WizardSteps element.\
Example: `[ { entryA }, { entryB } ]`

#### EmbeddedCommandPage	

Page with an embedded command. The page ID is defined by the given command.

command (string)
: Command to execute, usually with a dialog.\
Example: `comparison.create_min_max_deviation_label`

### Menu entries

#### AccordionEntry

Accordion entries are a group of menu entries which can be collapsed and expanded.

entries (List of MenuEntries)
: List of [Menu entries](#menu-entries), each entry should be a valid JSON object describing a Menu entry element.\
Example: `[ { entryA }, { entryB } ]`


#### NextPageEntry

A next page entry leads to a new page.

page ([Page-Object](#pages))
: Either a single page ID if referring to an already existing page or a definition of a new page.\
Example: `label_menu` / `{ pageA }`


#### CommandEntry

A command entry allows to execute a command. If the command has a dialog, this dialog will be embedded in the workflow assistant.

command (string)
: Command to execute.\
Example: `inspection.inspect_by_deviation_label`

### Wizard steps

#### EmbeddedCommandStep

A wizard allows to execute a sequence of commands. The command dialogs are embedded into the workflow assistant.

```{note}
One of the fields 'command' and/or 'commands' must exist.
```

command (string)
: Command to execute\
Example: `inspection.inspect_by_deviation_label`

commands (List of Objects)
: Each object in the list can either be

* a string with the command
* an object with the following keys:
  * "command"
  * "info"* 
  * "info_help_id"* 
  * "interactive"*

Example: `[ commandA, commandB ]`

interactive* (boolean)
: Defines whether to execute the command in interactive mode. (Default: True)

info* ([String-like](#string-like-entry))
: Descriptive info text for this wizard step\
Example: `Compute statistics for deviation analysis on an inspection element with color deviation representation. Select an area on the color deviation representation with any of the point selection functions."`

info_help_id* (string)
: Reference to a help article in the ZEISS Quality Tech Guide\
Example: `"info_help_id": "cmd_comparison_create_min_max_deviation_label"`

### Advanced entry types

This section introduces some advanced data types for definition of strings and icons.

### String-like entry

#### String

Plain string

#### Translated (Object)

Runtime-translated string, based on xliff files located in the App's `languages/` folder.

translate (boolean)
: Translate the string at runtime

text (string)
: Text to translate

id (string)*
: Automatically generated translate id

### Icon-like entry

Icon-like entries can be defined in multiple ways listed below. They provide an icon to display as part of an element in the Workflow Assistant. Currently only .svg files are fully supported.

#### Simple (string)

Specifies how and where to load an icon from (see [Advanced](#advanced-object) type below for more information about `<path>` and `<mode>`). Always uses "auto" dark mode setting.

`"<path>"` or `"<mode>::<path>"`

Example: "inspection_home" / `"app::icons/workflow/my_icon.svg"`

#### Advanced (object)

path (string)
: Path to an icon or value of icon (if using a decoder)

mode* (string)	
: Mode to use to interpret the path. (default: "system")

  * "system": Loads a system icon with the given name. Example: `{"path": "inspection_home", "mode": "system"}`
  * "app"
    * Loads an icon from the originating App. The path is relative to the App's root-folder. Example: `{"path": "icons/workflow/my_icon.svg"}`
    * Loads an icon from any App specified by an AddOnUrl. Example: `{"path": "acp:///b2cc0788-1a2b-4652-ba7e-3f789126006e/icons/workflow/my_icon.svg", "mode": "app"}`
  * "file": Loads an icon based on an absolute file path. **Should be used with care** (mostly while testing) due to poor portability. Example: `{"path": "C:\\Downloads\\my_icon.svg", "mode": "file"}`
  * "base64": Decodes the icon from an embedded [base64](https://en.wikipedia.org/wiki/Base64)-encoded string. Example: {"path": "PHN2ZyBpZD0iTGF5ZXJfMSI...", "mode": "base64"}

dark (string)	
: Dark mode mode option. System icons ignore this setting.

  * "none": Do not change icon in dark mode.
  * "auto": Generate brightend version for darkmode automatically.

## Related

* [App Examples &ndash; WorkflowAssistants](https://github.com/ZEISS/zeiss-inspect-app-examples/tree/main/AppExamples/misc/WorkflowAssistants)
