## 1.2.1

*Note we skipped a version to align with `pzip`. Also, 1.2.0 was yanked due to incorrect
packaging.*

* Drop support for Django 3.x and Python 3.8
* Test on Django 5.x and Python 3.13
* Fixed an issue where the `needs_rotation` signal could be sent multiple times, and for
  invalid keys
* Require `pzip>=1.2.0` to address an issue on Python 3.13
* Expanded `PZipStorage.DEFAULT_NOCOMPRESS` to include more already-compressed filetypes
