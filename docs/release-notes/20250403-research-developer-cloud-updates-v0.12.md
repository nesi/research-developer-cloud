---
hidden: false
label_names:
- release-note
position: 3
title: Research Developer Cloud updates v0.12 - 20250403
---

##Infrastructure

####OpenStack Upgrade – Caracal Release

We’ve successfully upgraded our OpenStack services to the Caracal release, following the SLURP cadence (https://docs.openstack.org/project-team-guide/release-cadence-adjustment.html).

This upgrade focused on the OpenStack service containers and their underlying components, including databases, RabbitMQ, and other dependencies. The process involved:

Kayobe seed automation and configuration sync
Container version updates pulled via local Pulp mirror
Rolling service deployment across environments
Database migrations and service bring-up
This upgrade ensures we remain aligned with upstream OpenStack developments, improving security, performance, and long-term maintainability of our cloud platform.
