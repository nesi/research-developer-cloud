---
hidden: false
label_names:
- instance
- Flavors
position: 1
title: Avaliable Instance Flavors
vote_count: 1
vote_sum: 1
---

When you launch an instance in the RDC, you will need to choose a flavor.

What is a flavor? It’s just a template that determines the amount or resources the instance that you launch will utilise, such as: 

- number of processors (vCPUS)

- amount of memory (RAM) 

- Size of the operating system disk

- How much capacity is reserved for you for times when the hosting server is really busy

The flavor name also includes the generation (which generation or architecture of hardware is used), and can also specify other information in specialty flavors, sflavoursuch as which GPU will be attached to the instance. 

The flavors have the following naming:

```
<category prefix><generation>.<amount of vCPUs><GB of RAM>
for example:
balanced1.1cpu2ram
```

## Blanced Flavors

Our `balanced` range general/mixed use. The one to use if you’re not sure and is avaliable by default with any new project, 

```
balanced1.1cpu2ram
balanced1.2cpu4ram
balanced1.4cpu8ram
balanced1.8cpu16ram
balanced1.16cpu32ram
balanced1.32cpu64ram
```

## Compute Flavors

Our `compute` flavors that have a higher ratio if vCPUs to memory, and also have higher guaranteed CPU shares/weight, for more CPU-intensive or -critical tasks.

```
compute1.1cpu2ram
compute1.2cpu4ram
compute1.4cpu8ram
compute1.8cpu16ram
compute1.16cpu32ram
compute1.32cpu64ram
```

## Memory Flavors

Our `memory` flavors that have a higher ratio of Memory per vCPU, and may have other memory-performance optimisations in place for memory-intensive tasks. 

```
memory1.1cpu4ram
memory1.2cpu8ram
memory1.4cpu16ram
memory1.8cpu32ram
memory1.16cpu64ram
memory1.32cpu128ram
```

## Devtest Flavors

Our `devtest` flavors are very small, for testing and general use

```
devtest1.1cpu1ram
devtest1.2cpu2ram
devtest1.4cpu4ram
```

## GPU Flavors

Our `gpu` range consists of the following flavors and is avaliable on request

```
gpu1.44cpu240ram.a40.1g.48gb
gpu1.88cpu480ram.a40x2.1g.48gb
```