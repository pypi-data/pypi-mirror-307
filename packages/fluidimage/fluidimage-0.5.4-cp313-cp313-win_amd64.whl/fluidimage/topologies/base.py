"""Topology base (:mod:`fluidimage.topologies.base`)
====================================================

.. autoclass:: Work
   :members:
   :private-members:

.. autoclass:: Queue
   :members:
   :private-members:

.. autoclass:: TopologyBase
   :members:
   :private-members:

.. autoclass:: TopologyBaseFromSeries
   :members:
   :private-members:

.. autoclass:: TopologyBaseFromImages
   :members:
   :private-members:

"""

import json
import os
import sys
from abc import ABC, abstractmethod
from collections import OrderedDict
from pathlib import Path
from typing import Sequence, Union
from warnings import warn

from fluiddyn.io.query import query
from fluidimage import ParamContainer, SerieOfArraysFromFiles, SeriesOfArrays
from fluidimage.util import DEBUG, cstring, logger

from ..executors import (
    ExecutorBase,
    get_executor_names,
    import_executor_class,
    supported_multi_executors,
)

how_values = ("ask", "new_dir", "complete", "recompute", "from_path_indices")


def prepare_path_dir_result(
    path_dir_input, path_saving, postfix_saving, how_saving
):
    """Makes new directory for results, if required, and returns its path."""

    if how_saving not in how_values:
        raise ValueError(
            f"how_saving (here equal to '{how_saving}') "
            f"should be in {how_values}"
        )

    path_dir_input = str(path_dir_input)

    if path_saving is not None:
        path_dir_result = path_saving
    else:
        path_dir_result = path_dir_input + "." + postfix_saving

    how = how_saving
    if not os.path.exists(path_dir_result):
        if how == "ask":
            how = "recompute"
    else:
        if how == "ask":
            answer = query(
                f"The directory {path_dir_result} "
                + "already exists. What do you want to do?\n"
                "New dir, Complete, Recompute or Stop?\n"
            )

            while answer.lower() not in ["n", "c", "r", "s"]:
                answer = query(
                    "The answer should be in ['n', 'c', 'r', 's']\n"
                    "Please type your answer again...\n"
                )

            if answer == "s":
                print("Stopped by the user.")
                sys.exit()

            elif answer == "n":
                how = "new_dir"
            elif answer == "c":
                how = "complete"
            elif answer == "r":
                how = "recompute"

        if how == "new_dir":
            i = 0
            while os.path.exists(path_dir_result + str(i)):
                i += 1
            path_dir_result += str(i)

    path_dir_result = Path(path_dir_result)
    path_dir_result.mkdir(exist_ok=True)
    return path_dir_result, how


class Work:
    """Represent a work

    Work are treated differently by executors depending of the ``kind``
    argument. Work can be:

    - "global": the work acts globally on its input and output queues.

    - "one shot": the work has to be called only once per execution.

    - "io": the work involves input/output and is not computationally heavy.

    - "eat key value": the work takes as argument a tuple ``(key, value)``.

    """

    def __init__(
        self,
        name: str,
        func_or_cls,
        params_cls=None,
        input_queue=None,
        output_queue=None,
        kind: Union[str, Sequence[str]] = None,
    ):
        self._kwargs = dict(
            name=name,
            func_or_cls=func_or_cls,
            params_cls=params_cls,
            input_queue=input_queue,
            output_queue=output_queue,
            kind=kind,
        )
        # to avoid a pylint warning
        self.name = None

        self.__dict__.update(self._kwargs)
        self.name_no_space = self.name.replace(" ", "_")

        if kind is None:
            self._eat_key_value = False
        elif isinstance(kind, str):
            self._eat_key_value = kind == "eat key value"
        else:
            self._eat_key_value = "eat key value" in kind

    def __repr__(self):
        return super().__repr__() + f"\n{self._kwargs}"

    def check_exception(self, key, obj):
        """Check if `obj` is an exception"""
        if isinstance(obj, Exception):
            if self.output_queue is not None:
                self.output_queue[key] = obj
            else:
                logger.error(
                    cstring(
                        f"work {self.name_no_space} ({key}) "
                        "can not be done because of a previously "
                        "raised exception.",
                        color="FAIL",
                    )
                )
            return True
        return False

    def prepare_argument(self, key, obj):
        if self._eat_key_value:
            return (key, obj)
        else:
            return obj


