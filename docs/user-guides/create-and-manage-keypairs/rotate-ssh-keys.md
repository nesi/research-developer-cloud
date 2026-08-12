---
hidden: false
label_names:
- keypairs
- security
- ssh
position: 2
title: Rotate SSH Keys
description: Replace an SSH key on the Research Developer Cloud, across single instances and whole clusters, without losing access to what is already running.
---

Replacing an SSH key means adding the new one and removing the old one from
every host that trusts it. The RDC keypair record is only part of that, and not
the part that controls access.

!!! warning
    Deleting a keypair in the RDC does **not** revoke access to instances that
    are already running. OpenStack uses the keypair record only to inject your
    public key when an instance is **first built**. After that the key lives in
    `~/.ssh/authorized_keys` on the instance and OpenStack no longer tracks it.
    To retire a key you must remove it from `authorized_keys` on every instance
    that has it.

An instance keeps trusting a key until it is removed from that instance, which
is why the procedure below works the way it does.

## What each action affects

| Action | Running instances | New instances |
| --- | --- | --- |
| Upload a new public key to the RDC | No effect | Get the new key |
| Delete a keypair in the RDC | No effect | Cannot use that name |
| Edit `authorized_keys` on a host | Takes effect at once | No effect |
| Rebuild an instance with a new key | That one instance gets the new key, and is reinstalled | No effect |

## When to rotate a key

Rotation is usually on a routine cycle, brought forward by any of these events.

