# Deployment Standard Operating Procedure

## Purpose
This SOP defines the production deployment process for the Atlas service.

## Pre-deployment
Create a release branch, run unit and integration tests, review the migration plan, and obtain approval from the service owner. The deployment checklist must include rollback steps and database backup verification.

## Deployment process
Build the immutable container, scan it for vulnerabilities, deploy to staging, run smoke tests, and promote to production using a canary rollout. Monitor error rate and SQL timeout latency for fifteen minutes. If the error budget is exceeded, stop the rollout and execute rollback.

## Risks
SQL timeout during migration can block requests. A failed rollback may require restoring the latest database backup.

## Change record
Owner: Platform Engineering
Version: 2.0
