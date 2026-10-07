# App file format

## Introduction

```{note}
An ZEISS INSPECT App file (extension: *.addon) is a ZIP archive with pre-defined folder- and filenames. 
```

While an App file will be created and modified with the App Editor in most cases, it can also be unzipped/edited/zipped manually if necessary.

## Structure

### Folder structure

| File              | Description                                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| `<other folder>/` | All other folders are containing App content. The format of this content is discussed below.                 |
| `doc/`            | App documentation as displayed in the Software Store. Must contain a `README.md` file in markdown format and release notes in markdown format and PDF. |
| `icon.png`        | App icon as displayed in the App Manager and the Software Store                                              |
| `key.enc`         | App protection and licensing information in case the App is protected                                        |
| `license/`        | Terms-of-use related to this App. Can contain a set of text files like `license.txt` , `license_numpy.txt` , ... which will be displayed and must be acknowledged upon App installation                                                                                              |
| `metainfo.json`   | App metainfo data (title, description, version, ...); see [`metainfo.json` documentation](#metainfojson-documentation)                             |

### Content types

```{note}
The top level folders determine the "content type". Inside these top level folders, a separate sub folder must be provided for each item.
```

| Folder / Provider name    | Content type                                    | Notes        |
| ------------------------- | ----------------------------------------------- | ------------ |
| backgrounds	            | Environment (rendering) backgrounds	          |              |
| cad_import_modes	        | CAD import templates	                          |              |
| configurations	        | Visibility settings	                          | INTERNAL     |
| diagrams	                | Diagrams (3D view)	                          |              |
| element_properties	    | Element creation properties	                  |              | 
| explorer_filter_templates	| Explorer filter settings	                      |              |
| export_templates	        | Element export scripts	                      |              |
| gradient_color_maps	    | Templates for volume color gradient	          |              |
| gvf_templates	            | Gray value feature templates	                  |              |
| inspection_styles	        | I-Inspect configurations	                      |              |
| import_templates	        | Element import scripts	                      |              |
| iso_tolerance_tables	    | ISO tolerance table templates	                  |              |
| keywordsets	            | Project keywords	                              |              |
| labels	                | Element label templates	                      |              |
| languages	                | Translation files	                              |              |
| legends	                | 3D legend templates	                          |              |
| lightingconfigs	        | Light setup templates (rendering)	              |              |
| materials                 | Material templates (rendering)	              |              |
| perspectives	            | UI configurations	                              |              |
| range_color_maps	        | Templates for volume color ranges	              |              |
| reports	                | Report page templates	                          |              |
| scripts	                | Scripts	                                      |              |
| scripted_elements	        | Scripted elements	                              |              |
| surface_classifications	| Surface defect classifications	              |              |
| tables	                | Table templates (3D view)	                      |              |
| terms_of_use	            | Collection of terms-of-use for App creation     |              |
| tolerance_legends	        | Tolerance legends (3D)	                      |              |
| user_defined_checks	    | User defined checks	                          |              |
| user_defined_inspection_principles | User defined inspection principles     |              |
| workflow_assistant        | Workflow assistant configuration                |              |
| workspaces                | Workspace definitions                           |              |

### Content data

```{note}
Each "content object" consists of a folder in one of the "content type" (top level) folders.
```

* A "content object" is a single template/script/element/... distributed via an App.
* Each "content object" is represented by the content of a folder in the "content type" folder matching the content type.
* The exact format of the content representation depends on the "content type".
* The name of the "content object" is the same as its folder's name.
* For template-like objects, there is always a JSON file with administrative data present. Other types may vary.

#### Example: Labels

**Folder layout 'labels'**

```
metainfo.json
labels
|-- Name
|   |--Name.json
|-- Results
|   |-- Results.json
...
```

* The folder names 'Name' and 'Results' are the templates' names
* The JSON file in each folder contains both administrative data and content information

**Name.json**

```json
{
    "content": {
        "!all:" {
            "label_background": "gom.Color (0, 0, 0, 0)",
            "label_border_mode": "'none'",
            "...": "...",
            "label_text": "..."
        },
        "...": "..."
    },
    "sort_index": 1,
    "uuid": "4a6ef87a-5214-4089-bdc3-5a96cf8b5108"
}
```

#### Example: Scripts

**Folder layout 'scripts'**
```
scripts/
|-- Tools/
|   |-- Workspaces
|       |-- create_workspace.py
|       |-- create_workspace.metainfo
|-- ...
...
```

## `metainfo.json` documentation

Example: <a href="https://github.com/ZEISS/zeiss-inspect-app-examples/blob/main/AppExamples/data_interfaces/CheckResultsDataArray/metainfo.json">AppExamples/data_interfaces/CheckResultsDataArray/metainfo.json</a>

### Mandatory elements

- **title**: `String` &ndash; App title
- **uuid**: `String` &ndash; App UUID
- **version**: `String` &ndash; App version
- **author**: `String` &ndash; App author
- **description**: `String` &ndash; App short description 
- **software-version**: `String` &ndash; ZEISS INSPECT version
- **software-revision**: `String` &ndash; ZEISS INSPECT revision
- **licensing**: `Object` &ndash; Which license is required to run the App
    - **licenses**: `[[String]]`
    - **product-codes**: `[[String|int, String]]`

### Optional elements

- **documentation**: `String` &ndash; Link (URL) to external App documentation, see <a href="../app_documentation/app_documentation.html#link-to-external-documentation">Documenting Apps – Link to external documentation</a>
- **environment**: `String` &ndash; Shared App environment, see <a href="../using_shared_environments/using_shared_environments.html">Using shared environments</a>
- **services**: `Object` &ndash; Service definitions, see <a href="../using_services/using_services.html">Using services</a>
    - **endpoint**: `String`
    - **name**: `String`
    - **script**: `String`
- **settings**: `Object` &ndash; App settings, see <a href="../../python_api/python_api.html#gom-api-settings">gom.api.settings</a>

### ZEISS Quality Software Store

- **technical-category**: `String` &ndash; One of the following options
    - `Element Transformation`
    - `Import and Export`
    - `Norm-Based Evaluation`
    - `Surface Inspection`
    - `Curve Inspection`
    - `Airfoil Inspection`
    - `Multipart`
    - `Section-Based Inspection`
    - `Geometries`
    - `Testing`
    - `Collections`
    - `Measuring Accuracy`
    - `Miscellaneous`
    - `App Examples`
- **business-category**: `String` &ndash; One of the following options
    - `major`
    - `basic`
    - `minor`
- **compatible-software**: `[String]`  &ndash; Combination of the following options
    - `ZEISS INSPECT Optical 3D`
    - `ZEISS INSPECT X-Ray`
    - `ZEISS INSPECT CMM`
    - `ZEISS INSPECT VMM`
    - `ZEISS CORRELATE`

### Additional information

- **build**: `String` &ndash; App build number
- **labels**: `[String]`
- **references**: `[String]` &ndash; Reference links used for <a href="../../python_examples/examples_overview.html">ZEISS INSPECT App Examples Overview</a>
- **tags**: `[String]` &ndash; Tags used for <a href="../../python_examples/examples_overview.html">ZEISS INSPECT App Examples Overview</a>

## Python script `<name>.metainfo` documentation

Most elements of the script `.metainfo` file are available via the 'Edit Properties...' dialog in the App editor.

![Edit script properties dialog](assets/edit_script_properties.png)

### Examples

* Basic script: <a href="https://github.com/ZEISS/zeiss-inspect-app-examples/blob/main/AppExamples/data_interfaces/CheckResultsDataArray/scripts/check_results_data_array.metainfo">AppExamples/data_interfaces/CheckResultsDataArray/scripts/check_results_data_array.metainfo</a>
* Scripted actual element: <a href="https://github.com/ZEISS/zeiss-inspect-app-examples/blob/main/AppExamples/scripted_actuals/ScriptedActualPoint/scripts/OffsetPointSimple.metainfo">AppExamples/scripted_actuals/ScriptedActualPoint/scripts/OffsetPointSimple.metainfo</a>
* Scripted check: <a href="https://github.com/ZEISS/zeiss-inspect-app-examples/blob/main/AppExamples/scripted_checks/ScriptedCurveCheck/scripts/ScriptedCurveCheck.metainfo">AppExamples/scripted_checks/ScriptedCurveCheck/scripts/ScriptedCurveCheck.metainfo</a>

### JSON elements

- **display_name**: `String` &ndash; Script's name shown in menu\
<br>&ndash; or &ndash;
- **display_name**: `Object` &ndash; Script's name and translation information ![New in Version 2025](https://img.shields.io/badge/New-Version_2025-orange)
    - **id**: `String` &ndash; Translation element ID
    - **text**: `String` &ndash; Name shown in menu if not replaced by translated name
    - **translate**: `Boolean` &ndash; Name is translated if `true`
- **icon**: `String` &ndash; Script's icon shown in menu (uuencoded). Default icon is used if empty.
- **iinspect_condition**: `String` &ndash; Condition for enabling I-Inspect entry, e.g. `true` or `type == 'section'`
- **folded_blocks**: `[Integer]` &ndash; Line numbers (zero-based) of folded code blocks in the App Editor

- **main_menu_path**: `Object` &ndash; Script's position in ZEISS INSPECT menu
    - **anchor**: `Object` &ndash; Anchor element of script's menu structure
        - **item**: `String` &ndash; Anchor element item name; empty if no anchor element is used
        - **submenu**: `[String]` &ndash; Submenu hierarchy
        - **type**: `String `&ndash; Anchor element type
            - `command`
            - `submenu`
    - **script**: `String` &ndash; Python script path; `<prefix><path><script>`\
    `<prefix>`: `userscript.` (normal script) or `ude.` (user defined element, i.e. scripted element or scripted check)\
    `<path>`: Path relative to Apps' `scripts/` folder (double underscore is used as path separator)\
    `<script>`: Script file name without extension `.py`
    - **submenu**: `[String]` &ndash; Script's submenu created at anchor element

- **multicreation_script**: `Boolean` &ndash; Reserved for ZEISS internal use. Default: `false`.

- **script_element_type**: `String` &ndash; <a href="../scripted_elements/scripted_actuals.html">Scripted actual element</a> type
    - `none`
    - `circle`
    - `cone`
    - `curve`
    - `cylinder`
    - `distance`
    - `point`
    - `point_cloud`
    - `section`
    - `surface`
    - `surface_curve`
    - `volume`
    - `volume_defects`
    - `volume_region`
    - `volume_section`

- **script_check_type**: `String`  &ndash; <a href="../scripted_elements/scripted_checks.html">Scripted checks</a> type
    - `scalar`
    - `scalar_curve`
    - `scalar_surface`

- **show_in_iinspect**: `Boolean` &ndash; Show script in I-Inspect if `true`

- **show_in_menu**: `Boolean` &ndash; Show script in menu Apps ► Execute Script if `true`;\
  the menu hierarchy is created from the script's path within the App's `scripts/` folder

- **uuid**: `String` &ndash; Script's UUID

## FAQ

### Structure

#### Why is there a folder for every single element?
* The App Editor can handle the elements transparently in this way. Just the folder is dragged & dropped, visible etc., while the content is abstracted and can edited (e.g. in a graphical editor)
* The content format specification of an element can easier be changed over time
