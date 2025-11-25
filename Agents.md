# Agents.md - ZEISS INSPECT App API Documentation

## Overview

This document provides guidance for AI agents interacting with the ZEISS INSPECT App API documentation repository at https://github.com/ZEISS/zeiss-inspect-app-api.

## Repository Purpose

**Documentation sources** for App development of ZEISS INSPECT metrology software. This repository contains the source files that generate the comprehensive App development documentation website.

**Rendered Documentation**: https://zeiss.github.io/zeiss-inspect-app-api/

## What Can AI Agents Help With?

When users ask about ZEISS INSPECT App development, agents can assist with:

1. **API Reference Queries** - Explaining specific API functions and their usage
2. **Development Guidance** - Directing users to appropriate how-to guides based on skill level
3. **Code Examples** - Helping users understand Python API examples and patterns
4. **Architecture Questions** - Explaining App structure, scripted elements, and data interfaces
5. **Feature Discovery** - Helping users find the right API functions for their needs
6. **Troubleshooting** - Guiding users to relevant documentation sections
7. **Version Navigation** - Helping users find documentation for specific ZEISS INSPECT versions
8. **What's New** - New features or documentation 

## Key Resources

- **Repository**: https://github.com/ZEISS/zeiss-inspect-app-api
- **Main Documentation (2026)**: https://zeiss.github.io/zeiss-inspect-app-api/2026/
- **Main Documentation (2025)**: https://zeiss.github.io/zeiss-inspect-app-api/2025/
- **Main Documentation (2023)**: https://zeiss.github.io/zeiss-inspect-app-api/2023/
- **Main Documentation (2022)**: https://zeiss.github.io/gom-software-python-api/2022/
- **App Examples**: https://zeiss.github.io/zeiss-inspect-app-api/2026/python_examples/examples_overview.html
- **Example Apps Repository**: https://github.com/ZEISS/zeiss-inspect-app-examples
- **ZEISS Quality Tech Guide**: https://techguide.zeiss.com/en/zeiss-inspect-2026/
- **Apps News**: Check documentation for latest updates

## Documentation Structure

### 1. How-to Guides

The documentation is organized by difficulty level:

#### Basic Level
- **Python API Introduction** - Getting started with ZEISS INSPECT Python API
- **Creating Wizard Dialogs** - Building multi-step dialog interfaces
- **Using Additional Python GUI Libraries** - Integrating external UI frameworks

#### Intermediate Level
- **Using Shared Environments** - Managing Python environments across Apps
- **Using Python Wheelhouses** - Incorporating external Python packages
- **Adding Workspaces to Apps** - Customizing the ZEISS INSPECT interface
- **Workflow Assistant** - Creating guided workflows for users
- **Using Services** - Implementing background services in Apps

#### Expert Level
- **Using Scripted Diagrams** - Creating custom data visualizations
- **Using Jupyter Notebook** - Interactive development with Jupyter
- **Using Jupyter Notebook with VSCode** - Advanced IDE integration
- **Software and Script Starting Options** - Advanced configuration options
- **Scripting with Legacy Projects** - Working with part-less projects

### 2. Python API Specification

Complete reference documentation for:
- **gom.api.imaging** - Image point/pixel operations and photogrammetry
- **gom.api.project** - Project data access and management
- **gom.api.addons** - Add-on/App management and inspection
- **gom.api.progress** - API for accessing the progress bar in the main window
- **gom.api.script_resources** - API for the ResourceDataLoader
- **gom.api.scripted_checks_util** - Utility functions for scripted checks
- **gom.api.services** - API for accessing the script based API extensions (services)
- **gom.api.testing** - API with testing and verification functions
- **gom.api.settings** - Persistent configuration storage
- **gom.api.interpreter** - API for accessing python script interpreter properties
- **gom.api.introspection** - API for accessing the available API modules, functions and classes (for debugging and testing)
- **Scripted Elements API** - Building custom geometric elements
- **gom.Resource API** - Accessing App resources

**Full API Documentation**:
- 2026: https://zeiss.github.io/zeiss-inspect-app-api/2026/python_api/python_api.html
- 2025: https://zeiss.github.io/zeiss-inspect-app-api/2025/python_api/python_api.html
- 2023: https://zeiss.github.io/zeiss-inspect-app-api/2023/python_api/python_api.html

### 3. Python API Examples

Comprehensive examples organized by category (see separate examples repository), tagg

## Core API Modules Reference

### gom.api.imaging
**Purpose**: Image point/pixel operations to query images from the measurements of an object.

**Key Functions**:
- `compute_epipolar_line()` - Compute epipolar line coordinates from pixel projections
- `compute_pixels_from_point()` - Convert 3D point coordinates to 2D image pixels (photogrammetric)
- `compute_point_from_pixels()` - Reconstruct 3D points from pixels in multiple images

