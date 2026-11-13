<p align='left'><strong>Hello There! </strong><img src='https://user-images.githubusercontent.com/74038190/241763891-7bb1e704-6026-48f9-8435-2f4d40101348.gif' height='50'></p>

### I'm Sohail, an ML engineer at [Eyewa](https://github.com/Eyewa). I work on correctness in the open-source libraries that computer vision, robotics and ML systems run on.

**Currently working on**

- **Computer vision:** OpenCV, Ultralytics, Supervision, RF-DETR
- **Robotics and simulation:** Drake, MuJoCo, Newton, Gazebo
- **ML inference and data infra:** vLLM, TensorRT-LLM, Feast, Apache Beam
- **Apple Silicon (MPS):** code paths that crash or drift from CPU results on Mac GPUs

**Selected merged work**

| Project | Merged | One fix to look at |
|:--|--:|:--|
| [OpenCV](https://github.com/opencv/opencv/pulls?q=is%3Apr+is%3Amerged+author%3Asohailshk) | <!-- n:opencv/opencv -->5<!-- /n --> | [CLAHE read pixels outside a sub-matrix while padding](https://github.com/opencv/opencv/pull/30782) |
| [Ultralytics](https://github.com/ultralytics/ultralytics/pulls?q=is%3Apr+is%3Amerged+author%3Asohailshk) | <!-- n:ultralytics/ultralytics -->4<!-- /n --> | [ONNX models on MPS crashed or drifted from CPU results](https://github.com/ultralytics/ultralytics/pull/27117) |
| [Supervision](https://github.com/roboflow/supervision/pulls?q=is%3Apr+is%3Amerged+author%3Asohailshk) | <!-- n:roboflow/supervision -->5<!-- /n --> | [YOLO-NAS pose scores were lost as detection confidence](https://github.com/roboflow/supervision/pull/2909) |
| [Drake](https://github.com/RobotLocomotion/drake/pulls?q=is%3Apr+is%3Amerged+author%3Asohailshk) | <!-- n:RobotLocomotion/drake -->3<!-- /n --> | [yaml_load shared aliased nodes instead of copying them](https://github.com/RobotLocomotion/drake/pull/25230) |
| [Feast](https://github.com/feast-dev/feast/pulls?q=is%3Apr+is%3Amerged+author%3Asohailshk) | <!-- n:feast-dev/feast -->7<!-- /n --> | [Point-in-time SQL joins mixed up entity rows](https://github.com/feast-dev/feast/pull/7124) |
| [Apache Beam](https://github.com/apache/beam/pulls?q=is%3Apr+is%3Amerged+author%3Asohailshk) | <!-- n:apache/beam -->3<!-- /n --> | [RunInference ignored the device for custom inference functions](https://github.com/apache/beam/pull/41086) |

Also merged in NVIDIA torch-harmonics, NeMo Automodel, Docling, Rerun, NumPyro, Kornia, Trimesh, Gazebo, Newton and more.
[See every merged PR →](https://github.com/search?q=is%3Apr+is%3Amerged+author%3Asohailshk+-user%3Asohailshk&type=pullrequests&s=updated)

<details>
<summary><b>Recently merged</b> (updated daily)</summary>

<!-- recent-merged:start -->
- [newton-physics/newton#5294](https://github.com/newton-physics/newton/pull/5294) Fold scalar MJCF actuator gear into joint-target drives
- [feast-dev/feast#7124](https://github.com/feast-dev/feast/pull/7124) fix: Keep entity rows apart in the SQL point-in-time joins
- [opencv/opencv#30782](https://github.com/opencv/opencv/pull/30782) imgproc: do not read pixels outside a sub-matrix in CLAHE padding
- [lballabio/QuantLib#3031](https://github.com/lballabio/QuantLib/pull/3031) Don't move explicit stub dates to the end of the month
- [feast-dev/feast#7142](https://github.com/feast-dev/feast/pull/7142) fix: Use valid Postgres type names for Arrow types in entity dataframe uploads
<!-- recent-merged:end -->

</details>

[sohailshk.me](https://www.sohailshk.me) · [LinkedIn](https://www.linkedin.com/in/mohdsohailshk/)

<sub>Large projects are team efforts. Everything above was reviewed and merged by each project's maintainers.</sub>
