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

: Wizard step with alternative next-button text
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

## Related

* [Dialog widgets &ndash; Wizard widget](dialog_widgets.md#wizard-widget)
% Workflow Assistant