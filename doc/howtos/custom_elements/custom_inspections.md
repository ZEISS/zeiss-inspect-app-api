![New in Version 2027](https://img.shields.io/badge/New-Version_2027-20B2AA)

# Custom inspections

Custom inspections always refer to a geometric target element, in most cases an actual element. Therefore the name of an inspection element is typically composed of the target element's name and an abbreviation indicating the inspection purpose. For example, a radius inspection on the circle element 'Circle 1' could be named 'Circle1.R'.

```{note}
In this How-to, the preferred prose term is "inspection". In the API, the current technical class family is `CustomInspection`. `ScriptedInspection` is documented as a legacy alias.
```

Inspections can be applied to

* Scalar element properties &ndash; e.g. a circle's radius
* Curves &ndash; e.g. deviation of a section curve's points in z-direction
* Surfaces &ndash; e.g. deviation of a surface curve's points in z-direction

The inspection element computes the deviation between the reference element's actual value(s) and its nominal value(s). The deviation value(s) can have a dimension (e.g. length).

## Dialog definition

The dialog must contain

* A <a href="../user_defined_dialogs/dialog_widgets.html#selection-element-widget">Selection element widget</a> to select the target element

* An <a href="../user_defined_dialogs/dialog_widgets.html#element-name-widget">Element name widget</a> to set the custom inspection's element name

```{caution}
The element name widget object must be set to `name` in the Dialog Editor.
```

The dialog can optionally provide

* A <a href="../user_defined_dialogs/dialog_widgets.html#unit-widget">Unit widget</a> to set the deviation value's dimension

* A <a href="../user_defined_dialogs/dialog_widgets.html#tolerances-widget">Tolerances widget</a> for evaluating the deviation value(s)

```{caution}
The tolerances widget's name must be set to `tolerance` in the Dialog Editor.
```

Both object names &ndash; `name` and `tolerance` &ndash; are reserved and case-sensitive.

### Custom inspection Python script

All custom elements are based on the <a href="../../python_api/python_api.html#gom-api-extensions">Extensions API</a>. More specifically, a custom inspection class is inherited from the <a href="../../python_api/python_api.html#gom-api-extensions-inspections">CustomInspection</a> base class.

Use this How-to for implementation flow and practical patterns. For complete constructor and return-value specifications, refer to the inspections class references in the API documentation.

```{code-block} python
:caption: Custom_Scalar_Check.py &ndash; Minimal example &ndash; Custom scalar inspection
:linenos:

import gom
import gom.api.custom_checks_util
import gom.api.extensions.inspections

from gom import apicontribution

@apicontribution
class MinimalScalarInspection (gom.api.extensions.inspections.Scalar):

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
        dlg.slct_element.filter = gom.api.custom_checks_util.is_scalar_checkable
        # -------------------------------------------------------------------------
        self.initialize_dialog(context, dlg, args)

        # Provide dialog handle in event()
        self.dlg = dlg

        return self.apply_dialog(dlg, gom.api.dialog.show(context, dlg))

    def event(self, context, event_type, parameters):
        """
        Set custom inspection name: <target_element>.<abbreviation>
        """
        if event_type == 'dialog::initialized' or event_type == 'dialog::changed':
            if parameters['values']['slct_element'] is not None:
                self.dlg.name.value = self.dlg.slct_element.value.name + '.' + 'ScrSca'
                return True

        return False

    def compute (self, context, values):
        # ----------------------------------------------------
        # --- insert your computation here -------------------
        # ----------------------------------------------------
        ACTUAL_RESULT = 1.0
        NOMINAL_RESULT = 2.0
        # ----------------------------------------------------
        return {
            "nominal": NOMINAL_RESULT,
            "actual":  ACTUAL_RESULT,
            "target_element": values['slct_element'],
            "unit": values['unit']
        }

gom.run_api ()
```

line 2..5:
: Import custom inspection specific packages.

line 7..8:
: The class `MinimalScalarInspection` is inherited from [gom.api.extensions.inspections.Scalar](../../python_api/python_api.md#gomapiextensionsinspectionsscalar). The decorator `@apicontribution` allows to register the class `MinimalScalarInspection` in the ZEISS INSPECT framework.

line 10..16:
: The constructor calls the super class constructor while defining unique contribution ID, human-readable description, dimension and abbreviation. See the API reference for full signature details.

line 18..28:
: The `dialog()` method applies an element filter (see <a href="../../howtos/user_defined_dialogs/dialog_widgets.html#selection-element-widget">Selection element widget</a>) and copies the dialog handle to the member `dlg` for usage in `event()`.

line 30..39:
: The `event()` method sets the custom inspection element name.

line 41..53:
: The `compute()` method uses constant actual and nominal values for demonstration purposes. The exact required result schema depends on the inspection type and is defined in the API reference.

line 55:
: `gom.run_api()` is executed when the script is started as a service.

### Service definition and troubleshooting

For service definition details and troubleshooting guidance (including service startup issues), refer to the corresponding sections in [Custom nominal/actual elements](custom_nominals_actuals.md#service-definition):

* [Service definition](custom_nominals_actuals.md#service-definition)
* [Troubleshooting](custom_nominals_actuals.md#troubleshooting)

### Applying tolerances

To apply tolerances to a custom inspection, forward the tolerance value from the dialog result in `apply_dialog()`.

```{code-block} python
:caption: Forwarding tolerance values in apply_dialog()
:linenos:

def apply_dialog(self, dlg, result):
    params = super().apply_dialog(dlg, result)
    params['name'] = result['name']
    params['tolerance'] = result['tolerance']
    return params
```

The framework consumes `name` and `tolerance` automatically. The `values` dictionary is still forwarded unchanged to `compute()`.

## References

* [Extensions API &ndash; Inspections](../../python_api/python_api.md#gomapiextensionsinspections)
* [Extensions API &ndash; Scalar Inspections](../../python_api/python_api.md#gomapiextensionsinspectionsscalar)
* [Extensions API &ndash; Curve Inspections](../../python_api/python_api.md#gomapiextensionsinspectionscurve)
* [Extensions API &ndash; Surface Inspections](../../python_api/python_api.md#gomapiextensionsinspectionssurface)