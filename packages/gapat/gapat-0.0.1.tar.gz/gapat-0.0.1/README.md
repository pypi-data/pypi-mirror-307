# A comprehensive framework of GPU-accelerated image reconstruction for photoacoustic computed tomography

The repository provides code of the paper with the same name as this repository.

> A comprehensive framework of GPU-accelerated image reconstruction for photoacoustic computed tomography.

## Abstract

**Significance**: Photoacoustic Computed Tomography (PACT) is a promising non-invasive imaging technique for both life science and clinical implementations. To achieve fast imaging speed, modern PACT systems have equipped arrays that have hundreds to thousands of ultrasound transducer (UST) elements, and the element number continues to increase. However, large number of UST elements with parallel data acquisition could generate a massive data size, making it very challenging to realize fast image reconstruction. Although several research groups have developed GPU-accelerated method for PACT, there lacks an explicit and feasible step-by-step description of GPU-based algorithms for various hardware platforms.

**Aim**: In this study, we propose a comprehensive framework for developing GPU-accelerated PACT image reconstruction (Gpu-Accelerated PhotoAcoustic computed Tomography, _**GAPAT**_), helping the research society to grasp this advanced image reconstruction method.

**Approach**: We leverage widely accessible open-source parallel computing tools, including Python multiprocessing-based parallelism, Taichi Lang for Python, CUDA, and possible other backends. We demonstrate that our framework promotes significant performance of PACT reconstruction, enabling faster analysis and real-time applications. Besides, we also described how to realize parallel computing on various hardware configurations, including multicore CPU, single GPU, and multiple GPUs platform.

**Results**: Notably, our framework can achieve an effective rate of approximately 871 times when reconstructing extremely large-scale 3D PACT images on a dual-GPU platform compared to a 24-core workstation CPU. Besides this manuscript, we shared example codes in the GitHub.

**Conclusions**: Our approach allows for easy adoption and adaptation by the research community, fostering implementations of PACT for both life science and medicine.

**Keywords**: photoacoustic computed tomography, large-scale data size, GPU-accelerated method, Taichi Lang for python, multiple GPU platform.
