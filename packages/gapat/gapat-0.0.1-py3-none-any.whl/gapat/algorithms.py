import multiprocessing
import os

import numpy as np
import taichi as ti


def recon(
    signal_backproj,
    detector_location,
    detector_normal,
    volume_range,
    volume_res,
    vs,
    fs,
    num_devices=1,
    device="cpu",
    method="das",
):
    """
    Reconstruction of photoacoustic computed tomography.

    Parameters
    ----------
    signal_backproj : np.ndarray
        The input signal. Each row is a signal of a detector. Shape: (num_detectors, num_times).
    detector_location : np.ndarray
        The location of the detectors. Each row is the coordinates of a detector. Shape: (num_detectors, 3).
    detector_normal : np.ndarray
        The normal direction of the detectors which points to the volume.
        Each row is the normal direction of a detector and length is 1. Shape: (num_detectors, 3).
    volume_range : np.ndarray
        The range of the volume. The first row is the start x, y, z. The second row is the end x, y, z.
        Shape: (2, 3).
    volume_res : float
        The resolution of the volume.
    vs : float
        The speed of sound in the volume.
    fs : float
        The sampling frequency.
    num_devices : int
        The number of devices to run the reconstruction.
    device : str
        The device to run the reconstruction. Options: "cpu", "gpu".
    method : str
        The method of reconstruction. Options: "das", "ubp".
    """

    x_start, y_start, z_start = volume_range[0]
    x_end, y_end, z_end = volume_range[1]
    num_detectors, num_times = signal_backproj.shape
    num_x = int((x_end - x_start) / volume_res)
    num_y = int((y_end - y_start) / volume_res)
    num_z = int((z_end - z_start) / volume_res)
    z = [z_start + i * (z_end - z_start) / num_devices for i in range(num_devices)]

    @ti.kernel
    def recon_kernel_das(
        signal_backproj: ti.types.ndarray(),
        detector_location: ti.types.ndarray(),
        detector_normal: ti.types.ndarray(),
        signal_recon: ti.types.ndarray(),
        x_start: ti.f32,
        y_start: ti.f32,
        z_start: ti.f32,
    ):
        for i, j, k in ti.ndrange(num_x, num_y, num_z):
            point_x = x_start + i * volume_res
            point_y = y_start + j * volume_res
            point_z = z_start + k * volume_res
            total_solid_angle = 0.0
            for n in ti.ndrange(num_detectors):
                detector_to_point_vector_x = point_x - detector_location[n, 0]
                detector_to_point_vector_y = point_y - detector_location[n, 1]
                detector_to_point_vector_z = point_z - detector_location[n, 2]
                distance = ti.sqrt(
                    detector_to_point_vector_x * detector_to_point_vector_x
                    + detector_to_point_vector_y * detector_to_point_vector_y
                    + detector_to_point_vector_z * detector_to_point_vector_z
                )
                d_solid_angle = (
                    detector_to_point_vector_x * detector_normal[n, 0]
                    + detector_to_point_vector_y * detector_normal[n, 1]
                    + detector_to_point_vector_z * detector_normal[n, 2]
                ) / (distance * distance * distance)
                idx = ti.min(int(distance / vs * fs), num_times - 2)
                signal_recon[i, j, k] += signal_backproj[n, idx] * d_solid_angle
                total_solid_angle += d_solid_angle
            signal_recon[i, j, k] /= total_solid_angle

    @ti.kernel
    def recon_kernel_ubp(
        signal_backproj: ti.types.ndarray(),
        detector_location: ti.types.ndarray(),
        detector_normal: ti.types.ndarray(),
        signal_recon: ti.types.ndarray(),
        x_start: ti.f32,
        y_start: ti.f32,
        z_start: ti.f32,
    ):
        for i, j, k in ti.ndrange(num_x, num_y, num_z):
            point_x = x_start + i * volume_res
            point_y = y_start + j * volume_res
            point_z = z_start + k * volume_res
            total_solid_angle = 0.0
            for n in ti.ndrange(num_detectors):
                detector_to_point_vector_x = point_x - detector_location[n, 0]
                detector_to_point_vector_y = point_y - detector_location[n, 1]
                detector_to_point_vector_z = point_z - detector_location[n, 2]
                distance = ti.sqrt(
                    detector_to_point_vector_x * detector_to_point_vector_x
                    + detector_to_point_vector_y * detector_to_point_vector_y
                    + detector_to_point_vector_z * detector_to_point_vector_z
                )
                d_solid_angle = (
                    detector_to_point_vector_x * detector_normal[n, 0]
                    + detector_to_point_vector_y * detector_normal[n, 1]
                    + detector_to_point_vector_z * detector_normal[n, 2]
                ) / (distance * distance * distance)
                idx = ti.min(int(distance / vs * fs), num_times - 2)
                signal_recon[i, j, k] += (
                    signal_backproj[n, idx] - idx * (signal_backproj[n, idx + 1] - signal_backproj[n, idx])
                ) * d_solid_angle
                total_solid_angle += d_solid_angle
            signal_recon[i, j, k] /= total_solid_angle

    def recon_single(device_no):
        if device == "cpu":
            ti.init(arch=ti.cpu)
        elif device == "gpu":
            os.environ["CUDA_VISIBLE_DEVICES"] = str(device_no)
            ti.init(arch=ti.cuda)
        else:
            raise ValueError(f"Invalid device: {device}")
        signal_recon = np.zeros((num_x, num_y, num_z), dtype=np.float32)
        if method == "das":
            recon_kernel_das(
                signal_backproj, detector_location, detector_normal, signal_recon, x_start, y_start, z[device_no]
            )
        elif method == "ubp":
            recon_kernel_ubp(
                signal_backproj, detector_location, detector_normal, signal_recon, x_start, y_start, z[device_no]
            )
        else:
            raise ValueError(f"Invalid method: {method}")
        return signal_recon

    def recon_multi():
        results = []
        pool = multiprocessing.Pool(processes=num_devices)
        for device_no in range(num_devices):
            results.append(pool.apply_async(recon_single, args=(device_no,)))
        pool.close()
        pool.join()
        signal_recon = np.concatenate([result.get() for result in results], axis=2)
        return signal_recon

    if num_devices == 1:
        return recon_single(0)
    elif num_devices > 1:
        return recon_multi()
    else:
        raise ValueError(f"Invalid number of devices: {num_devices}")
