---
hidden: false
label_names:
- instance
- resize
position: 2
title: Deployment of an instance with Terraform
vote_count: 1
vote_sum: 1
---

!!! note
    You will need to have Terraform installed on the machine that will be executing the commands. Follow the [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) link from the official documentation.

Normally creating a folder space for Terraform projects can be a good thing as this ensures the Terraform state file doesn't clash with another.

Once you are in an empty folder, example `terraform-example-flexihpc`, we will need to create a file called `main.tf`

Inside this file we will need to define the provider

```
provider "openstack" {
  auth_url    = "https://keystone.akl-1.cloud.nesi.org.nz/v3"
  user_name   = "FLEXIHPC_USERNAME"
  password    = "FLEXIHPC_PASSWORD"
  project_id  = "FLEXIHPC_PROJECT_NAME"
  region      = "akl-1"
}
```

Replace the placeholders `FLEXIHPC_USERNAME`, `FLEXIHPC_PASSWORD` and `FLEXIHPC_PROJECT_NAME` with your actual OpenStack authentication details.

Then within the same file we want to define the compute instance

```
resource "openstack_compute_instance_v2" "compute_instance" {
  name            = "compute-instance-0"
  flavor_id       = "FLEXIHPC_FLAVOR_ID"
  image_id        = "FLEXIHPC_IMAGE_ID"
  key_pair        = "FLEXIHPC_KEY_PAIR_NAME"
  security_groups = ["FLEXIHPC_SECURITY_GROUP_NAME"]

  network {
    name = "FLEXIHPC_NETWORK_NAME"
  }
}
```

Replace the placeholders `FLEXIHPC_FLAVOR_ID`, `FLEXIHPC_IMAGE_ID`, `FLEXIHPC_KEY_PAIR_NAME`, `FLEXIHPC_SECURITY_GROUP_NAME`, and `FLEXIHPC_NETWORK_NAME` with appropriate values from your OpenStack environment.

The network name is normally the same as your FlexiHPC project name.

Then we want to apply a floating IP to the instance so we can connect from outside the FlexiHPC platform

```
resource "openstack_networking_floatingip_v2" "floating_ip" {
  pool = "external"
}

resource "openstack_compute_floatingip_associate_v2" "floating_ip_association" {
  floating_ip = openstack_networking_floatingip_v2.floating_ip.address
  instance_id = openstack_compute_instance_v2.compute_instance.id
}
```

The floating IP pool is `external` within the FlexiHPC platform.

Once all the above is filled in then you only need to run the standard terraform commands

```
terraform init
```

This will initialize the terraform directory with all the required modules

Then we run the command to create our resources

```
terraform apply
```

Terraform will prompt you to confirm the changes. Type "yes" to proceed with the creation of the compute instance and the floating IP association.

Terraform will then provision the compute instance and associate the floating IP to it.

Remember that this is a basic example, and you might need to adapt it to your specific FlexiHPC environment and configurations.

The full `main.tf` file for completeness

```
terraform {
required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.51.1"
    }
  }
}

provider "openstack" {
  auth_url    = "https://keystone.akl-1.cloud.nesi.org.nz/v3"
  user_name   = "FLEXIHPC_USERNAME"
  password    = "FLEXIHPC_PASSWORD"
  project_id  = "FLEXIHPC_PROJECT_NAME"
  region      = "akl-1"
}

resource "openstack_compute_instance_v2" "compute_instance" {
  name            = "compute-instance-0"
  flavor_id       = "FLEXIHPC_FLAVOR_ID"
  image_id        = "FLEXIHPC_IMAGE_ID"
  key_pair        = "FLEXIHPC_KEY_PAIR_NAME"
  security_groups = ["FLEXIHPC_SECURITY_GROUP_NAME"]

  network {
    name = "FLEXIHPC_NETWORK_NAME"
  }
}

resource "openstack_networking_floatingip_v2" "floating_ip" {
  pool = "external"
}

resource "openstack_compute_floatingip_associate_v2" "floating_ip_association" {
  floating_ip = openstack_networking_floatingip_v2.floating_ip.address
  instance_id = openstack_compute_instance_v2.compute_instance.id
}
```