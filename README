![Python CI](https://github.com/ashutoshshelke/openshift-maintenance-lab/actions/workflows/ci.yml/badge.svg)

Incident: Application Pods repeatedly failed after a deployment change.

Symptom: The new Pod could not reach the Running state.

Investigation: Used oc get pods, oc describe pod, oc logs, and cluster events.

Root cause: APP_FILE pointed to a nonexistent Python file.

Resolution: Removed the invalid environment variable and verified successful rollout and health response.

## Maintenance and Backport Exercise

### Incident

The `/items` endpoint returned HTTP 500 when a client supplied a
non-numeric `limit` query parameter.

### Root cause

The endpoint converted untrusted query input directly using `int()`.
Invalid input raised an unhandled `ValueError`.

### Fix

- Added explicit integer validation.
- Added an accepted range of 1–100.
- Returned HTTP 400 for invalid client input.
- Added regression tests for valid, invalid, and out-of-range values.
- Validated the change through GitHub Actions.

### Backport

The fix was developed on `main` and cherry-picked into the supported
`release-1.0` branch. The complete test suite passed on both streams.
