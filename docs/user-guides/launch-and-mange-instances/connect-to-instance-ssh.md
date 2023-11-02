# Connect to your instance by using SSH

To use SSH to connect to your instance, use the downloaded keypair file.

!!! note
    The user name is `ubuntu` for the Ubuntu cloud images on FlexiHPC.

Insure your instance has a `floating ip` associated with it. If you need to assign one then check the following Assign Floating IP to an Instance via the Dashboard

Copy the `floating ip` address for your instance.

Use the **ssh** command to make a secure connection to the instance. For example:
```
ssh -i MyKey.pem ubuntu@10.0.0.2
```
At the prompt, type `yes`.