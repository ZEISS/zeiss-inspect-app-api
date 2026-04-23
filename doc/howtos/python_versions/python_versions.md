![New in Version 2027](https://img.shields.io/badge/New-Version_2026-yellow)

# Adding and using specific Python versions

## Available Python interpreter versions

See ZEISS INSPECT's preferences (Edit ► Preferences... &ndash; Apps / Python installation) for available Python interpreters.

You can add Python interpreters by adding the path to an existing Python installation on your computer or by installation from an App.

## Using a specific Python version in an App

To select a specific Python version (instead of the default) in an App &ndash; in the App's properties:
* Go to "Further properties"
* Add "Python version"
* Provide the desired Python version specification , e.g. "3.12.x". [npm semantic versioning syntax](https://docs.npmjs.com/about-semantic-versioning) is supported.

```{note}
Alternatively, you can add the Python version specification directly to `metainfo.json`: `"python-version": "3.12.x"`
``` 

```{caution}
"Protected Apps" can only be used with Python interpreters approved by ZEISS (Preferences &ndash; Apps / Python installation &ndash; Python interpreter: "System").
```

## Providing a custom Python interpreter as an App

```{important}
The Python distribution must have the package `websocket-client` installed!
```

1. Download "Python install manager" from [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Download the desired Python version

   Example:
   ```powershell
   pymanager install 3.12.7-64 --target .\python-dist
   ```

3. Install `websocket-client` into the Python directory (mandatory)

   ```powershell
   .\python-dist\python.exe -m pip install websocket-client
   ```

4. Install additional Python packages (optional) 

   See step 3.

5. Create a ZIP archive (replace the archive name as needed)
   ```powershell
   Compress-Archive -Path .\python-dist\* -DestinationPath .\python-3.12.7-64.zip -Force
   ```

6. Create a new App (e.g. 'Python 3.12.7')

7. Find the App's uuid in its `metainfo.json`

8. Go to the App's directory in `%APPDATA%\gom\2027\gom_edited_addons\<uuid>`

9. In the App's directory, copy the Python archive into a `python\<python_version>\` directory

   Example:
   ```
   gom_edited_addons\<uuid>\
     |
     |-- python
           |
           |-- Python312
                 |
                 |-- python-3.12.7-64.zip
   ```

10. Click the 'Refresh' button in the App Editor

    The new Python interpreter is now unpacked into `%APPDATA%\gom\2027\gom_python_interpreters\<uuid>` (same uuid as the App which provided the Python archive).

You can finalize and export your Python interpreter App as usual.

## Creating a Software Bill of Materials (SBOM)

```{note}
An SBOM is a structured list of the software components included in a package, including third-party and transitive dependencies. Its purpose is to make the contents of the package transparent so vendors, customers, and security teams know exactly what was shipped.
```

A CycloneDX SBOM for the custom Python interpreter App consists of two parts:

* The **packages BOM**: lists all pip-installed packages and their licenses.
* The **Python distribution BOM**: describes the CPython runtime itself.

Both are merged into a single file using `cyclonedx-cli`.

```{important}
Do not install `cyclonedx-bom` into the Python distribution archive that you want to ship.
Otherwise the BOM will also contain `cyclonedx-bom` and its dependencies, even though these packages are not part of the final archive.
```

### 1. Install `cyclonedx-bom` outside the portable Python directory

Install `cyclonedx-bom` into a separate helper Python installation, for example your regular local Python installation:

```powershell
python -m pip install cyclonedx-bom
```

You can also use any other Python installation that is not part of the shipped archive.

### 2. Generate the packages BOM for the target interpreter

Run `cyclonedx-py` from the helper installation and point it to the Python interpreter inside the portable distribution:

```powershell
cyclonedx-py environment .\python-dist\python.exe --output-format JSON -o packages-bom.json
```

This creates `packages-bom.json` listing all installed packages with their names, versions, licenses, and package URLs (PURLs).

### 3. Obtain the Python distribution BOM

The Python Software Foundation provides SPDX SBOM files for CPython releases. Download the BOM for your Python version from `https://www.python.org/ftp/python/<version>/`.

Example for 3.12.7: [https://www.python.org/ftp/python/3.12.7/](https://www.python.org/ftp/python/3.12.7/)


Look for a file named `python-<version>-amd64.spdx.json` or similar. These files are SPDX JSON and must be converted to CycloneDX JSON before merging with the packages BOM.

### 4. Convert the Python distribution BOM to CycloneDX

Download the `cyclonedx-win-x64.exe` standalone binary from [https://github.com/CycloneDX/cyclonedx-cli/releases](https://github.com/CycloneDX/cyclonedx-cli/releases).

Then convert the Python distribution SPDX BOM to CycloneDX JSON:

```powershell
./cyclonedx-win-x64.exe convert `
   --input-file .\python-3.12.7-amd64.exe.spdx.json `
   --input-format spdxjson `
   --output-file .\python-3.12.7-amd64.cdx.json `
   --output-format json
```

If no SBOM is available for the specific release, you can create a minimal CycloneDX component entry manually:

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "version": 1,
  "components": [
    {
      "type": "application",
      "name": "CPython",
      "version": "3.12.7",
      "licenses": [{ "license": { "id": "PSF-2.0" } }],
      "purl": "pkg:generic/python@3.12.7"
    }
  ]
}
```

Save this as `python-dist-bom.json`.

### 5. Merge the BOMs

Then merge both BOM files into one:

```powershell
.\cyclonedx-win-x64.exe merge `
   --input-files .\python-3.12.7-amd64.cdx.json packages-bom.json `
    --output-format json `
    --output-file python-3.12.7-64-sbom.json
```

The resulting `python-3.12.7-64-sbom.json` covers both the Python runtime and all installed packages.

## See also

* [Where are Apps located in the file system?](../faq/faq.md#where-are-apps-located-in-the-file-system)
* [CycloneDX Python (`cyclonedx-bom`)](https://github.com/CycloneDX/cyclonedx-python)
* [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli)
