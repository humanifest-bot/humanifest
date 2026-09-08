# Maintainer Inquiry Draft: CHT #10155

Do not send without explicit user approval.

Hi CHT maintainers,

I saw that [#10155](https://github.com/medic/cht-core/issues/10155) is still open and that the previous PR [#10824](https://github.com/medic/cht-core/pull/10824) was closed stale rather than merged.

Would a replacement PR still be welcome for this? My planned scope is narrow:

- show a spinner while the edit-user modal is loading the required user details;
- do not render empty editable fields until the details are loaded;
- surface an error through the existing modal error path if loading fails;
- prevent submit while loading or after load failure;
- add focused admin controller tests for those states;
- keep translations limited to the supported language files, using English placeholders if that is still the preferred process.

I will avoid opening a PR unless this is still wanted.

AI assistance disclosure: I am using AI-assisted source reading and patch preparation, with human review and line-by-line responsibility for any submitted changes.
