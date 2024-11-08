# Release notes

See also the
[unreleased changes](https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.5.3...branch%2Fdefault).

## [0.5.3] (2024-07-25)

- Support for Python 3.12 and Numpy 2.0

## [0.5.2] (2024-05-24)

- New command `fluidimage-mean` to compute mean of images with the new topology
  {class}`fluidimage.topologies.mean.TopologyMeanImage`.

- New executors `multi_exec_sync` ({mod}`fluidimage.executors.multi_exec_sync`) and
  `multi_exec_subproc_sync` ({mod}`fluidimage.executors.multi_exec_subproc_sync`).

- [!108](https://foss.heptapod.net/fluiddyn/fluidimage/-/merge_requests/108): save UVmat
  error codes in PIV files.

## [0.5.1] (2024-05-06)

- Follow UVmat: change defaults and exact meaning for parameter
  `params.multipass.smoothing_coef` (=2).

## [0.5.0] (2024-05-02)

- UVmat compatibility (launching in "local" mode).
- Change defaults and exact meaning for parameters. `params.multipass.smoothing_coef`
  (=2) and `params.multipass.threshold_tps` (=1.5).
- PIV saving: use float32 and save "smooth" displacement fields.

## [0.4.6] (2024-04-20)

- Fix a memory leak related to Pythran in {mod}`fluidimage.calcul.subpix` (see
  [!97](https://foss.heptapod.net/fluiddyn/fluidimage/-/merge_requests/97)).
- Performance optimizations for PIV.
- Remove `params.piv0.coef_correl_no_displ` (old useless parameter).
- Add option `--version` to fluidimage apps.
- `fluidimage-monitor`: show time info.
- Internal: better fft and correl with more testing.

## [0.4.5] (2024-04-17)

- Performance optimizations for PIV (- ~40% of CPU time without TPS)

## [0.4.4] (2024-04-16)

- `fluidimage-monitor` [Textual](https://textual.textualize.io/) app to monitor
  executions of topologies.
- Update and test doc/examples/piv_as_real.
- Support `pip install fluidimage[all]`.
- Change in PIV file names (can now be something like "piv02ab.h5").

## [0.4.3] (2024-03-27)

- [!85](https://foss.heptapod.net/fluiddyn/fluidimage/-/merge_requests/85):
  `fluidpivviewer`.
- [!84](https://foss.heptapod.net/fluiddyn/fluidimage/-/merge_requests/84):
  `multi_exec_async` using {class}`fluidimage.topologies.splitters.Splitter`.
- Other bugfixes and improvements (name PIV files and
  {class}`fluidimage.postproc.vector_field.VectorFieldOnGrid`).

## [0.4.2] (2024-03-20)

- Fix 2 bugs affecting PIV computations (`nb_peaks_to_search` and interpolation close to
  the borders of the image).

## [0.4.1] (2024-03-20)

- Fix a bug affecting PIV results (forget to rename a private method)!

## [0.4.0] (2024-03-18)

```{danger}

[0.4.0] should not be used because it contains a bug leading to wrong PIV results!

```

```{warning}

This version contains incompatible API changes documented below. It is particularly
interesting because it introduces a new executor (called "multi_exec_subproc") which
should work fine on operative systems like Windows and macOS. Since this is now the
default executor for these OSs, users should be able to use it without noticing.

```

### Changed

- Parameters for {class}`fluidimage.preproc.Topology` are now directly in `params` and no
  longer in `params.preproc`.

- Change topology logs, progress bars using [Rich](https://rich.readthedocs.io).

- Image to image functions take a tuple `(key, image)`

- `kind` can be `"eat key value"` (see {class}`fluidimage.topologies.base.Work`).

### Added

- [#74](https://foss.heptapod.net/fluiddyn/fluidimage/-/merge_requests/74): New executor
  `multi_exec_subproc` defined in
  {class}`fluidimage.executors.multi_exec_subproc.MultiExecutorSubproc` based on
  {class}`fluidimage.topologies.splitters.Splitter`. Useful for operative systems that do
  not support forks (in particular Windows).

- New method {func}`fluidimage.topologies.base.TopologyBase.read_log_data`.

## [0.3.0] (2024-03-05)

```{warning}

This version contains incompatible API changes documented here.

```

### Removed

- The parameter `strcouple` is replaced by `str_subset`.
- `from fluidimage.preproc import PreprocBase` has to be replaced by
  `from fluidimage.preproc import Work`.

### Changed

- Better default for `params.series.str_subset` (`"pairs"` for PIV),
  `params.series.ind_start` (`"first"`), `params.preproc.series.str_subset` (`"all1by1"`)
  and `params.preproc.series.ind_first` (`"first"`).

### Added

- Module {mod}`fluidimage.piv` to import the PIV classes `Work` and `Topology`.

- Module {mod}`fluidimage.image2image` to import classes `Work` and `Topology` for
  user-defined preprocessing.

- Modules {mod}`fluidimage.bos` and {mod}`fluidimage.optical_flow` to import the
  corresponding `Work` and `Topology` classes.

- The work classes {class}`fluidimage.piv.Work`, {class}`fluidimage.preproc.Work` and
  {class}`fluidimage.optical_flow.Work` now have parameters in `params.series` and a
  method {func}`fluidimage.works.BaseWorkFromSerie.process_1_serie` (see the examples on
  [preprocessing](./examples/preproc.md) and [PIV](./examples/piv_try_params.md)).

- The work classes {class}`fluidimage.image2image.Work` and {class}`fluidimage.bos.Work`
  now have a parameters in `params.images` and a method
  {func}`fluidimage.works.BaseWorkFromImage.process_1_image`.

- The work class {class}`fluidimage.image2image.Work` has a new method
  {func}`fluidimage.works.image2image.WorkImage2Image.display`.

- The work class {class}`fluidimage.preproc.Work` has a new method
  {func}`fluidimage.works.preproc.WorkPreproc.display`.

## [0.2.0] (2024-02-19)

- Python >=3.9,\<3.12
- Better support for Windows and MacOS
- Fix bugs related to subpix and `nb_peaks_to_search`
- Dev and build: PDM, Nox and Meson

## [0.1.5] (2023-02-15)

- Requires Python 3.9
- Improves legend, warnings, error log and documentation

## [0.1.4] (2022-12-13)

- Support Python 3.10
- Avoid a bug with pyfftw 0.13

## [0.1.3] (2021-09-29)

- Many bugfixes!
- Improve VectorFieldOnGrid and ArrayOfVectorFieldsOnGrid
- UVmat compatibility
- Fix incompatibility OpenCV and PyQt5

## [0.1.2] (2019-06-05)

- Bugfix install Windows

## [0.1.1] (2019-05-23)

- Optical flow computation
- Bugfixes + internal code improvements

## 0.1.0 (2018-10-03)

- New topologies and executors with Trio!
- Much better coverage & many bugfixes!
- Better surface tracking

## 0.0.3 (2018-08-29)

- Requirement Python >= 3.6
- Surface tracking
- image2image preprocessing
- BOS topology
- Handle .cine file
- Calibration
- fluidimslideshow-pg and fluidimviewer-pg (based on PyQtgraph)
- OpenCV backend for preprocessing

## 0.0.2 (2017-04-13)

- Bug fixes and documentation changes.
- Continuous integration (python 2.7 and 3.5) with bitbucket pipelines
  ([coverage ~40%](https://codecov.io/gh/fluiddyn/fluidimage))
- Preprocessing of images.
- First simple GUI (`fluidimviewer` and `fluidimlauncher`).

## 0.0.1b (2016-05-31)

- Topology and waiting queues classes to run work in parallel.
- PIV work and topology (multipass, different correlation methods).

[0.1.1]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.1.0...0.1.1
[0.1.2]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.1.1...0.1.2
[0.1.3]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.1.2...0.1.3
[0.1.4]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.1.3...0.1.4
[0.1.5]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.1.4...0.1.5
[0.2.0]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.1.5...0.2.0
[0.3.0]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.2.0...0.3.0
[0.4.0]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.3.0...0.4.0
[0.4.1]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.4.0...0.4.1
[0.4.2]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.4.1...0.4.2
[0.4.3]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.4.2...0.4.3
[0.4.4]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.4.3...0.4.4
[0.4.5]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.4.4...0.4.5
[0.4.6]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.4.5...0.4.6
[0.5.0]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.4.6...0.5.0
[0.5.1]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.5.0...0.5.1
[0.5.2]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.5.1...0.5.2
[0.5.3]: https://foss.heptapod.net/fluiddyn/fluidimage/-/compare/0.5.2...0.5.3
