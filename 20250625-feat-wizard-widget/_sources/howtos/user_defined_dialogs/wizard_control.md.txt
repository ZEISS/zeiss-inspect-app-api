# Wizard widget control

> Abstract: Enabling completion of a wizard step has been shown as a fundamental feature in [Dialog widgets &ndash; Wizard widget](dialog_widgets.md#wizard-widget). More functions for controlling the presentation and sequence of wizard steps are introduced in this section.

## Step complete

```{figure} assets/wizard_step1_complete_false.png
:class: bordered-figure

Step complete: False
```

```{figure} assets/wizard_step1_complete_true.png
:class: bordered-figure

Step complete: True
```

`DIALOG.wizard.step_set_complete(step_id, condition)`
: Enable completion of step `step_id`.

## Step optional

```{figure} assets/wizard_step2_optional.png
:class: bordered-figure

Step optional, complete: False
```

```{figure} assets/wizard_step2_complete.png
:class: bordered-figure

Step optional, complete: True
```

`DIALOG.wizard.step_set_optional(step_id, condition)`
: Set step `step_id` as optional.

## Skip button separate

```{figure} assets/wizard_step2_skip_button_separate.png
:class: bordered-figure

Separate skip-button
```

`DIALOG.wizard.step_set_skip_button_separate(step_id, condition)`
: Enable a separate skip-button in addition to the next-button.

## Next step

```{figure} assets/wizard_step3_next_id.png
:class: bordered-figure

Set ID of next step
```

`DIALOG.wizard.step_set_next_id(step_id, next_id)`
: Set ID of next step &ndash; allows out-of sequence execution of steps.

## Branch

```{figure} assets/wizard_step5_branch.png
:class: bordered-figure

Wizard step with a branch-button
```

`DIALOG.wizard.step_set_branch_button_visible(step_id, condition)`
: Enable the branch-button.

`DIALOG.wizard.step_set_branch_button_text(step_id, text)`
: Set the branch-button text to `text` (e.g. "Branch"). 

`DIALOG.wizard.step_set_branch_id(step_id, branch_step_id)`
: Set the branch target step ID.

## Next button text

```{figure} assets/wizard_step6_next_button_text.png
:class: bordered-figure

Wizard step with alternative next-button text
```

`DIALOG.wizard.step_set_next_button_text(step_id, text)`
: Set text of the next-button.

## Final step

```{figure} assets/wizard_step7_finish.png
:class: bordered-figure

Step with finish-button
```

`DIALOG.wizard.step_set_final(step_id, condition)`
: Set step `step_id` to a final step with finish-button. By default, the last step in the list is the final step.

## Wizard events

```{note}
A dedicated event handler function for the Wizard widget is recommended.
```

The argument of the Wizard widget event is a dict with the following keys:

`widget`
: The wizard widget

`step`
: Current wizard step

`type`
: Event type

  * `"initialized"` &ndash; A new step has been reached.

    Do setup for the new wizard step here, e.g. change the selection.

  * `"discarded"` &ndash; The current step has been discarded, either by the user navigating to the previous step or aborting the whole dialog. In the latter case a `"discarded"` event for all previously completed steps will be emitted in reversed order.
  
    Do cleanup here, e.g., delete temporary elements or restore some selection.

  * `"committed"`&ndash; The current step has been committed by the user.

    Finalize actions relevant to the step, e.g., create some (intermediate) element based on the current Dialog parameters.

  * `"skipped"` &ndash; The current step has skipped by the user.

    This can also be used to clean up, which may or may not be the same as for the discarded event.

  * `"branched"` &ndash; The user has pressed the branch button.

    This may be the same as the committed event, but it may also trigger a different action especially if there is no branch ID set.

  * `"id_changed"` &ndash; This is a general event when a the wizard step changes.
  
    This can be reacted to in place of the more detailed events above, e.g., if only the current id is needed to adjust your workflow.

## Related

* [Dialog widgets &ndash; Wizard widget](dialog_widgets.md#wizard-widget)
% Workflow Assistant