class Queue(OrderedDict):
    """Represent a queue"""

    def __init__(self, name, kind=None):
        self.name = name
        self.kind = kind
        super().__init__()

    def __repr__(self):
        return f'\nqueue "{self.name}": ' + super().__repr__()

    def __copy__(self):
        new_one = type(self)(self.name, kind=self.kind)
        new_one.__dict__.update(self.__dict__)

        for key, values in self.items():
            new_one[key] = values

        return new_one

    def pop_first_item(self):
        """Pop the first item of the queue"""
        return self.popitem(last=False)

    def is_name_in_values(self, image_name):
        """Check if a name is in the queue"""
        for names in self.values():
            if image_name in names:
                return True
        return False


class QueueList(list):

    def __init__(self, name):
        self.name = name
        super().__init__()


class TopologyBase:
    """Base class for topologies of processing.

    This class is meant to be subclassed, not instantiated directly.

    Parameters
    ----------

    path_dir_result : None, str

    logging_level : None,  {'warning', 'info', 'debug', ...}

    nb_max_workers : None, int

    """

    _short_name = "base"

    @classmethod
    def _add_default_params_saving(cls, params):

        params._set_child(
            "saving",
            attribs={"path": None, "how": "ask", "postfix": cls._short_name},
            doc="""Saving of the results.

- path : None or str

  Path of the directory where the data will be saved. If None, the path is
  obtained from the input path and the parameter `postfix`.

- how : str {'ask'}

  'ask', 'new_dir', 'complete' or 'recompute'.

- postfix : str

  Postfix from which the output file is computed.
""",
        )

        params._set_internal_attr(
            "_value_text",
            json.dumps(
                {
                    "program": "fluidimage",
                    "module": cls.__module__,
                    "class": cls.__name__,
                }
            ),
        )

    def __init__(
        self,
        params=None,
        path_dir_src=None,
        path_dir_result=None,
        logging_level="info",
        nb_max_workers=None,
    ):
        self.params = params
        self.path_dir_src = Path(path_dir_src)
        if path_dir_result is None:
            self._init_path_dir_result(path_dir_src)
        else:
            self.path_dir_result = path_dir_result
        self.logging_level = logging_level
        self.nb_max_workers = nb_max_workers

        self.queues = []
        self.works = []
        self.works_dict = {}
        self.executor = None

    def _init_path_dir_result(self, path_dir_src):
        p_saving = self.params.saving
        self.path_dir_result, self.how_saving = prepare_path_dir_result(
            path_dir_src, p_saving.path, p_saving.postfix, p_saving.how
        )
        p_saving.path = self.path_dir_result

    def add_queue(self, name: str, kind: str = None):
        """Create a new queue."""
        if kind == "list":
            queue = QueueList(name)
        else:
            queue = Queue(name=name, kind=kind)
        self.queues.append(queue)
        return queue

    def add_work(
        self,
        name: str,
        func_or_cls,
        params_cls=None,
        input_queue=None,
        output_queue=None,
        kind: str = None,
    ):
        """Create a new work relating queues."""
        if func_or_cls is None:
            warn(f'func_or_cls is None for work "{name}"')

        work = Work(
            name=name,
            input_queue=input_queue,
            func_or_cls=func_or_cls,
            params_cls=params_cls,
            output_queue=output_queue,
            kind=kind,
        )
        self.works.append(work)

        if name in self.works_dict:
            raise ValueError(f"The name {name} is already used.")
        self.works_dict[name] = work

    def compute(
        self,
        executor=None,
        nb_max_workers=None,
        sleep_time=0.01,
        sequential=False,
        stop_if_error=False,
        kwargs_executor=None,
    ):
        """Compute (run the works until all queues are empty).

        Parameters
        ----------

        executor : str or fluidimage.executors.base.ExecutorBase, optional

          If None, ``executor="multi_exec_async"``

        nb_max_workers : int, optional

        sleep_time : number, optional {0.01}

        sequential : bool, optional {False}

        stop_if_error : bool, optional {False}

        """

        if sequential:
            if executor is not None and executor != "exec_sequential":
                raise ValueError(
                    "Incompatible arguments sequential=True and "
                    f"executor={executor}"
                )
            executor = "exec_sequential"

        if executor is None:
            # fastest and safest executor for most cases
            # "multi_exec_async" on Linux
            # "multi_exec_subproc" elsewhere
            executor = supported_multi_executors[0]

        if not isinstance(executor, ExecutorBase):
            if executor not in get_executor_names():
                raise NotImplementedError(f"executor {executor} does not exist")

            if nb_max_workers is None:
                nb_max_workers = self.nb_max_workers

            if kwargs_executor is None:
                kwargs_executor = {}

            exec_class = import_executor_class(executor)
            self.executor = exec_class(
                self,
                path_dir_result=self.path_dir_result,
                nb_max_workers=nb_max_workers,
                sleep_time=sleep_time,
                logging_level=self.logging_level,
                stop_if_error=stop_if_error,
                **kwargs_executor,
            )

        self.executor.compute()

    def make_text_at_exit(self, time_since_start):
        """Make a text printed before exit."""
        txt = f"Stop compute after t = {time_since_start:.2f} s"
        try:
            nb_results = len(self.results)
        except AttributeError:
            nb_results = None
        if nb_results is not None and nb_results > 0:
            txt += f" ({nb_results} results, {time_since_start / nb_results:.2f} s/result)."
        else:
            txt += "."

        if hasattr(self, "path_dir_result"):
            txt += f"\npath results:\n{Path(self.path_dir_result).absolute()}\n"
        return txt

    def print_at_exit(self, time_since_start):
        """Print information before exit."""
        print(self.make_text_at_exit(time_since_start))

    def make_code_graphviz(self, name_file="tmp.dot"):
        """Generate the graphviz / dot code.

        This method only generates a graphviz code. The graph can be visualized
        with for example::

          dot {name_file}.dot -Tpng -o {name_file}.png && eog {name_file}.png

        """
        name_file = str(name_file)

        if name_file.endswith(".dot"):
            name_file = name_file[:-4]

        code = "digraph {\nrankdir = LR\ncompound=true\n"
        # waiting queues
        code += '\nnode [shape="record"]\n'
        txt_queue = (
            '{name_quoted:40s} [label="<f0> {name}|'
            + "|".join([f"<f{i}>" for i in range(1, 5)])
            + '"]\n'
        )

        for queue in self.queues:
            name_quoted = f'"{queue.name}"'
            code += txt_queue.format(name=queue.name, name_quoted=name_quoted)

        # works and links
        code += '\nnode [shape="ellipse"]\n'

        txt_work = '{:40s} [label="{}",color = "{}"]\n'

        for work in self.works:
            name_work = work.name
            color = "Black"
            if work.kind is not None:
                if "io" in work.kind:
                    color = "Green"
            code += txt_work.format(f'"{name_work}"', name_work, color)

        code += "\n"

        str_link = (
            '{:40s} -> "{}" [arrowhead = "{}", style = "{}", color = "{}"]\n'
        )

        for work in self.works:
            name_work = work.name
            arrowhead = "normal"
            style = "dashed"
            color = "Black"
            if work.kind is not None:
                if "one shot" in work.kind:
                    style = "filled"
                if "global" in work.kind:
                    arrowhead = "odiamond"
                if "io" in work.kind:
                    color = "Green"
            if work.input_queue is not None:
                queues = work.input_queue
                if isinstance(queues, Queue):
                    queues = (queues,)
                for queue in queues:
                    code += str_link.format(
                        '"' + queue.name + '"', name_work, arrowhead, style, color
                    )
            if work.output_queue is not None:
                queues = work.output_queue
                if isinstance(queues, Queue):
                    queues = (queues,)
                for queue in queues:
                    code += str_link.format(
                        '"' + name_work + '"', queue.name, arrowhead, style, color
                    )

        # Legend
        code += "\n subgraph cluster_01 {"
        code += '\n node [height="0px", width="0px",shape=none,];'
        code += "\n edge [ minlen = 1,];"
        code += '\n label = "Legend";'
        code += '\n key [label=<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">'
        code += '\n <tr><td align="right" port="i1">Global</td></tr>'
        code += '\n <tr><td align="right" port="i2">One Shot</td></tr>'
        code += '\n <tr><td align="right" port="i3">Multiple Shot</td></tr>'
        code += '\n <tr><td align="right" port="i4">I/O</td></tr>'
        code += "\n </table>>]"
        code += '\n key2 [label=<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">'
        code += '\n<tr><td port="i1">&nbsp;</td></tr>'
        code += '\n<tr><td port="i2">&nbsp;</td></tr>'
        code += '\n<tr><td port="i3">&nbsp;</td></tr>'
        code += '\n<tr><td port="i4">&nbsp;</td></tr>'
        code += "\n </table>>]"
        code += '\n  key:i1:e -> key2:i1:w [arrowhead = "odiamond"]'
        code += '\n  key:i2:e -> key2:i2:w [arrowhead = "none"]'
        code += '\n  key:i3:e -> key2:i3:w [style = "dashed", arrowhead = "none"]'
        code += '\n  key:i4:e -> key2:i4:w [arrowhead = "none", color="Green"]'
        code += "\n } \n"

        code += "}\n"

        with open(name_file + ".dot", "w", encoding="utf-8") as file:
            file.write(code)

        print(
            "A graph can be produced with graphviz with one of these commands:\n"
            f"dot {name_file}.dot -Tpng -o {name_file}.png && eog {name_file}.png\n"
            f"dot {name_file}.dot -Tx11"
        )

    def read_log_data(self, path=None):
        """Create and return an object containing the data from the log file(s)"""
        from fluidimage.topologies.log import LogTopology

        if path is None:
            path = self.path_dir_result

        return LogTopology(path)


