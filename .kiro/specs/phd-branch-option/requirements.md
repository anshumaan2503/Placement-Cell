# Requirements Document

## Introduction

This feature adds PhD (Doctor of Philosophy) as a selectable branch option in the "Add Student" functionality of the placement cell management system. Currently, the system only supports MCA and BCA programs, but the university also offers PhD programs whose graduates may be placed in industry positions. This enhancement will allow administrators to record placement information for PhD students alongside existing undergraduate and master's degree programs.

## Requirements

### Requirement 1

**User Story:** As an admin user, I want to select PhD as a branch option when adding a placed student, so that I can record placement information for doctoral graduates.

#### Acceptance Criteria

1. WHEN the admin opens the "Add Student" form THEN the system SHALL display PhD as an option in the branch dropdown
2. WHEN the admin selects PhD from the branch dropdown THEN the system SHALL accept this selection as valid
3. WHEN the admin submits the form with PhD selected THEN the system SHALL save the student record with PhD as the branch

### Requirement 2

**User Story:** As an admin user, I want the PhD option to be clearly labeled and positioned appropriately in the branch dropdown, so that it follows a logical academic progression order.

#### Acceptance Criteria

1. WHEN the branch dropdown is displayed THEN the system SHALL show options in the order: PhD, MCA, BCA
2. WHEN the PhD option is displayed THEN the system SHALL show the full descriptive text "PhD (Doctor of Philosophy)"
3. WHEN viewing the dropdown THEN the system SHALL maintain consistent formatting with existing options

### Requirement 3

**User Story:** As an admin user, I want PhD student records to be stored and displayed consistently with other student records, so that all placement data is managed uniformly.

#### Acceptance Criteria

1. WHEN a PhD student record is saved THEN the system SHALL store the branch value as "PhD" in the database
2. WHEN PhD student records are displayed in lists or reports THEN the system SHALL show "PhD" as the branch
3. WHEN filtering or searching student records THEN the system SHALL include PhD students in relevant queries