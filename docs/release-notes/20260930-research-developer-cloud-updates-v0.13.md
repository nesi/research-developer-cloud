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

<!-- HPC-803: drafted from the upstream Dalmatian (2024.2) and Epoxy (2025.1) release notes.
Items marked CONFIRM depend on the Epoxy point release or RDC configuration deployed under
FS-18571. Confirm or remove each one before merge, then delete these comments. -->

Moving from Caracal to Epoxy skips the intermediate Dalmatian (2024.2) release, so the changes below come from both the Dalmatian and Epoxy releases. The changes most likely to be noticed are listed here.

### Images and Volumes

<!-- CONFIRM: [image_format]/require_image_format_match is left at its default (true) on RDC. -->
- Glance now inspects uploaded images and checks the contents against the declared disk format. An image uploaded with a disk format that does not match the file, such as a qcow2 file uploaded as `raw`, is rejected. The `qemu-img info` command shows the actual format of an image file.
- qcow2 images that reference an external data file are rejected, both when uploading an image and when creating a volume from an image. Unsafe qcow2 and vmdk files are also rejected.

### Identity

- Application credentials now include any roles implied by the roles selected when the credential is created. For example, a credential created with `member` also carries `reader`.
<!-- CONFIRM: the deployed Keystone is 27.0.2 or later. Remove this item if not. -->
- Tokens issued from an application credential are no longer able to create or manage trusts. Tools that create trusts on the user's behalf, such as Heat stacks, are not able to authenticate with an application credential.
<!-- CONFIRM: the deployed Keystone is 27.1.0 or later. Remove this item if not. -->
- A token issued from an application credential is no longer able to be exchanged for another token, or to create and delete application credentials. Authenticating with the username and password, or with a new application credential, is unaffected.

### Instances

- Server details now include the properties of the image the instance was launched from (compute API version 2.98), and the scheduler hints given when the instance was created (compute API version 2.100).
- Resizing to a flavour with less swap space now works, including a flavour with no swap.
<!-- CONFIRM: the deployed Nova is 31.3.1 or later. Remove this item if not. -->
- Launching an instance with a security group given by name fails if more than one security group in the project has that name. Giving the security group ID avoids this.

### Networking

- Networks, ports, routers, floating IPs and security groups are able to carry up to 50 tags each. A resource that already has more than 50 tags keeps them, but no tags are able to be added or changed until some are removed.
- Project members are now able to update and delete subnets in their project.
- Security group rules accept `any` as the protocol, as described in the API reference.

### Command Line Client

- The current `openstack` command line client needs Python 3.9 or later. On older Python versions, `pip` installs an older client that does not include the newest options.
- In `openstack volume set`, the `--retype-policy` option is now named `--migration-policy`.

For the full list of upstream changes, see the [OpenStack Dalmatian release notes](https://releases.openstack.org/dalmatian/index.html) and the [OpenStack Epoxy release notes](https://releases.openstack.org/epoxy/index.html).

If something behaves differently after the upgrade, contact us at [support@cloud.nesi.org.nz](mailto:support@cloud.nesi.org.nz).
