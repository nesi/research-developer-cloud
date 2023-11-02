# Connect to your instance by using SSH

To use SSH to connect to your instance, use the downloaded keypair file.

!!! note
    The user name is `ubuntu` for the Ubuntu cloud images on FlexiHPC. We have a list of default users for the most common cloud images in [Default user for images](default-user-nesi-images.md)

Insure your instance has a `floating ip` associated with it. If you need to assign one then check the following Assign Floating IP to an Instance via the Dashboard

Copy the `floating ip` address for your instance.

Use the **ssh** command to make a secure connection to the instance. For example:

```
ssh -i MyKey.pem ubuntu@10.0.0.2
```

!!! note
    A `MyKey.pem` private key is a key kept secret by the SSH user on their client machine. The user must never reveal the private key to anyone, including the server (server administrator), to ensure the their identity is never compromised.
    Please look at [Create and Manage Keypairs](../create-and-manage-keypairs/index.md) to create or import a keypair for use on the RDC

At the prompt, type `yes`.