**Terminology**:
- **point** = 3D coordinate in a measurement
- **pixel** = 2D coordinate in an image

**Common Use Cases**:
- Converting between 3D model space and 2D image space
- Stereo photogrammetry calculations
- Finding corresponding points across camera views

### gom.api.project
**Purpose**: Accessing project structures and data

**Key Functions**:
- `get_image_acquisition()` - Get image acquisition object for specific measurement/camera/stage
- `get_image_acquisitions()` - Get multiple image acquisition objects
- `create_progress_information()` - Create progress status indicators for long operations

**Camera Types**:
- `left camera` - Left camera in stereo system or only camera in single camera system
- `right camera` - Right camera in stereo system
- `photogrammetry` - TRITOP photogrammetry camera

**Common Use Cases**:
- Accessing measurement images from different cameras
- Managing stage-based measurements
- Displaying progress for long-running operations

### gom.api.addons
**Purpose**: Managing and inspecting installed Apps (Add-ons)

**Key Capabilities**:
- Query installed Apps: `get_installed_addons()`, `get_addon(uuid)`, `get_current_addon()`
- Read App files: `AddOn.read(filename)`
- Write to current App: `AddOn.write(path, data)` (self-modification only)
- Check App properties: `is_protected()`, `has_license()`, `is_edited()`
- Access App metadata: `get_id()`, `get_name()`, `get_level()`

**Important Notes**:
- ⚠️ Apps can only modify their own content
- Protected Apps are encrypted and cannot be read
- Apps in edit mode are directory-based, not ZIP-based

**Common Use Cases**:
- Self-updating Apps during migration
- Reading App resources programmatically
- Checking license status
- Listing App files and structure

### gom.api.settings
**Purpose**: Persistent configuration storage for Apps

**Key Functions**:
- `get(key)` - Read setting value
- `set(key, value)` - Write setting value
- `list()` - List all available keys for current App

**Configuration Definition**:
- Settings must be defined in App's `metainfo.json` file
- Settings appear in application preferences dialog (if `visible: true`)
- Supports: integers, floats, strings, booleans, file selectors

**File Selector Modes**:
- `any` - Any file
- `new` - New file in writable directory
- `load_file` - Existing file (reading)
- `load_files` - Multiple existing files (reading)
- `save_file` - Existing or new file (writing)
- `load_dir` - Existing directory (reading)
- `save_dir` - Existing directory (writing)
- `exec` - Existing executable file

**Common Use Cases**:
- Storing user preferences persistently
- File path storage
- Application thresholds and parameters

## Guidance for User Queries

### When Users Ask About:

**"How do I get started with App development?"**\
→ Point to Python API Introduction (Basic level)\
→ Recommend reviewing ZEISS Quality Tech Guide for ZEISS INSPECT basics\
→ Suggest starting with simple examples from examples repository\
→ Note: App development is advanced - requires ZEISS INSPECT familiarity

**"How do I access [images/measurements/check results]?"**\
→ Direct to `gom.api.project` for project data access\
→ Direct to `gom.api.imaging` for image/pixel operations\
→ Point to data_interfaces examples in examples repository

**"How do I create custom [dialogs/UI/widgets]?"**\
→ Basic: "User-defined Dialogs" how-to guide\
→ Basic: "Creating Wizard Dialogs" how-to guide\
→ Intermediate: "Using Additional Python GUI Libraries"\
→ Refer to dialog_widgets examples

**"How do I [use/create] a service?"**\
→ Use `gom.api.services` module\
→ Intermediate: "Using Services" how-to guide\
→ Explain relation between service scripts and `services` definition in `metainfo.json`\
→ Refer to ServiceExample

**"How do I convert between 3D points and 2D pixels?"**\
→ Use `gom.api.imaging.compute_pixels_from_point()` (3D → 2D)\
→ Use `gom.api.imaging.compute_point_from_pixels()` (2D → 3D)\
→ Refer to PointPixelTransformations example

**"How do I store settings/preferences?"**\
→ Use `gom.api.settings` module\
→ Define settings in `metainfo.json` first\
→ Explain persistent storage across sessions

**"How do I use external Python packages?"**\
→ Explain wheel installation in App structure\
→ Intermediate: "Using Python Wheelhouses" how-to guide

**"How do I create [custom/parametric] geometric elements?"**\
→ Point to Scripted Elements API\
→ Refer to scripted_actuals examples (e.g. ScriptedActualCurve)\
→ Explain actual vs. nominal elements

**"How do I create custom inspection checks?"**\
→ Point to scripted_checks examples\
→ Explain scalar vs. curve vs. surface checks\
→ Note custom coordinate system support