| Trigger | Urgency |
| --- | --- |
| Routine cycle | Every 12 months |
| Someone leaves the team or project | Same day, see [When someone leaves](../create-and-manage-identity/use-a-service-account.md#when-someone-leaves) |
| A laptop or phone is lost or stolen | Immediately |
| A private key was sent over email or chat | Immediately |
| A key was stored without a passphrase on a shared machine | Immediately |
| An instance shows signs of compromise | Immediately, and see [If a Key Is Compromised](if-a-key-is-compromised.md) |
| A key was shared between people | At the next window, then stop sharing |

## Rotate a key step by step

The order matters: the new key is added and tested before the old one is
removed, so a mistake at any point still leaves you a way in.

!!! note
    Before you start, confirm you have a second way in: console access through
    the [RDC Dashboard](https://dashboard.cloud.nesi.org.nz/), or a colleague
    with their own working key. Recovering an instance whose only key is gone
    is slow.

### 1. Check what you have

List the keypairs on your account and note the name, type and fingerprint of
the one you are replacing:

``` { .sh }
openstack keypair list
```

``` { .sh .no-copy }
+-----------------+-------------------------------------------------+------+
| Name            | Fingerprint                                     | Type |
+-----------------+-------------------------------------------------+------+
| name-rdc-2025-03 | f0:4f:53:d1:3d:aa:71:d9:ef:b6:32:22:88:c2:68:42 | ssh  |
+-----------------+-------------------------------------------------+------+
```

Then list every instance that was built with it, so you know the full set of
hosts to update:

``` { .sh }
openstack server list --long -c Name -c "Key Name" -c Networks
```

Add anything the RDC cannot see: nodes reached through a bastion, hosts you
added the key to by hand, and any automation that holds a copy.

### 2. Generate the new key

Follow
[Create a protected key](secure-your-ssh-keys.md#create-a-protected-key), giving
the new key its own filename and a comment that dates it:

``` { .sh }
ssh-keygen -t ed25519 -a 100 -C "name@laptop-2026-08" -f ~/.ssh/id_rdc_2026_08
```

Keep the old key in place for now. You need it to install the new one.

### 3. Add the new key

Append the new public key to `authorized_keys` on every host from step 1,
authenticating with the old key. The new key is added alongside the old, so
nothing breaks yet:

``` { .sh }
NEWPUB=$(cat ~/.ssh/id_rdc_2026_08.pub)
ssh -i ~/.ssh/id_rdc_2025_03 ubuntu@INSTANCE_IP \
  "umask 077; mkdir -p ~/.ssh; grep -qxF '$NEWPUB' ~/.ssh/authorized_keys \
   || echo '$NEWPUB' >> ~/.ssh/authorized_keys"
```

The `grep -qxF` test makes the command safe to run twice: it appends the key
only if it is not already there.

Repeat for every host. For more than a handful, see
[Rotate keys on a cluster](#rotate-keys-on-a-cluster).

### 4. Test the new key

Leave your current session open. In a **second terminal**, connect with the new
key only:

``` { .sh }
ssh -i ~/.ssh/id_rdc_2026_08 -o IdentitiesOnly=yes ubuntu@INSTANCE_IP
```

`IdentitiesOnly=yes` stops SSH quietly falling back to the old key and giving
you a false pass. You should be prompted for the new passphrase, then let in.

The remaining steps assume this has succeeded on **every** host.

### 5. Remove the old key

Removing the entry from `authorized_keys` is what actually revokes the old key.
Match on the key body rather than the comment, which anyone can edit:

``` { .sh }
OLDPUB=$(awk '{print $2}' ~/.ssh/id_rdc_2025_03.pub)
ssh -i ~/.ssh/id_rdc_2026_08 ubuntu@INSTANCE_IP \
  "grep -v -F '$OLDPUB' ~/.ssh/authorized_keys > ~/.ssh/ak.new \
   && mv ~/.ssh/ak.new ~/.ssh/authorized_keys \
   && chmod 600 ~/.ssh/authorized_keys"
```

Confirm what is left, and that you recognise all of it:

``` { .sh }
ssh -i ~/.ssh/id_rdc_2026_08 ubuntu@INSTANCE_IP "ssh-keygen -lf ~/.ssh/authorized_keys"
```

Other accounts on the host hold their own `authorized_keys`, `root` in
particular:

``` { .sh }
sudo ssh-keygen -lf /root/.ssh/authorized_keys
```

The old private key can come off your workstation once every host is done.

### 6. Update OpenStack

Import the new public key so that instances built from now on receive it:

``` { .sh }
openstack keypair create --public-key ~/.ssh/id_rdc_2026_08.pub name-rdc-2026-08
openstack keypair delete name-rdc-2025-03
```

A dated name keeps the two keys visible side by side and makes the change
obvious in Terraform or Heat plans.

!!! note
    If the keypair name is pinned in a template you cannot easily edit, reuse
    it instead. OpenStack keypairs cannot be updated in place, so delete and
    re-create:

    ``` { .sh }
    openstack keypair delete KEY_PAIR_NAME
    openstack keypair create --public-key ~/.ssh/id_rdc_2026_08.pub KEY_PAIR_NAME
    ```

    Between the two commands the name does not exist, so any automation that
    builds instances will fail until the second command completes.

Confirm the fingerprint in the RDC matches the key on your workstation:

``` { .sh }
openstack keypair list
ssh-keygen -lf ~/.ssh/id_rdc_2026_08.pub -E md5
```

### 7. Record the change

Worth noting in your team documentation or ticket system:

- The date, and who performed the rotation
- Old and new key names, and their fingerprints
- Which hosts were updated, and any that were skipped
- Why the key was rotated, if it was not the routine cycle
- The date the next routine rotation is due

Fingerprints are the useful part: they let anyone confirm later which key a
host actually trusts.

## Rotate keys on a cluster

Kubernetes and other multi-node clusters need the same steps applied to every
node. Two approaches scale better than editing nodes by hand.

### Update every node

Configuration management makes the result repeatable and easy to audit. The
Ansible `authorized_key` module with `exclusive: true` sets the file to exactly
the keys you list, which handles the add and the remove in one pass:

{% raw %}

``` { .yaml }
- name: Set the authorised keys for the ubuntu user
  ansible.posix.authorized_key:
      user: ubuntu
      state: present
      exclusive: true
      key: "{{ lookup('file', '~/.ssh/id_rdc_2026_08.pub') }}"
```

{% endraw %}

!!! warning
    `exclusive: true` removes every other key for that user, including any
    added by a platform tool or a colleague. Run it against one node first, and
    check the result before you run it against the rest.

Reach nodes on a private network through the bastion:

``` { .sh }
ansible-playbook -i inventory.ini rotate-keys.yml \
  --ssh-common-args '-o ProxyJump=ubuntu@BASTION_IP'
```

### Replace nodes instead

Replacing nodes is usually cleaner than editing them. A node built after the
keypair is updated comes up with only the new key, so there is nothing to
remove and no chance of a missed host.

Drain and replace one node at a time so the workload stays up:

``` { .sh }
kubectl drain NODE_NAME --ignore-daemonsets --delete-emptydir-data
```

Delete the node through your cluster tooling, let the group build a
replacement, then confirm it before moving on:

``` { .sh }
kubectl get nodes
```

!!! warning
    `openstack server rebuild --key-name NEW_KEY SERVER` also resets the key,
    but it rebuilds the instance from its image and destroys everything on the
    root disk. Only use it where the instance holds no state.

### New nodes and scaling

Editing `authorized_keys` on a running node changes that node alone. When the
cluster scales up, or replaces a failed node, the replacement is built from the
keypair recorded in the cluster or node-group definition.

Updating that definition as well as the nodes is what stops the old key
reappearing on the next node built. After a scaling event, a new node can be
checked with:

``` { .sh }
ssh -i ~/.ssh/id_rdc_2026_08 -o IdentitiesOnly=yes ubuntu@NEW_NODE_IP \
  "ssh-keygen -lf ~/.ssh/authorized_keys"
```
