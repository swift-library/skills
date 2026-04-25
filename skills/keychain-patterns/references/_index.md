# Keychain Patterns References

Use these files selectively. Start with the task-specific file, then add
`common-anti-patterns.md` for review work and `testing-security-code.md` when
the task requires tests.

| File | Use for |
| --- | --- |
| `keychain-fundamentals.md` | SecItem CRUD, query dictionaries, OSStatus handling, add-or-update, macOS data protection keychain |
| `keychain-item-classes.md` | kSecClass selection, primary keys, GenericPassword vs InternetPassword, keys, certificates, identities |
| `keychain-access-control.md` | kSecAttrAccessible, SecAccessControl flags, lock-state behavior, data protection classes |
| `keychain-sharing.md` | Access groups, app extensions, iCloud Keychain sync, entitlement debugging |
| `credential-storage-patterns.md` | OAuth tokens, API keys, password lifecycle, logout cleanup, key rotation |
| `migration-legacy-stores.md` | Moving secrets out of UserDefaults, @AppStorage, plists, NSCoding, and stale installs |
| `biometric-authentication.md` | Keychain-bound Face ID / Touch ID, LAContext pitfalls, enrollment changes |
| `common-anti-patterns.md` | Review backbone for insecure storage, ignored errors, biometric bypasses, weak crypto, and logging |
| `testing-security-code.md` | Protocol-based keychain tests, simulator/device split, CI handling |
| `compliance-owasp-mapping.md` | OWASP Mobile Top 10, MASVS, and MASTG audit mapping |

Some copied references mention CryptoKit or certificate trust as neighboring
security topics. For deep work in those areas, use `cryptokit-patterns` or
`certificate-trust-patterns` rather than expanding this skill's scope.
