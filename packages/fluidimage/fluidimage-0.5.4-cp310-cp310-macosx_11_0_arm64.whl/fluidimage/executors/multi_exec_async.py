"""
Multi executors async
=====================

.. autoclass:: MultiExecutorAsync
   :members:
   :private-members:

"""

import copy
from multiprocessing import Process

from fluidimage.topologies.splitters import split_list

from .base import MultiExecutorBase
from .exec_async_seq_for_multi import ExecutorAsyncSeqForMulti


class MultiExecutorAsync(MultiExecutorBase):
    """Manage the multi-executor mode

     This class is not the one whose really compute the topology. The topology is
     split and each slice is computed with an ExecutorAsync

    Parameters
    ----------

    nb_max_workers : None, int

      Limits the numbers of workers working in the same time.

    nb_items_queue_max : None, int

      Limits the numbers of items that can be in a output_queue.

    sleep_time : None, float

      Defines the waiting time (from trio.sleep) of a function. Async functions
      await `trio.sleep(sleep_time)` when they have done a work on an item, and
      when there is nothing in their input_queue.

    """

    ExecutorForMulti = ExecutorAsyncSeqForMulti

    def _start_processes(self):
        """
        There are two ways to split self.topology work:

        - If first self.topology has "series" attribute (from seriesOfArray), it
          creates "self.nb_max_workers" topologies and changes "ind_start" and
          "ind_stop" of topology.series. The split considers series.ind_step.

        - Else, if the first work of the topology has an unique output_queue, it
          splits that queue in "self.nb_max_worker" slices and create as many
          topologies. On these last, the first work will be removed and the first
          queue will be filled with a partition of the first queue Then create as
          many Executer_await as topologies, give each topology to each executors,
          and call each Executor_await.compute in a process from multiprocessing.

        """
        if hasattr(self.topology, "series"):
            self._start_multiprocess_series()
        else:
            self._start_multiprocess_first_queue()

    def _start_multiprocess_first_queue(self):
        """Start the processes spitting the work with the first queue"""

        keys_for_processes = split_list(self._keys_first_queue, self.nb_processes)

        # change topology
        self.topology.first_queue = self.topology.works[0].output_queue
        topology = copy.copy(self.topology)
        topology.first_queue.clear()
        del topology.works[0]
        old_queue = topology.first_queue

        for idx_process, keys_proc in enumerate(keys_for_processes):
            topology_this_process = copy.copy(self.topology)
            new_queue = copy.copy(topology.first_queue)
            topology_this_process.first_queue = new_queue

            for iq, queue in enumerate(topology_this_process.queues):
                if queue is old_queue:
                    topology_this_process.queues[iq] = new_queue

            for work in topology_this_process.works:
                if work.output_queue is old_queue:
                    work.output_queue = new_queue

                if work.input_queue is old_queue:
                    work.input_queue = new_queue

                if isinstance(work.input_queue, (tuple, list)):
                    work.input_queue = list(work.input_queue)
                    for iq, queue in enumerate(work.input_queue):
                        if queue is old_queue:
                            work.input_queue[iq] = new_queue
                if isinstance(work.output_queue, (tuple, list)):
                    work.output_queue = list(work.output_queue)
                    for iq, queue in enumerate(work.output_queue):
                        if queue is old_queue:
                            work.output_queue[iq] = new_queue

            for key in keys_proc:
                new_queue[key] = self._first_queue[key]

            old_queue = new_queue

            self.launch_process(topology_this_process, idx_process)

    def _start_multiprocess_series(self):
        """Start the processes spitting the work with the series object"""

        try:
            splitter_cls = self.topology.Splitter
        except AttributeError as error:
            raise ValueError(
                "MultiExecutorAsync can only execute "
                "topologies with a Splitter."
            ) from error

        params = copy.deepcopy(self.topology.params)
        splitter = splitter_cls(
            params, self.nb_processes, self.topology, self._indices_to_be_computed
        )
        assert self.num_expected_results == splitter.num_expected_results

        if (
            hasattr(self.topology, "how_saving")
            and self.topology.how_saving == "complete"
            and hasattr(splitter, "save_indices_files")
        ):
            path_dir_indices = (
                self.path_dir_result / f"indices_files_{self._unique_postfix}"
            )
            path_dir_indices.mkdir(exist_ok=True)
            splitter.save_indices_files(path_dir_indices)

            for idx_process, index_series in enumerate(splitter.indices_lists):
                if not index_series:
                    continue
                new_topology = copy.copy(self.topology)
                new_topology.series.set_index_series(index_series)
                self.launch_process(new_topology, idx_process)

        else:
            for idx_process, start_stop_step in enumerate(splitter.ranges):
                if len(range(*start_stop_step)) == 0:
                    continue
                new_topology = copy.copy(self.topology)
                series = new_topology.series
                series.ind_start, series.ind_stop, series.ind_step = (
                    start_stop_step
                )
                self.launch_process(new_topology, idx_process)

    def init_and_compute(self, topology_this_process, log_path, idx_process):
        """Create an executor and start it in a process"""
        executor = self.ExecutorForMulti(
            topology_this_process,
            self.path_dir_result,
            sleep_time=self.sleep_time,
            path_log=log_path,
            logging_level=self.logging_level,
            t_start=self.t_start,
            index_process=idx_process,
        )
        executor.compute()

    def launch_process(self, topology, idx_process):
        """Launch one process"""

        log_path = self._log_path.parent / f"process_{idx_process:03d}.txt"
        self.log_paths.append(log_path)

        process = Process(
            target=self.init_and_compute,
            args=(topology, log_path, idx_process),
        )
        process.daemon = True
        process.start()
        self.processes.append(process)

    def _poll_return_code(self, process):
        return process.exitcode

    def _join_processes(self):
        """Join the processes"""
        for process in self.processes:
            process.join()


Executor = MultiExecutorAsync
