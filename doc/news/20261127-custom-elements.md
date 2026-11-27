# Custom Elements in ZEISS INSPECT 2027

```{eval-rst}
.. feed-entry::
   :date: 2026-11-27 09:55
```

In ZEISS INSPECT 2027, [custom elements](../howtos/custom_elements/custom_elements_toc.md) are the standard replacement for scripted elements. They allow Apps to extend the software with application-specific geometry and inspections that integrate into familiar project workflows. Existing scripted elements remain supported for backward compatibility.

The updated documentation introduces the current API and expands the guidance for three areas:

* [Custom nominal/actual elements](../howtos/custom_elements/custom_nominals_actuals.md) define geometry such as points, curves, and surfaces using Python. They can depend on other project elements and are recalculated when those dependencies change.
* [Custom inspections](../howtos/custom_elements/custom_inspections.md) evaluate scalar properties, curves, or surfaces using application-specific calculations. They can be created interactively through I-Inspect or directly from Python scripts, with tolerances for evaluating the results.
* [Custom sequences](../howtos/custom_elements/custom_sequences.md) combine regular element creation commands into one coordinated, editable unit. The new guide explains how to keep the sequence configuration synchronized when users edit its child elements.

The expanded collection of <a href="../python_examples/examples_overview.html#custom-elements-how-to-create-custom-elements">custom element example Apps</a> provides practical starting points for development. Examples cover nominal and actual geometry, inspections, and sequences.

Start with the linked how-to guides for the concepts and implementation workflow. For class definitions and detailed requirements, see the <a href="../python_api/python_api.html#gom-api-extensions">Extensions API reference</a>.
