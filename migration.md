# Migration Guide: medic/pyxform Update

This document outlines the changes made to update the medic/pyxform fork to match the latest XLSForm/pyxform while preserving CHT-specific functionality.

## Overview

The Community Health Toolkit (CHT) uses ODK forms to capture input data from users for various configurable workflows. Pyxform is used to transform ODK form configurations from the .xlsx format into the .xml configuration interpreted by the CHT server. The current implementation uses a forked version of pyxform (medic/pyxform) that has fallen behind the original repository (XLSForm/pyxform) and is missing many fixes and improvements.

This project aims to update the medic/pyxform codebase to incorporate the latest features from XLSForm/pyxform while maintaining backward compatibility with CHT-specific customizations.

## Phase 1: Core Implementation (Current PR)

This PR focuses on the most critical feature identified in the issue description: **deterministic ordering of XML attributes**. It also verifies that key CHT-specific customizations are preserved.

### 1. Deterministic Ordering of XML Attributes

**Problem Addressed:**
Currently, regenerating a form XML that has not changed can still result in significant diffs since the ordering of attributes in the XML elements is not deterministic and their order can change (even if the content of the xlsx file stayed the same).

**What Changed:**

- Modified the `node()` function in `utils.py` to use `sorted(kwargs.items())` instead of the default iteration:

  ```python
  # Before:
  for k, v in kwargs.items():
      # ...

  # After:
  for k, v in sorted(kwargs.items()):
      # ...
  ```

- This ensures that XML attributes are consistently ordered alphabetically, regardless of the order they appear in the code
- Added comments to explain the importance of deterministic ordering:

  ```python
  # Sort the attributes to guarantee a consistent order across Python versions.
  # This is crucial for deterministic XML generation.
  ```

**Benefits:**

- More predictable and consistent XML generation
- Easier version control and diff comparison
- Reduced noise in form updates
- Simplified testing and validation of forms

**Implementation Details:**

- The change is implemented in `pyxform/utils.py` in the `node()` function
- Added a test file `tests/test_deterministic_ordering.py` to verify consistent attribute ordering
- The test creates nodes with identical attributes in different orders and verifies the resulting XML is identical

**Code Change:**

```python
# Before:
for k, v in kwargs.items():
    # ...

# After:
for k, v in sorted(kwargs.items()):
    # ...
```

### 2. Custom Question Types (Verification)

**What's Verified:**

- All CHT-specific question types are maintained:
  - `db:person`
  - `db:clinic`
  - `db:health_center`
  - `db:district_hospital`
  - `tel`

**Implementation Details:**

- These custom types are defined in `pyxform/question_type_dictionary.py`
- Added a test file `tests/test_custom_question_types.py` to verify these types work correctly
- The test creates form elements with each custom type and verifies they are properly represented in the generated XML

### 3. Meta Section Handling (Verification)

**What's Verified:**

- Special handling for meta sections with `tag="hidden"` attribute
- This ensures proper display and processing of meta sections in CHT applications

**Implementation Details:**

- This functionality is implemented in `pyxform/section.py`
- Added a test file `tests/test_meta_section.py` to verify meta sections have the `tag="hidden"` attribute
- The test creates a survey with a meta section and verifies the generated XML includes the tag="hidden" attribute

## Phase 3: CHT-Specific Customizations

This phase implements the remaining CHT-specific customizations that are essential for backward compatibility.

### 1. Instance Tag Values Copying

**Problem Addressed:**
In the original pyxform, tag attributes were filtered out if they matched the element's tag name, which prevented instance tag values from being properly copied.

**What Changed:**

- Modified the tag attribute handling in `utils.py` to allow tag attributes to pass through except when the tag attribute matches the element's tag name:

  ```python
  # Before:
  if k in blocked_attributes:
      continue

  # After:
  if k == 'tag' and v == tag:
      continue
  ```

**Benefits:**

- Ensures that instance tag values are properly copied in the generated XML
- Maintains backward compatibility with existing CHT forms
- Allows for more flexible form design

**Implementation Details:**