**"Can I use Jupyter Notebooks?"**\
→ Yes - Expert level guide available\
→ Supports both standalone Jupyter and VSCode integration\
→ Point to relevant how-to guides

**"What versions are supported?"**\
→ Current documentation: ZEISS INSPECT 2026, 2025 and 2023\
→ Check documentation for specific version requirements\
→ Examples typically require ZEISS INSPECT 2023 or later

## Important Technical Concepts

### App Structure
- Apps are ZIP files with specific directory structure
- Contains: scripts, templates, definitions, resources
- `metainfo.json` defines App metadata and settings schema
- Can be edited (directory-based) or finished (ZIP-based)

### Image Acquisition Objects
- Proxy between image data structures and processing functions
- Required for accessing measurement images
- Specify: measurement, camera type, stage index

### Scripted Elements
- Three types:
1. **Scripted Actuals** - Custom geometric elements (surfaces, points, etc.)
2. **Scripted Checks** - Custom inspection checks (scalar, curve, surface)
3. **Scripted Diagrams** - Custom data visualizations
- Scripted element type must be set in script's `.metainfo` file
- Run in separate Python process
- gom.script.* and gom.interactive.* commands cannot be used in a scripted element

### Coordinate Systems
- Project coordinate system (3D)
- Image coordinate system (2D, origin = upper left corner)
- Custom coordinate systems for checks
- Photogrammetric transformations between systems

### Progress Information
- For long-running operations
- Updates main application progress widget
- Retrieved via `gom.api.project.create_progress_information()`

## Common Code Patterns

### Accessing Images from Measurements
```python
measurement = gom.app.project.measurement_series['Series'].measurements['M1']
stage = gom.app.project.stages['Stage 1']
left = gom.api.project.get_image_acquisition(measurement, 'left camera', [stage.index])[0]
right = gom.api.project.get_image_acquisition(measurement, 'right camera', [stage.index])[0]
```

### 3D to 2D Conversion
```python
point = gom.app.project.actual_elements['Point 1'].coordinate
pixels = gom.api.imaging.compute_pixels_from_point([(point, left), (point, right)])
```

### 2D to 3D Conversion
```python
pixel_pair = [(gom.Vec2d(1587.74, 793.76), img_left), 
              (gom.Vec2d(2040.22, 789.53), img_right)]
points = gom.api.imaging.compute_point_from_pixels([pixel_pair], use_calibration=False)
```

### Settings Usage
```python
# Read setting
width = gom.api.settings.get('dialog.width')

# Write setting
gom.api.settings.set('dialog.width', 640)

# List all settings keys
keys = gom.api.settings.list()
```

### Iterating Through Apps
```python
for addon in gom.api.addons.get_installed_addons():
    if not addon.is_protected():
        print(addon.get_name(), addon.get_id())
```

## Common Workflows to Support

1. **Finding API Function**
   - Understand user's goal
   - Identify appropriate module (imaging/project/addons/settings)
   - Provide function signature and example
   - Link to API specification

2. **Understanding API Function**
   - Explain parameters and return values
   - Clarify terminology (point vs pixel, acquisition objects, etc.)
   - Provide practical example
   - Note API version requirements

3. **Implementing Feature**
   - Guide to appropriate how-to guide by skill level
   - Suggest relevant examples
   - Explain required concepts
   - Provide code patterns

4. **Debugging Issues**
   - Check API version compatibility
   - Verify parameter types and values
   - Check settings definition in metainfo.json
   - Direct to FAQ or documentation search

## Version Compatibility

- **Current Documentation**: 2026, 2025, 2023
- **API Versions**: Functions note minimum API version required
- **Software Requirements**: Most examples require ZEISS INSPECT 2023+
- Users should check specific example requirements

## Important Notes for Agents

- Always emphasize that App development is **advanced** - users should know ZEISS INSPECT basics first
- Reference the ZEISS Quality Tech Guide for foundational ZEISS INSPECT knowledge
- API is under active development - some features marked "under development"
- Protected Apps cannot be read or modified
- Apps can only modify their own content
- Settings must be defined in metainfo.json before use
- Direct complex questions to official documentation
- Pixel coordinates: origin is **upper left corner**

## Support Escalation

For issues beyond API documentation:
- **ZEISS Quality Tech Guide**: https://techguide.zeiss.com/
- **Training**: https://qualitytraining.zeiss.com/
- **Software Store**: https://software-store.zeiss.com
- **Examples Repository**: https://github.com/ZEISS/zeiss-inspect-app-examples

## Related Resources

- **Example Apps Repository**: Contains working code examples for API features
- **ZEISS INSPECT Software**: Main metrology application
- **ZEISS Quality Software Store**: Download Apps
- **ZEISS Quality Training Center**: Comprehensive training courses
