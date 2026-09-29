---
hidden: false
label_names:
- release-note
position: 3
title: RDC Updates v0.13
description: OpenStack services on the Research Developer Cloud upgraded from Caracal to the Epoxy release
---

## Epoxy Upgrade

We’ve upgraded our OpenStack services from the Caracal (2024.1) release to the Epoxy (2025.1) release. Epoxy is the next release in the [SLURP cadence](https://docs.openstack.org/project-team-guide/release-cadence-adjustment.html) after Caracal, which allows the upgrade to go directly from one to the other.

As with the Caracal upgrade, this covered the OpenStack service containers and their underlying components, including databases, RabbitMQ, and other dependencies. The process involved:

- Kayobe seed automation and configuration sync
- Container version updates pulled via local Pulp mirror
- Rolling service deployment across environments
- Database migrations and service bring-up

## What Changes for Users

<!-- HPC-803: user-facing changes between Caracal and Epoxy (API, CLI client, Horizon,
deprecations and removals), supplied by the upgrade team. If there are none, say so here. -->

For the full list of upstream changes, see the [OpenStack Epoxy release notes](https://releases.openstack.org/epoxy/index.html).

If something behaves differently after the upgrade, contact us at [support@cloud.nesi.org.nz](mailto:support@cloud.nesi.org.nz).
