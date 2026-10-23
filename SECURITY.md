# Security Policy

This repository handles device pairing tokens and encrypted payloads
for Lumen's optional caregiver sync. Tokens act as long-lived API keys;
a leaked token lets an attacker read and write that device's blobs,
though never decrypt their content without the client-side key.

Do not open a public issue for a security vulnerability. Use GitHub's
private vulnerability reporting on this repository (repository page,
"Security" tab, "Report a vulnerability").

See the [organization-wide security policy](https://github.com/lumen-assistive/.github/blob/main/SECURITY.md)
for response times and scope.
