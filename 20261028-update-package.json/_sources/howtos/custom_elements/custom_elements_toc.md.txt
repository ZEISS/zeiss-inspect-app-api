![New in Version 2027](https://img.shields.io/badge/New-Version_2027-20B2AA)

# Custom elements

```{note}
Since ZEISS INSPECT 2027, custom elements are the standard replacement for <a href="https://zeiss.github.io/zeiss-inspect-app-api/2026/howtos/scripted_elements/scripted_elements_toc.html">Scripted elements</a>. Scripted elements remain supported for backward compatibility.
```

Custom elements are ZEISS INSPECT elements which are defined using the Python <a href="../../python_api/python_api.html#gom-api-extensions">Extensions API</a>. They can be parametric, i.e. their parameters may depend on other elements. If a dependency changes, a recomputation of the custom element is triggered. 

```{note}
In this How-to chapter, the user-facing term "custom elements" is used. The current API uses the `Custom*` class family (for example `CustomElement`, `CustomActual`, `CustomNominal`, and `CustomInspection`). `Scripted*` class names are documented as legacy aliases.
```

```{seealso}
Custom elements are commonly used as data providers for interactive diagrams.

Continue with [Using Custom Diagrams](../using_custom_diagrams/using_custom_diagrams.md) once you are familiar with defining custom element payloads.
```
 
The following How-to sections will introduce the concept of custom elements.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :titlesonly:
   
   custom_nominals_actuals
   custom_inspections
   custom_sequences
```