- The change is implemented in `pyxform/utils.py`
- Added a test file `tests/test_instance_tag_values.py` to verify instance tag values are properly copied
- The test creates elements with tag attributes and verifies they appear in the generated XML

### 2. Language Tag Format

**Problem Addressed:**
The standard pyxform uses a complex format for language tags (e.g., `label::/data/label:en`), while CHT uses a simplified format (e.g., `label::en`).

**What Changed:**

- Added a configuration option in `constants.py` for language tag format:

  ```python
  # CHT-specific constants
  CHT_SIMPLIFIED_LANGUAGE_FORMAT = True  # Use label::en instead of label::/data/label:en
  ```

- Modified the `_translation_path` method in `survey_element.py` to support the simplified format:

  ```python
  def _translation_path(self, display_element):
      from pyxform.constants import CHT_SIMPLIFIED_LANGUAGE_FORMAT

      if CHT_SIMPLIFIED_LANGUAGE_FORMAT:
          # Use simplified format: label::en instead of label::/data/label:en
          return display_element
      else:
          # Use standard format: label::/data/label:en
          return self.get_xpath() + ":" + display_element
  ```

**Benefits:**

- Maintains backward compatibility with existing CHT forms
- Simplifies the language tag format for easier reading and debugging
- Reduces the size of the generated XML

**Implementation Details:**

- Added the configuration option in `pyxform/constants.py`
- Modified the `_translation_path` method in `pyxform/survey_element.py`
- Added a test file `tests/test_language_tag_format.py` to verify the simplified format is used

### 3. Empty Label Handling

**Problem Addressed:**
The standard pyxform raises an error for empty labels, while CHT needs to support them for certain form designs.

**What Changed:**

- Modified the `xml_label_and_hint` method in `survey_element.py` to handle empty labels:

  ```python
  # Before:
  if self.label or self.media:
      result.append(self.xml_label())
      label_appended = True

  # After:
  # Handle empty label case for CHT compatibility
  if self.label == "" or self.label or self.media:
      result.append(self.xml_label())
      label_appended = True
  ```

**Benefits:**

- Allows forms with empty labels to be processed without errors
- Maintains backward compatibility with existing CHT forms
- Provides more flexibility in form design

**Implementation Details:**

- Modified the `xml_label_and_hint` method in `pyxform/survey_element.py`
- Added a test file `tests/test_empty_label.py` to verify empty labels are handled correctly

## Migration Notes

### For Form Developers

- No changes are needed for existing forms
- The deterministic ordering of XML attributes is transparent to form developers
- All CHT-specific question types continue to work as before

### For Application Developers

- The updated pyxform should be a drop-in replacement for the current version
- No changes to application code should be needed
- The deterministic ordering of XML attributes may affect how diffs appear in version control, but in a positive way (more consistent)

## Testing

The following tests have been added to verify the implemented features:

### Phase 1 Tests:

1. `tests/test_deterministic_ordering.py` - Verifies consistent attribute ordering
2. `tests/test_custom_question_types.py` - Verifies CHT-specific question types
3. `tests/test_meta_section.py` - Verifies meta section handling

### Phase 3 Tests:

4. `tests/test_instance_tag_values.py` - Verifies instance tag values are properly copied
5. `tests/test_language_tag_format.py` - Verifies simplified language tag format is used
6. `tests/test_empty_label.py` - Verifies empty labels are handled correctly

To run the tests:

```bash
python -m unittest discover
```

To run specific tests:

```bash
python -m unittest tests/test_deterministic_ordering.py
python -m unittest tests/test_instance_tag_values.py
```

## Known Issues

- Some tests may fail due to ODK Validate issues
- These failures are not related to the implemented features and will be addressed in future PRs

## Relationship to Original Issue

This PR addresses the most important change identified in the original issue:

> DETERMINISTIC ORDERING OF XML ATTRIBUTES
> This is the most important change as currently, regenerating a form xml that has not changed can still result in a significant diff since the ordering of attributes in the xml elements is not deterministic and their order can change (even if the content of the xlsx file stayed the same).

By implementing deterministic ordering of XML attributes, we ensure that regenerating a form XML that has not changed will not result in significant diffs, making version control and form management much easier.
