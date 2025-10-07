# Implementation Plan

- [x] 1. Update admin add student form template
  - Add PhD option to the branch dropdown in `templates/add_student.html` (line 95-98)
  - Position PhD option first in academic hierarchy order (PhD, MCA, BCA)
  - Use format "PhD (Doctor of Philosophy)" to match existing descriptive style
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3_

- [x] 2. Update student self-registration form template
  - Add PhD option to the branch dropdown in `templates/student_self_register.html` (line 185-188)
  - Ensure PhD option matches the same format and positioning as admin form
  - Maintain consistent styling and functionality with existing options
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3_

- [x] 3. Update Excel export statistics calculation
  - Add PhD count calculation in the `/export-excel` route in `app.py` (around line 405)
  - Include PhD count in summary statistics alongside existing MCA and BCA counts
  - Add PhD count row to the summary_data list in the Summary worksheet
  - _Requirements: 3.1, 3.2, 3.3_