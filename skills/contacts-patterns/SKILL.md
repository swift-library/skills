---
name: contacts-patterns
description: Use this skill for Contacts and ContactsUI implementation and review across CNContactStore authorization, limited contact access, ContactAccessButton, CNContactPickerViewController, contact fetching, key descriptors, CNContact/CNMutableContact, CNSaveRequest, groups, containers, vCard import/export, change history, contact notes entitlement boundaries, and SwiftUI picker wrappers. Do not use for generic address-book data models, interface copy only, account sync backends, or privacy text with no Contacts framework behavior.
---

# Contacts Patterns

## Purpose

Guide implementation, review, and troubleshooting for Contacts and ContactsUI
features that read, write, select, display, or synchronize a person's contacts
inside Apple-platform apps.

## When To Use

- Requesting or reviewing `CNContactStore` access and contact authorization.
- Handling limited contact access, `ContactAccessButton`, or contact access
  pickers.
- Selecting contacts with `CNContactPickerViewController`, `CNContactPicker`,
  or SwiftUI wrappers.
- Fetching, filtering, creating, updating, deleting, grouping, or exporting
  contacts.
- Working with key descriptors, partial-contact failures, vCards, change
  history, notes entitlement boundaries, or contact database change handling.

## When Not To Use

- Do not use for generic person/address models that do not touch Contacts.
- Do not use for privacy or permission copy only.
- Do not use for account sync backend design unless Contacts framework behavior
  is in scope.
- Do not use for Keychain credential storage, authentication, or payment
  contacts.
- Do not invent limited-access behavior, notes entitlement behavior, or picker
  platform behavior. Verify current Apple documentation and local SDK symbols.

## Inputs To Inspect

- `Info.plist` usage strings, entitlements, and target capabilities.
- `CNContactStore` authorization, fetch, enumerate, save, group, container, and
  change-history code.
- `CNContactPickerViewController`, `CNContactViewController`, SwiftUI wrappers,
  delegates, and selected-contact state.
- Key descriptors, predicates, partial-contact handling, vCard import/export,
  and notes-field access.
- Tests, sample contacts, simulator/device permission state, and data-migration
  behavior.

## Workflow

1. Identify whether the feature needs full contact-store access, limited access,
   picker-only selection, mutation, or change tracking.
2. Prefer picker-based access when the app only needs a user-selected contact.
3. Request store authorization only when the app must read or write contacts
   beyond picker selection.
4. Fetch only the keys the feature needs, and handle partial-contact failures
   by refetching with explicit descriptors.
5. Perform create/update/delete through `CNSaveRequest` with predictable error
   handling and no main-thread database work.
6. Keep contact identifiers, groups, containers, vCards, and history tokens
   explicit when persistence or sync is involved.
7. Validate denied, limited, picker-only, changed-permission, and missing-field
   states.

## Review Rules

- Do not request broad contact access for one-time selection.
- Do not assume picker selection grants persistent full-store access.
- Do not fetch all contacts or all keys when a predicate or key descriptor can
  narrow the work.
- Do not read or write contact notes without the required entitlement and a
  current-source check.
- Do not store more contact data than the app needs for the user task.
- Keep SwiftUI wrappers' coordinator and delegate lifetimes explicit.

## Validation

- Build the affected app target.
- Test denied, limited, authorized, and changed authorization states.
- Test picker cancel, single/multiple selection, and property-filtered
  selection where applicable.
- Test create/update/delete, vCard import/export, and change-history handling
  when those paths change.
- Test on device when limited-access or ContactsUI platform behavior matters.

## Output

For implementation or review work, return:

1. Contact access model
2. Picker, fetch, mutation, and history findings
3. Privacy, notes, and data-minimization boundaries
4. Validation run or still needed
5. Current-source assumptions for entitlement or platform behavior
