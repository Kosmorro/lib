# [Version 1.0.12](https://github.com/Kosmorro/lib/compare/v1.0.11...v) (2025-03-16)

### Bug Fixes

* fix support for Python 3.13 ([#74](https://github.com/Kosmorro/lib/issues/74)) ([240d567](https://github.com/Kosmorro/lib/commit/240d567940c78781ab3010ad5011dd0ac030accb))


# [Version 1.0.11](https://github.com/Kosmorro/lib/compare/v1.0.10...v1.0.11) (2024-08-03)


### Bug Fixes

* **dependencies:** force using Numpy 2.0 ([#73](https://github.com/Kosmorro/lib/issues/73)) ([9332a38](https://github.com/Kosmorro/lib/commit/9332a38c604a2ed73f2cf04bd1e12ed63fbc9b2b))



# [Version 1.0.10](https://github.com/Kosmorro/lib/compare/v1.0.9...v1.0.10) (2023-11-11)


### Bug Fixes

* compatibility with Python 3.12 ([#68](https://github.com/Kosmorro/lib/issues/68)) ([1d84b89](https://github.com/Kosmorro/lib/commit/1d84b89e5663df90a05a3d80567d2dde7d0dd0f7))



# [Version 1.0.9](https://github.com/Kosmorro/lib/compare/v1.0.8...v1.0.9) (2023-08-19)


### Bug Fixes

* fix compatibility with the last versions of NumPy ([#65](https://github.com/Kosmorro/lib/issues/65)) ([e43319b](https://github.com/Kosmorro/lib/commit/e43319bd6dc7f370eecfa923a126f09b740939d2))



# [Version 1.0.8](https://github.com/Kosmorro/lib/compare/v1.0.7...v1.0.8) (2023-05-05)


### Bug Fixes

* **deps:** update skyfield-data requirement from >=3,<5 to >=3,<6 ([#62](https://github.com/Kosmorro/lib/issues/62)) ([a2aa56c](https://github.com/Kosmorro/lib/commit/a2aa56c36b37c1937d6ed04480aec98ed95df739))



# [Version 1.0.7](https://github.com/Kosmorro/lib/compare/v1.0.6...v1.0.7) (2022-11-11)


### Build System

* add support for Python 3.11 ([#58](https://github.com/Kosmorro/lib/issues/58)) ([807be7d](https://github.com/Kosmorro/lib/commit/807be7def324c1accdad6dc35738624589eb7b06))


### BREAKING CHANGES

* Python 3.7 is not supported anymore.



# [Version 1.0.6](https://github.com/Kosmorro/lib/compare/v1.0.5...v1.0.6) (2022-03-19)


### Bug Fixes

* prevent `get_ephemerides()` from returning values out of the dates given in arguments ([1cf40f5](https://github.com/Kosmorro/lib/commit/1cf40f5b40991b6dc567f979f6bd69fc63807e4e))



# [Version 1.0.5](https://github.com/Kosmorro/lib/compare/v1.0.4...v1.0.5) (2022-02-21)


### Bug Fixes

* **ephemerides:** fix the rise, culmination and set times being too often `None` ([bbf1b9f](https://github.com/Kosmorro/lib/commit/bbf1b9f53efb8c906e597c9054f90e674d1b7dd9))
* fix the warning message from `skyfield-data` package about expired data ([f3d39ad](https://github.com/Kosmorro/lib/commit/f3d39ad5bf1d66fcebb4864064111d2f0af87c63))



# [Version 1.0.4](https://github.com/Kosmorro/lib/compare/v1.0.3...v1.0.4) (2022-01-09)


### Bug Fixes

* **Breaking change:** restore `kosmorrolib.__version__` module ([0245394](https://github.com/Kosmorro/lib/commit/02453943ad36829072f339cf9b3695491c8e1f04))



# [Version 1.0.3](https://github.com/Kosmorro/lib/compare/v1.0.2...v1.0.3) (2022-01-09)


### Bug Fixes

* fix packaging ([853d3c1](https://github.com/Kosmorro/lib/commit/853d3c12810200a09d6b3fe713fef83447e22add))



# [Version 1.0.2](https://github.com/Kosmorro/lib/compare/v1.0.1...v1.0.2) (2022-01-09)


### Bug Fixes

* fix Python support for NumPy ([#40](https://github.com/Kosmorro/lib/issues/40)) ([a99ef9d](https://github.com/Kosmorro/lib/commit/a99ef9d6a6b174f653abe2887d8211c809b3a732))
* make the opposition detection more reliable ([#39](https://github.com/Kosmorro/lib/issues/39)) ([761ec4e](https://github.com/Kosmorro/lib/commit/761ec4ef21b95473829672d69320330f52d1890b))
* remove NumPy direct dependency ([#41](https://github.com/Kosmorro/lib/issues/41)) ([f0b4267](https://github.com/Kosmorro/lib/commit/f0b42679853d2d8310005cdde2afd1c7674ccaf9))

  Note that Numpy is still a dependency of Skyfield and its dependencies, so NumPy is actually still needed to run Kosmorrolib. But now, it is not used anymore here.

# [Version 1.0.1](https://github.com/Kosmorro/lib/compare/v1.0.0...v1.0.1) (2021-11-01)


### Bug Fixes

* add missing dependency ([ec255da](https://github.com/Kosmorro/lib/commit/ec255daefdef376b2b43190c7ea2a8e8960cfd99))



# [Version 1.0.0](https://github.com/Kosmorro/lib/compare/v0.11.2...v1.0.0) (2021-11-01)


### Bug Fixes

* **ephemerides:** fix a bug that made the ephemerides calculations impossible for the Poles ([#21](https://github.com/Kosmorro/lib/issues/21)) ([40988f1](https://github.com/Kosmorro/lib/commit/40988f193fe996cf3f56b6b8071ef7b72ec7fa15))


### Features

* add support for Earth perihelion and aphelion ([#30](https://github.com/Kosmorro/lib/issues/30)) ([22a5ee0](https://github.com/Kosmorro/lib/commit/22a5ee0b0394e7c816fee12a40934d959420bef7))
* add support for Python 3.10 ([#32](https://github.com/Kosmorro/lib/issues/32)) ([6fb8d07](https://github.com/Kosmorro/lib/commit/6fb8d0789f76b6571f3b4364b2f2efbcfb098647))
* **event:** add support for Earth seasons ([#24](https://github.com/Kosmorro/lib/issues/24)) ([ad96b8b](https://github.com/Kosmorro/lib/commit/ad96b8bebf9676f1d450bd6f337367664a9616ea)), closes [#21](https://github.com/Kosmorro/lib/issues/21) [#25](https://github.com/Kosmorro/lib/issues/25)
* **event:** add support for lunar eclipses ([#28](https://github.com/Kosmorro/lib/issues/28)) ([f43d604](https://github.com/Kosmorro/lib/commit/f43d6043b057e56de7081093c7470b8b46f632d6))
* use Skyfield-Data library instead of downloading needed files at first time ([#22](https://github.com/Kosmorro/lib/issues/22)) ([50b9569](https://github.com/Kosmorro/lib/commit/50b9569e5ec4121e9b1dd04dac56929309241851))


### BREAKING CHANGES

* Project license is now GNU Affero General Public License (previously it was CeCILL-C)
* EventType constants `MOON_APOGEE` and `MOON_PERIGEE` have been renamed to `APOGEE` and `PERIGEE`
* **event:** the `Event.details` field is now a dictionary (was previously a string).



# [Version 0.11.2](https://github.com/Kosmorro/lib/compare/v0.11.1...v0.11.2) (2021-05-08)


### Bug Fixes

* "minute must be in 0..59" error ([#20](https://github.com/Kosmorro/lib/issues/20)) ([592f8b1](https://github.com/Kosmorro/lib/commit/592f8b15d06e55fd8f0ba174972282e4c8eda6a0))



# [Version 0.11.1](https://github.com/Kosmorro/lib/compare/v0.11.0...v0.11.1) (2021-05-01)


### Bug Fixes

* false positives on opposition ([#17](https://github.com/Kosmorro/lib/issues/17)) ([03f0c57](https://github.com/Kosmorro/lib/commit/03f0c57042604e7690cd736a6e9fa94ffd2b00e4))
* fix error in the serialization of the Object type ([#18](https://github.com/Kosmorro/lib/issues/18)) ([9ad4371](https://github.com/Kosmorro/lib/commit/9ad437103267b404cab689c4a3bc9dd6b7457561))
* remove useless dev dependencies ([#16](https://github.com/Kosmorro/lib/issues/16)) ([152efe7](https://github.com/Kosmorro/lib/commit/152efe72e15de69939c8d558fa6ceaafba4139bd))

### Misc.

* Kosmorrolib now supports Windows environment! ([#14](https://github.com/Kosmorro/lib/pull/14)) ([746ce95](https://github.com/Kosmorro/lib/commit/746ce953c839d9050862c465c036f53c6491e8da))


# [Version 0.11.0](https://github.com/Kosmorro/lib/compare/v0.10.0...v0.11.0) (2021-04-18)


### Bug Fixes

* add missing enums to the exposed model, rename data.py to model.py ([#11](https://github.com/Kosmorro/lib/issues/11)) ([64c8dd9](https://github.com/Kosmorro/lib/commit/64c8dd901da118e8dd11e932ad2a13874ccb2726))


### Build System

* fix some variables in __version__.py ([#13](https://github.com/Kosmorro/lib/issues/13)) ([2d24786](https://github.com/Kosmorro/lib/commit/2d24786f7b2a52c7b9b77ac4d54c0b7e223236f6))


### BREAKING CHANGES

* `__build__` constant in `__version__.py` has been removed.
* `kosmorrolib.data` has been renamed to
`kosmorrolib.model`. To ensure further BC-break to happen on this side,
prefer using the model now exposed from kosmorrolib directly.



# Version 0.10.0 (2021-04-05)


### Bug Fixes

* take the timezone in account on get_moon_phase ([2df588e](https://github.com/Kosmorro/lib/commit/2df588e5c13246c19b3b5828bdf58b95d11ec104))


### Features

* make the date parameter optional (default value: today) ([c59b553](https://github.com/Kosmorro/lib/commit/c59b553c86999958027a7649c52811b2bc5162fd))



