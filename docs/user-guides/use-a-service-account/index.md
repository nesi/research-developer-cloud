---
hidden: false
label_names:
- identity
- security
- service account
position: 1
title: Use a Service Account
description: Build project resources with your team service account rather than a personal account, so that access survives when someone leaves the team.
vote_count: 1
vote_sum: 1
---

Build your project on an account that belongs to the project, not to a person.

When a team member leaves and their account is removed, anything created under
that account goes with it. A service account is an OpenStack user that REANNZ support team
creates for your project and your team shares, so that ownership of instances,
keys and automation is never tied to whether one individual is still with the
organisation.

!!! note
    Service accounts are created on request. 
    [Contact the support team](mailto:support@cloud.nesi.org.nz?subject=Research%20Developer%20Cloud%20Service%20Account).

## When an personnal account is deleted

Instances belong to your **project**, but keypairs and application credentials
are scoped to the **user** who created them. Removing a person's account
therefore leaves the instances running, and breaks everything used to reach and
manage them.

| What was created under a personal account | After the account is removed |
| --- | --- |
| Instances | Still running, and still billed to the project |
| The keypair record in the RDC | Gone, so you cannot see which key built the instance |
| That person's public key in `authorized_keys` | Still there, still valid, nobody managing it |
| Application credentials they created | Stop working, so automation and pipelines fail |
| Their password and dashboard access | Gone, along with any recovery path through it |

The third row is the one that matters most: the departing person's key keeps
working until somebody removes it by hand from every instance. See
[Secure and Rotate SSH Keys](../create-and-manage-keypairs/secure-and-rotate-ssh-keys.md)
for how to do that.

## Which credential to use

A service account does not replace your own key. The two do different jobs, and
using both keeps day-to-day access attributable while keeping the project
recoverable.

| Credential | Belongs to | Used for | Replace it when |
| --- | --- | --- | --- |
| Your personal SSH key | You | Day-to-day connections to instances | You leave, or a device is lost |
| Service account SSH key | The project | Building instances, automation, recovery access | Anyone who held it leaves |
| Service account password | The project | Dashboard sign-in, issuing application credentials | Anyone who held it leaves |

In practice: build the instance with the service account keypair, then add each
team member's personal public key to `authorized_keys` for everyday use. A
departure then costs you one `authorized_keys` edit, not a rebuild.

!!! warning
    Do not use the service account for routine interactive work. Logs record
    the account, not the person, so shared sign-ins make it impossible to tell
    afterwards who ran a command. Reserve it for building resources, for
    automation, and for recovery.

## Request a service account

Please [contact Support](mailto:support@nesi.org.nz) and include:

- The project the account is for
- A name for the account, matching your project so it is recognisable
- Who should be able to use it, and who owns it
- What it will be used for, such as Terraform, a cluster, or shared instances

## Set up the account

Work through these once, when the account is first issued.

1. Sign in to the [RDC Dashboard](https://dashboard.cloud.nesi.org.nz/) as the
   service account and set a new password:

    ``` { .sh }
    openstack user password set --password NEW_PASSWORD --original-password OLD_PASSWORD
    ```

2. Record the new password in your team password manager, not anywhere else.

3. Generate an SSH key for the account on a workstation, following
   [Create a protected key](../create-and-manage-keypairs/secure-and-rotate-ssh-keys.md#create-a-protected-key).
   Give it a passphrase, and store the private key and its passphrase in the
   same password manager entry.

4. Import the public key while authenticated as the service account:

    ``` { .sh }
    openstack keypair create --public-key ~/.ssh/id_svc_project.pub project-svc-2026-08
    ```

5. Build instances with that keypair, then add each person's personal public key
   to `authorized_keys` for day-to-day access.

6. Create [application credentials](index.md) under the service account for any
   automation, so pipelines no longer depend on an individual.

## Who may hold the secrets

The service account is only as good as the discipline around its secrets. A
shared credential that everyone can read is worse than a personal one, because
nothing ties an action back to a person.

- Keep the password, private key and passphrase in a **team password manager**,
  with a separate login per person. Access is then granted and revoked per
  person without changing the secret itself
- Never put them in a repository, chat message, email, ticket or shared drive
- Grant access to the smallest group that needs it, and keep a written list of
  who currently holds it. You will need that list the day someone leaves
- Review the list whenever the team changes, and at least once a year
- Update the password when a team member leaves and rotate it regularly

## When someone leaves

Work through this on their last day. Steps 1 and 2 cover any departure. Steps 3
onwards apply when the person had access to the service account secrets.

1. Remove their personal public key from `authorized_keys` on every instance,
   following
   [Rotate a key step by step](../create-and-manage-keypairs/secure-and-rotate-ssh-keys.md#rotate-a-key-step-by-step)
2. Revoke their login to the team password manager
3. Recreate the service account password, because they knew the old one:

    ``` { .sh }
    openstack user password set --password NEW_PASSWORD --original-password OLD_PASSWORD
    ```

4. Rotate the service account SSH key, because they held a copy of the private
   key, then update the new password and key in the password manager
5. Delete and recreate any application credentials they could have copied. A new
   password does **not** invalidate them, because each has its own secret
6. Check for anything still owned by their personal account, such as keypairs,
   application credentials or instances they built before the team moved to the
   service account
7. Record what was rotated, and when

!!! warning
    Step 5 is the one most often missed. Application credential secrets are
    independent of the account password, so a credential copied before someone
    left keeps working until it is deleted. List them with
    `openstack application credential list` while signed in as the service
    account.

## Move an existing project

If your instances were built with a personal key, you do not need to rebuild
them to change over.

1. Request the service account, and set it up as above
2. Add the service account's public key to `authorized_keys` on every existing
   instance, using steps 3 and 4 of
   [Rotate a key step by step](../create-and-manage-keypairs/secure-and-rotate-ssh-keys.md#rotate-a-key-step-by-step)
3. Recreate application credentials under the service account, and update the
   automation that uses them
4. Build all new instances with the service account keypair
5. Once everything is reachable through the service account, remove the personal
   keys that were being used for ownership rather than day-to-day access

!!! note
    A keypair cannot be transferred between accounts. Import the same public key
    under the service account, or generate a new one, then remove the old
    keypair record from the personal account.