class TopologyBaseFromSeries(TopologyBase, ABC):

    series: SeriesOfArrays
    how_saving: str
    params: ParamContainer

    _message_empty_series = "encountered empty series. No images to preprocess."

    @abstractmethod
    def compute_indices_to_be_computed(self):
        """Compute the indices corresponding to the series to be computed"""

    def init_series(self):
        """Initializes the SeriesOfArrays object `self.series` based on input
        parameters."""
        series = self.series
        if not series:
            logger.warning(self._message_empty_series)
            return

        if self.how_saving in ("complete", "from_path_indices"):
            if self.how_saving == "complete":
                index_series = self.compute_indices_to_be_computed()
            elif self.how_saving == "from_path_indices":
                path_indices = self.params.series.path_indices_file
                index_series = [
                    int(line) for line in open(path_indices, encoding="utf-8")
                ]
            series.set_index_series(index_series)
            if self.how_saving == "complete" and not index_series:
                logger.warning(
                    'topology in mode "complete" and work already done.'
                )
                return
            if logger.isEnabledFor(DEBUG):
                logger.debug(repr([serie.get_name_arrays() for serie in series]))

        nb_series = len(series)
        if nb_series == 1:
            plural = ""
        else:
            plural = "s"

        logger.info("Add %s image serie%s to compute.", nb_series, plural)


