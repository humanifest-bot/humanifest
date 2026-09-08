# Security And Isolation

Before executing third-party setup code, inspect:

- package manifests and lifecycle hooks;
- shell scripts;
- Dockerfiles and Compose files;
- CI workflows;
- requested privileges;
- ports, services, mounts, persistent volumes, and network destinations;
- secret requirements.

Default rules:

- never use `sudo` without explicit user approval;
- never expose host Docker socket to untrusted containers;
- never mount unrelated host directories;
- keep secrets environment-scoped and minimal;
- prefer non-root containers;
- destroy or reset disposable environments after contribution work.

Security vulnerability work must follow the target project's private disclosure process.
