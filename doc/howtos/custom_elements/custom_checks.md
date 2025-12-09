![New in Version 2026](https://img.shields.io/badge/New-Version_2026-red)

# Custom checks

Custom checks always refer to a geometric target element, in most cases an actual element. Therefore the name of a check (or inspection) element is typically composed of the target element's name and an abbreviation indicating the check's purpose. For example, a radius check on the circle element 'Circle 1' could be named 'Circle1.R'

Checks can be applied to

* Scalar element properties &ndash; e.g. a circle's radius
* Curves &ndash; e.g. deviation of a section curve's points in z-direction
* Surfaces &ndash; e.g. deviation of a surface curve's points in z-direction

The check element computes the deviation between the reference element's actual value(s) and its nominal value(s). The deviation value(s) can have a dimension (e.g. length).

## Dialog definition

The dialog must contain

* A <a href="../user_defined_dialogs/dialog_widgets.html#selection-element-widget">Selection element widget</a> to select the target element

* An <a href="../user_defined_dialogs/dialog_widgets.html#element-name-widget">Element name widget</a> to set the custom check's element name

```{caution}
The element name widget object must be set to `name` in the Dialog Editor.
```

The dialog can optionally provide

* A <a href="../user_defined_dialogs/dialog_widgets.html#unit-widget">Unit widget</a> to set the deviation value's dimension

* A <a href="../user_defined_dialogs/dialog_widgets.html#tolerances-widget">Tolerances widget</a> for evaluating the deviation value(s)

```{caution}
The tolerances widget's name must be set to `tolerance` in the Dialog Editor.
```

### Custom check Python script

All custom elements are based on the <a href="../../python_api/python_api.html#gom-api-extensions">Extensions API</a>. More specifically, a custom check class is inherited from the <a href="../../python_api/python_api.html#gom-api-extensions-inspections">ScriptedInspection</a> base class.

```{code-block} python
:caption: Custom_Scalar_Check.py &ndash; Minimal example &ndash; Scripted scalar check
:linenos:

import gom
import gom.api.scripted_checks_util
import gom.api.extensions.inspections

from gom import apicontribution

@apicontribution
class MinimalScalarCheck (gom.api.extensions.inspections.Scalar):

    def __init__ (self):
        super ().__init__ (
            id='examples.custom_scalar_check',
            description='Custom Scalar Check',
            dimension='length',
            abbreviation='ScrSca'
        )

    def dialog (self, context, args):
        dlg = gom.api.dialog.create (context, '/Custom_Scalar_Check.gdlg')
        # -------------------------------------------------------------------------
        dlg.slct_element.filter = gom.api.scripted_checks_util.is_scalar_checkable
        # -------------------------------------------------------------------------
        self.initialize_dialog(context, dlg, args)

        # Provide dialog handle in event()
        self.dlg = dlg

        return self.apply_dialog(dlg, gom.api.dialog.show(context, dlg))

    def event(self, context, event_type, parameters):
        """
        Set Custom check's name: <target_element>.<abbreviation>
        """
        if event_type == 'dialog::initialized' or event_type == 'dialog::changed':
            if parameters['values']['slct_element'] is not None:
                self.dlg.name.value = self.dlg.slct_element.value.name + '.' + 'ScrSca'
                return True

        return False

    def compute (self, context, values):
        # ----------------------------------------------------
        # --- insert your calculation  here ------------------
        # ----------------------------------------------------
        actual_result = 1.0
        nominal_result = 2.0
        # ----------------------------------------------------
        return {
            "nominal": nominal_result,
            "actual":  actual_result,
            "target_element": values['slct_element'],
            "unit": values['unit']
        }

gom.run_api ()
```

line 2..5:
: Import custom check specific packages.

line 7..8:
: The class `MinimalScalarCheck` is inherited from [gom.api.extensions.inspections.Scalar](../../python_api/python_api.md#gomapiextensionsinspectionsscalar). The decorator `@apicontribution` allows to register the class `MinimalScalarCheck` in the ZEISS INSPECT framework.

line 10..16:
: The constructor calls the super class constructor while defining unique contribution ID, (human readable) description, dimension and abbreviation.

line 18..28:
: The `dialog()` method applies an element filter (see <a href="../../howtos/user_defined_dialogs/dialog_widgets.html#selection-element-widget">Selection element widget</a>) and to copies the dialog handle to the member `dlg` for using in `event()`.

line 30..39:
: The `event()` method sets the custom check's element name

line 41..53:
: The `compute()` method uses constant actual and nominal values for demonstration purposes.

line 55:
: `gom.run_api()` is executed when the script is started as a service.

## References

* [Extensions API &ndash; Inspections](../../python_api/python_api.md#gomapiextensionsinspections)
* [Extensions API &ndash; Scalar Inspections](../../python_api/python_api.md#gomapiextensionsinspectionsscalar)
* [Extensions API &ndash; Curve Inspections](../../python_api/python_api.md#gomapiextensionsinspectionscurve)
* [Extensions API &ndash; Surface Inspections](../../python_api/python_api.md#gomapiextensionsinspectionssurface)