def _tuple_ints_from_str(line):
    return tuple(int(c.strip()) for c in line.strip()[1:-1].split(",") if c)


class TopologyBaseFromImages(TopologyBase):

    serie: SerieOfArraysFromFiles
    how_saving: str
    path_dir_src: Path
    params: ParamContainer

    def _get_name_result_from_name(self, name):
        return name

    def compute_indices_to_be_computed(self):
        """Compute the indices corresponding to the images to be computed"""
        indices_images = []
        for indices in self.serie.iter_indices():
            name = self.serie.compute_name_from_indices(*indices)
            path_im_output = (
                self.path_dir_result / self._get_name_result_from_name(name)
            )
            if path_im_output.exists():
                continue
            indices_images.append(indices)
        self._fix_indices_images(indices_images)
        return indices_images

    def _fix_indices_images(self, indices_images):
        """Fix the indices images in fill_queue_paths"""

    def fill_queue_paths(self, input_queue, output_queue):
        """Fill the first queue (paths)"""
        assert input_queue is None

        serie = self.serie
        if not serie:
            logger.warning("add 0 image. No image to process.")
            return

        if self.how_saving == "complete":
            indices_images = self.compute_indices_to_be_computed()
        elif self.how_saving == "from_path_indices":
            path_indices = self.params.images.path_indices_file
            indices_images = [
                _tuple_ints_from_str(line)
                for line in open(path_indices, encoding="utf-8")
            ]
        else:
            indices_images = list(serie.iter_indices())
            self._fix_indices_images(indices_images)

        if not indices_images:
            if self.how_saving == "complete":
                logger.warning(
                    'topology in mode "complete" and work already done.'
                )
            else:
                logger.warning("Nothing to do")
            return

        names = []
        for indices in indices_images:
            name = serie.compute_name_from_indices(*indices)
            names.append(name)
            path_im_input = str(self.path_dir_src / name)
            output_queue[name] = path_im_input

        nb_names = len(names)
        logger.info("Add %s images to compute.", nb_names)
        logger.info("First files to process: %s", names[:4])

        logger.debug("All files: %s", names)
