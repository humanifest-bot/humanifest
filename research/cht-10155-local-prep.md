# CHT #10155 Local Prep

Date: 2026-09-06.

Target clone: `/private/tmp/humanifest-cht-core`

Branch: `10155-edit-user-load-state`

## Decision

Start with CHT #10155 rather than more Humanifest-internal work. This issue is a better near-term proof of Humanifest than more scaffold polish: it is labeled Help wanted, has prior maintainer guidance, is user-facing but not clinical, and is small enough for line-by-line review.

Do not open a PR yet. Prior PR #10824 closed stale, so a replacement PR should be preceded by a short maintainer check.

## Source Mapping

- Controller: `admin/src/js/controllers/edit-user.js`
- Template: `admin/src/templates/edit_user.html`
- Unit tests: `admin/tests/unit/controllers/edit-user.spec.js`
- Translation files: `api/resources/translations/messages-{en,es,fr,ne,pt,sw}.properties`

## Local Patch Shape

- Add `loadingUserDetails` while `determineEditUserModel()` and `datasourcePromise` resolve.
- Add `userDetailsLoadFailed` if setup rejects.
- Hide edit form until details load successfully.
- Use existing `setError(err, 'admin.user.load.error')` modal error path.
- Disable and guard submit while loading or failed.
- Add focused controller tests for loading, failure, and submit guards.

## Difference From Stale PR #10824

The stale PR added loading/error flags and translations. This prep branch also guards `editUser()` in the controller because the modal's `disable-submit` only applies a disabled CSS class; `ng-click` can still call the submit handler.

## Checks Run

```bash
node --check admin/src/js/controllers/edit-user.js
git diff --check
```

Both passed.

## Checks Not Run

`npm run unit-admin` was not run because this fresh clone has no `node_modules`, and `npm install` would execute CHT `postinstall` and `prepare` scripts (`patch-package`, `husky`). Run tests only in an approved devcontainer/Codespaces or after explicit approval for dependency setup.

## Next Step

Ask maintainers whether they want a replacement PR for #10155 and whether the loading/error/submit-guard approach matches current expectations.

## Recheck: 2026-09-08

The [current recheck](2026-09-08-opportunity-recheck.md) confirms the local patch is
still uncommitted; no Karma result was verified in that recheck. Current translation guidance
has changed since the historical PR discussion; the original English-placeholder
preparation must not be presented as completing today's translation requirements.
Current opportunity records remain controlling, and maintainer confirmation is
still absent from the inspected discussions.
