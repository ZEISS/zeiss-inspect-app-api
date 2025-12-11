---
myst:
   html_meta:
      "description": "ZEISS INSPECT 2026 App Python API Documentation"
      "keywords": "Metrology, ZEISS INSPECT, Python API, GOM API, Scripting, Add-ons, Apps, How-tos, Examples, Specification, Documentation"
--- 

# ZEISS INSPECT 2026 App Development Documentation 

Welcome to the [ZEISS INSPECT 2026 App](https://www.zeiss.com/metrology/en/software/zeiss-inspect/zeiss-inspect-apps.html) development documentation. With Apps, you will be able to customize and extend the functionality of your ZEISS INSPECT software. 
You can include several template configurations from the software, as well as completely new workflows programmed in Python.

```{important}
Creating Apps is a rather advanced topic, so you should be familiar with the basic inspection concept of ZEISS INSPECT beforehand. New to ZEISS INSPECT? You find an introduction in the ZEISS Quality Tech Guide:

[Access Point: ZEISS INSPECT](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/access_point_gom_inspect.html)

Or, depending on your application, you might be interested in the specific articles:
* [Access Point: ZEISS INSPECT X-Ray](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/access_point_volume_inspect.html)
* [Access Point: ZEISS INSPECT CMM](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/access_point_zeiss_inspect_cmm.html)
* [Access Point: ZEISS INSPECT VMM](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/access_point_zeiss_inspect_vmm.html)
* [Access Point: Airfoil Inspection](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/access_point_gom_blade_inspect.html)
* [Access Point: ZEISS CORRELATE](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/access_point_zeiss_inspect_correlate.html)

```
If you are new to Apps, you find some introductions in the ZEISS Quality Tech Guide:

* [Introduction to Apps](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/introduction_to_add-ons.html)
* [How to Create a Basic App](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/how_to_create_a_basic_add_on.html)
* [How to Create an Advanced App](https://techguide.zeiss.com/en/zeiss-inspect-2026/article/how_to_create_an_advanced_add_on.html)

Check out the ZEISS INSPECT Apps news page!

```{eval-rst}
.. toctree::
   :maxdepth: 1
   
   news/news
```

```{eval-rst}
.. toctree::
   :hidden:

   news/20251127-jupyter-notebook
   news/20251126-update-dialog-widgets
   news/20251125-release-2026
   news/20250804-workflow-assistant
   news/20250516-update-vscode
   news/20250123-gom-math
   news/20250106-app-doc-link
   news/20241217-scripted-diagrams
   news/20241211-services
   news/20241205-autodialogcontext
   news/20241028-insert-file
   news/20241125-release-2025
   news/20240315-element-selection
   news/20240314-internationalization-tool-update
   news/20240307-mesh-selection
   news/20240307-csharp_dotnet
   news/20240209-test-coverage
   news/20240205-using-gui-libraries
   news/20240130-working-with-stages
   news/20240130-using-wheelhouses
   news/20240119-scripted-elements-examples
   news/20240115-software-starting-options
   news/20240115-project-keywords
   news/20231215-api-examples
   news/20231221-faq
   news/welcome
```

Furthermore, we recommend following our How-to Guides to get you started.

```{eval-rst}
.. _how-to-guides-basic:

.. toctree:: 
   :maxdepth: 1
   :caption: How-to Guides – Basic

   howtos/python_api_introduction/python_api_introduction
   howtos/python_api_introduction/selecting_elements
   howtos/using_app_editor/using_app_editor
   howtos/app_file_format/app_file_format
   howtos/python_api_introduction/file_selection_dialog
   howtos/user_defined_dialogs/user_defined_dialogs
   howtos/user_defined_dialogs/dialog_widgets
   howtos/user_defined_dialogs/executing_dialogs
   howtos/scripting_solutions/scripting_solutions
   howtos/faq/faq
```

```{eval-rst}
.. _how-to-guides-intermediate:

.. toctree::
   :maxdepth: 1
   :caption: How-to Guides – Intermediate

   howtos/using_vscode_editor/using_vscode_editor
   howtos/app_documentation/app_documentation
   howtos/custom_elements/custom_elements_toc
   howtos/scripted_elements/scripted_elements_toc
   howtos/python_api_introduction/using_script_resources
   howtos/stages/stages
   howtos/project_keywords/project_keywords
   howtos/localization/localization
   howtos/testing_apps/testing_apps
```

```{eval-rst}
.. _how-to-guides-expert:

.. toctree::
   :maxdepth: 1
   :caption: How-to Guides – Expert

   howtos/user_defined_dialogs/wizard_control
   howtos/user_defined_dialogs/creating_wizard_dialogs
   howtos/using_gui_libraries/using_gui_libraries
   howtos/using_shared_environments/using_shared_environments
   howtos/using_wheelhouses/using_wheelhouses
   howtos/adding_workspaces_to_apps/adding_workspaces_to_apps
   howtos/workflow_assistant/workflow_assistant
   howtos/using_services/using_services
   howtos/using_scripted_diagrams/using_scripted_diagrams
   howtos/using_jupyter_notebook/using_jupyter_notebook
   howtos/using_jupyter_notebook/using_jupyter_and_vscode
   howtos/starting_options/starting_options
   howtos/scripting_legacy_projects/scripting_legacy_projects
```

If you already know how to create an App and now you are interested in Python programming in ZEISS INSPECT, take a look at our collection of Python examples.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :caption: Python API Examples

   python_examples/index
   python_examples/examples_overview
```

Available API functions are documented in the Specification.

```{eval-rst}
.. toctree::
   :maxdepth: 2
   :caption: Python API Specification

   python_api/python_api
   python_api/scripted_elements_api
   python_api/resource_api
```

```{mermaid}

    sequenceDiagram
      participant Alice
      participant Bob
      Alice->John: Hello John, how are you?
```

