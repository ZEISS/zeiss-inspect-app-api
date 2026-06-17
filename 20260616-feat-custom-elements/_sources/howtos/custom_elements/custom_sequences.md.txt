![New in Version 2027](https://img.shields.io/badge/New-Version_2027-20B2AA)

# Custom sequence elements

Custom sequence elements group multiple regular ZEISS INSPECT creation commands into one coordinated unit. In contrast to custom actuals and custom nominals, a sequence does not compute geometry itself. Instead, it creates and manages a set of standard elements and keeps them synchronized through the sequence lifecycle.

```{note}
This How-to focuses on implementation flow, editing behavior, naming, and troubleshooting. For full constructor signatures, return schemas, and API semantics, refer to <a href="../../python_api/python_api.html#gom-api-extensions-sequence">Extensions API &ndash; Custom Sequence Elements</a>.
```

The upcoming custom sequence example app will be linked here once it is published. Until then, the API reference and the example app documentation are the primary sources for concrete implementation details.

## When to use a custom sequence

Use a custom sequence when a feature is best represented as a coordinated set of elements rather than a single computed result. Typical cases include:

* A leading element with one or more child elements
* Editable sub-elements that should stay logically grouped
* Derived constructions where the leading element depends on child elements
* Workflows that need coordinated re-editing of multiple regular elements

If the feature only computes one geometric result, a custom nominal or actual element is usually the better fit.

## Core lifecycle

The sequence lifecycle is different from the lifecycle of custom actuals or nominals:

1. **Dialog** - The user enters the sequence parameters in a custom dialog. The dialog framework is provided by <a href="../../python_api/python_api.html#gom-api-extensions-customelement">Extensions API &ndash; Custom Element</a>.
2. **Create** - The sequence creates the regular elements that belong to it and returns them in creation order. See <a href="../../python_api/python_api.html#gom-api-extensions-sequence-customsequence-create">Extensions API &ndash; CustomSequence.create</a>.
3. **Edit** - Re-opening the leading element updates the existing sequence elements. See <a href="../../python_api/python_api.html#gom-api-extensions-sequence-customsequence-edit">Extensions API &ndash; CustomSequence.edit</a>.
4. **Child edit** - If child editing is enabled, direct edits to child elements are reflected back into the sequence arguments. See <a href="../../python_api/python_api.html#gom-api-extensions-sequence-customsequence-on-edited">Extensions API &ndash; CustomSequence.on_edited</a>.

The API documentation describes the full method contracts. This How-to should be read as a usage guide for the implementation flow.

## Design guidance

### Keep the leading element as the sequence representative

The leading element is the entry point for the sequence. It should represent the whole construction and be the element that users edit when they want to reconfigure the sequence as a unit.

### Use child elements for the editable building blocks

Create child elements for the parts that users may want to adjust independently. Use `edit_child_elements_separately` when the child elements should remain individually editable.

### Keep element order stable

The order returned by `create()` matters. It must be the same order used later by `edit()` and `on_edited()`.

This is the main contract to remember:

* `create()` returns all elements in creation order
* `edit()` receives the current elements in the same order
* `on_edited()` receives the updated child parameters in the same order

### Generate clear child names

Child elements should be named so that they are clearly associated with the leading element. Use `generate_element_name()` for that purpose.

### Validate geometry early

If the sequence depends on a geometric condition, validate it in the dialog event handler before creation succeeds. This prevents invalid or ambiguous constructions from reaching the project.

## Typical implementation checkpoints

### Dialog

The dialog should collect the parameters that define the sequence and provide an element name widget for the leading element.

### Create

The create step should:

* Create the child elements first
* Create the leading element last
* Return both the full element list and the leading element

### Edit

The edit step should update existing elements, not create new ones. It should use the current arguments and the stored element order to reapply the sequence configuration.

### On edited

The child-edit callback should translate child edits back into the sequence arguments. That keeps the dialog state consistent if the user later reopens the whole sequence.

## Service definition

Define the sequence service in the App's `metainfo.json` file, just like other custom elements.

Key points:

* Use a unique and stable service endpoint
* Point the service to the sequence script in `scripts/`
* Keep the endpoint stable after release
* Ensure the script calls `gom.run_api()`

For the general service structure and startup troubleshooting, see [Custom nominal/actual elements](custom_nominals_actuals.md#service-definition) and [Troubleshooting](custom_nominals_actuals.md#troubleshooting).

## Troubleshooting

The most common sequence issues are implementation-order problems rather than API problems:

* The element order returned by `create()` does not match the order expected by `edit()` or `on_edited()`
* The dialog accepts invalid geometry because validation is too late or incomplete
* Child edits are not copied back into the sequence arguments
* Names collide when the same sequence is created multiple times
* The service does not start because the script is not registered or does not call `gom.run_api()`

If a child element is meant to stay editable on its own, make sure `edit_child_elements_separately` is enabled and that the sequence handles direct child edits correctly.

## References

* <a href="../../python_api/python_api.html#gom-api-extensions-sequence">Extensions API &ndash; Custom Sequence Elements</a>
* [Custom nominal/actual elements](custom_nominals_actuals.md)
* Published example app link to be added after release