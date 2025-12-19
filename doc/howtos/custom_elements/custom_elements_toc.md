![New in Version 2026](https://img.shields.io/badge/New-Version_2026-red)

# Custom elements

```{note}
Custom elements will replace [Scripted elements](../scripted_elements/scripted_elements_toc.md) in future versions of ZEISS INSPECT.
```

Custom elements are ZEISS INSPECT elements which are defined using the Python <a href="../../python_api/python_api.html#gom-api-extensions">Extensions API</a>. They can be parametric, i.e. their parameters may depend on other elements. If a dependency changes, a recomputation of the custom element is triggered. 
 
The following How-to sections will introduce the concept of custom elements.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :titlesonly:
   
   custom_nominals_actuals
   custom_checks
   custom_diagrams
```