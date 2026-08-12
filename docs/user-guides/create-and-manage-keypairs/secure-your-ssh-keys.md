---
hidden: false
label_names:
- keypairs
- security
- ssh
position: 1
title: Secure Your SSH Keys
description: Protect an SSH private key with a passphrase, keep it in an agent, and confirm the key in the RDC is the one on your workstation.
---

An SSH private key is what gets you in to your instances. Unlike a password it
does not expire, nothing prompts you to change it, and a copy can sit forgotten
on an old laptop for years.

This page covers generating a key that is protected from the start, and working
with it day to day. For replacing a key that already exists, see
[Rotate SSH Keys](rotate-ssh-keys.md).

## What makes a key safer

| Choice | Effect |
| --- | --- |
| Generating the key on your own machine | A key the cloud generates for you was known to the cloud, and crossed the network |
| A passphrase on the private key | A stolen laptop or a stray backup is then useless to whoever holds it |
| `ed25519` over RSA | Short, fast, and no key-size trap. RSA 4096 is there for anything too old to accept `ed25519` |
| One key per person, per device | A shared key cannot be revoked for one person, and logs cannot tell you who connected |
| Instances built with a service account | Access survives someone leaving. See [Use a Service Account](../create-and-manage-identity/use-a-service-account.md) |
| Moving the public key, never the private one | A private key that has been through email, chat, a ticket or a shared drive should be treated as exposed |
| `600` on the key and `700` on `~/.ssh` | OpenSSH refuses to use a private key that others can read |
| A comment on every key | `name@laptop-2026-08` tells you whose key it is and when it was made |
| An agent rather than `ssh -A` | Agent forwarding lets the remote host borrow your key. `ProxyJump` does not |
| Rotation on a routine cycle | See [When to rotate a key](rotate-ssh-keys.md#when-to-rotate-a-key) |

## Create a protected key

!!! note
    `openstack keypair create KEY_PAIR_NAME` asks the cloud to generate the
    key for you and returns the private half over the network, with no
    passphrase. Generating the key on your own machine and uploading only the
    public half avoids both. See
    [Create and manage keypairs via CLI](create-and-manage-keypairs-via-cli.md)
    for the full command reference.

Generate the pair on your workstation:

``` { .sh }
ssh-keygen -t ed25519 -a 100 -C "name@laptop-2026-08" -f ~/.ssh/id_rdc_ed25519
```

| Option | Meaning |
| --- | --- |
| `-t ed25519` | Key type. Fast, small, and secure at a fixed strength |
| `-a 100` | Rounds used to derive the encryption key from your passphrase, which slows down anyone guessing it |
| `-C` | A comment stored in the key, so you can identify it later |
| `-f` | Where to write the pair |

You are prompted for a passphrase. The passphrase encrypts the private key on
disk, so a copied key file is worthless without it. A phrase of several
unrelated words, not used anywhere else and kept in your password manager, works
well here.

The command writes two files:

| File | Contents | Who may see it |
| --- | --- | --- |
| `id_rdc_ed25519` | Private key, encrypted with your passphrase | You only |
| `id_rdc_ed25519.pub` | Public key | Anyone |

Then set the permissions:

``` { .sh }
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rdc_ed25519
```

### Add a passphrase later

To add or change the passphrase on a key you already hold, without changing
the key itself:

``` { .sh }
ssh-keygen -p -f ~/.ssh/id_rdc_ed25519
```

!!! note
    This protects the file from here on, but the key material does not change.
    If the key may already have been copied or exposed, a new passphrase
    achieves nothing, and a new key is needed instead. See
    [Rotate SSH Keys](rotate-ssh-keys.md).

### Check a key fingerprint

A fingerprint identifies a key without revealing it, and lets you confirm that
the key in the RDC is the one on your laptop:

``` { .sh }
ssh-keygen -lf ~/.ssh/id_rdc_ed25519.pub
```

``` { .sh .no-copy }
256 SHA256:tMVbtbRdT2vmaZU2ciC5LLWrbql5yw6X8L+OMujXJ1Y name@laptop-2026-08 (ED25519)
```

The RDC displays MD5 fingerprints, so add `-E md5` when comparing against
`openstack keypair list`:

``` { .sh }
ssh-keygen -lf ~/.ssh/id_rdc_ed25519.pub -E md5
```

``` { .sh .no-copy }
256 MD5:57:71:50:18:ac:c2:ed:d9:54:05:c0:62:42:68:1d:3e name@laptop-2026-08 (ED25519)
```

## Use an SSH agent

A passphrase prompt on every connection is the main reason people leave keys
unprotected. An agent avoids that: unlock the key once per session, and the
agent holds it in memory.

Start an agent and add the key:

``` { .sh }
eval "$(ssh-agent -s)"
ssh-add -t 8h ~/.ssh/id_rdc_ed25519
```

`-t 8h` makes the agent forget the key after eight hours, so an unattended
laptop does not stay unlocked overnight. List what the agent currently holds
with `ssh-add -l`, and drop everything with `ssh-add -D`.

An entry in `~/.ssh/config` gets the right key offered automatically:

``` { .sh }
Host rdc-*
    User ubuntu
    IdentityFile ~/.ssh/id_rdc_ed25519
    IdentitiesOnly yes
    AddKeysToAgent yes
```

| Platform | Notes |
| --- | --- |
| Linux | Most desktops start an agent at login, so `eval` is rarely needed |
| macOS | Use `ssh-add --apple-use-keychain` and add `UseKeychain yes` to the config |
| Windows | Run `Set-Service ssh-agent -StartupType Automatic`, then `Start-Service ssh-agent`, in an elevated PowerShell |

!!! note
    Agent forwarding (`ssh -A` or `ForwardAgent yes`) lets anyone with root on
    the machine you connect to use your forwarded agent to authenticate as you
    elsewhere. `ProxyJump` keeps the key on your workstation instead:

    ``` { .sh }
    ssh -J ubuntu@BASTION_IP ubuntu@NODE_IP
    ```

## Retiring a key

Deleting a keypair in the RDC does **not** revoke access to instances that are
already running, because the key lives in `~/.ssh/authorized_keys` on the
instance once it is built. See
[Rotate SSH Keys](rotate-ssh-keys.md) for what that means in practice, and
[If a Key Is Compromised](if-a-key-is-compromised.md) if a key may already be in
someone else's hands.
