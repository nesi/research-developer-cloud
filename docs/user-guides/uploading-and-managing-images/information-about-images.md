---
hidden: false
label_names:
- images
position: 1
title: Understanding RDC Images
vote_count: 1
vote_sum: 1
---

We provide a range of images for use in the Researcher Developer Cloud (RDC). These images are grouped into four visibility categories:

## Public
These images are available to all RDC users. They are the latest versions we’ve produced and are recommended for general use unless you have specific requirements.

- **Virtual Machine (VM) images** typically follow the naming pattern:  
  `rdc-<OS>-<version>-<description>`  
  For example: `rdc-rocky-9-upstream`  
  “Upstream” indicates the image is built from base OS provider images. These include:
  - `fail2ban` for basic security
  - A message of the day
  - RDC terms and conditions

- **Kubernetes images** follow a more detailed naming convention:  
  `<OS>-<version>-<container runtime>-<special packages (optional)>-<Kubernetes version>`  
  Examples:
  - `rocky-9-containerd-nvidia-v1.32.7` (GPU support)
  - `rocky-9-containerd-v1.33.3` (standard image)

## Private
Images created specifically within your project. These are only visible and usable within that project.

## Shared
Images that were originally private but have been shared with you by another project.

## Community
This visibility includes a growing list of images shared by the community.

Public images that are no longer actively maintained—but may still be in use—are moved to the Community category. A date is appended to each image name to indicate when it was retired. These images do not require special access permissions.

Over time, community images may be cleaned up. Because the list is expanding, we recommend using the search function to locate specific images.

## Image Lifecycle & Best Practices
Public images are regularly maintained. When a new image is released (e.g. with a newer OS version), the older one is moved to **Community** visibility before eventual removal.

Because image lifecycles can be short, we recommend:

- **Creating your own image** from a public base image.
- **Customizing it** with any additional software or packages you need.
- **Using your custom image** for deployments to avoid unexpected changes.

## Image Metadata
To help others (and your future self), we recommend adding metadata to your images to describe the starting image, their contents (if anything else was added) as well as any other description fields that you feel pertinent. 

<figure markdown>
  ![Screenshot of image metadata fields in the RDC dashboard](../../../assets/images/flexi/image-metadata.png)
</figure>
