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



