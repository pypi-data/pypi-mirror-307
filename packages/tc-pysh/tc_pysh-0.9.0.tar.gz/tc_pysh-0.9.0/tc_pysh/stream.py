from typing import Iterable, Callable, Any
import collections
from itertools import islice
from multiprocessing import Pool


StreamPred = Callable[[Any], bool]


class Stream:
    "A stream of elemnts passing through a pipe of filters and transformations."

    def __init__(self, source: Iterable):
        self.raw_source = source
        self.source = iter(source)

    def __iter__(self):
        return self.source

    def __next__(self):
        return next(self.source)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        if isinstance(self.raw_source, Stream):
            self.raw_source.close()

    def first(self):
        "Return the first element of the stream."
        return next(iter(self), None)

    def last(self):
        "Return the last element of the stream."
        it = None

        for it in self:
            pass

        return it

    def count(self) -> int:
        "Count the remaining elements of the stream. Warning, the stream is exhausted."
        return sum(1 for _ in self)

    def fold(self, folder, seed):
        "Left fold of the collection."
        acc = seed
        for elem in self:
            acc = folder(acc, elem)
        return acc

    def collect(self) -> list:
        "Collect all the elements into a list."
        return list(self)

    def for_each(self, fn) -> None:
        for e in self:
            fn(e)

    def zip(self, other) -> "Stream":
        return Stream(zip(self, other))

    def scan(self, folder, seed) -> "Stream":
        def f():
            acc = seed
            for elem in self:
                acc = folder(acc, elem)
                yield acc

        return Stream(f())

    def tail(self, n=10) -> "Stream":
        "Keep only the last n elements."
        q = collections.deque(self.source, maxlen=n)
        return self.__class__(iter(q))

    def before(self, n=10) -> "Stream":
        "Return an iterator over the last n items"

        def be():
            d = collections.deque(maxlen=n)
            for line in self:
                if len(d) == n:
                    yield d.pop()

                d.appendleft(line)

        return self.__class__(be())

    def filter(self, pred: StreamPred) -> "Stream":
        """Create an arbitrary query filter from a predicate.

        :param pred: keep only the elements for which `pred(elem)` is true.
        """

        def source():
            for e in self:
                if pred(e):
                    yield e

        return self.__class__(source())

    def sort(self, key=None) -> "Stream":
        """Sort the elements of the query.

        :param key: (optional) see :py:func:`sorted`
        """
        return self.__class__(sorted(self, key=key))

    def map(self, fn) -> "Stream":
        def source():
            for e in self:
                yield fn(e)

        return Stream(source())

    def enumerate(self, start=0) -> "Stream":
        def source():
            for i, e in enumerate(self, start=start):
                yield (i, e)

        return Stream(source())

    def islice(self, *args) -> "Stream":
        return self.__class__(islice(self, *args))

    def parallel(self, worker, *, njobs=4, chunksize=8, args=()) -> "Stream":
        """Execute the function `worker` on each element in parallel.

        :param worker: the function to parallelize
        :param njobs: (optional, 4) the number of jobs
        :return: a stream of the results in the same order
        """

        def wrapper():
            "Wrap the iterator to keep the pool alive until all results are consumed"

            def wrapped_worker(e):
                return worker(*args, e)

            with Pool(njobs) as p:
                yield from p.imap(wrapped_worker, self, chunksize=chunksize)

        return Stream(wrapper())

    def parallel_unordered(self, worker, *, njobs=4, chunksize=8, args=()) -> "Stream":
        """Execute the function `worker`  in parallel.

        This variant returns ad

        :param worker: the function to parallelize
        :param njobs: (optional, 4) the number of jobs
        :return: a stream of the results in the same order
        """

        def wrapper():
            "Wrap the iterator to keep the pool alive until all results are consumed"

            with Pool(njobs) as p:
                yield from p.imap_unordered(
                    worker, self.map(lambda e: (*args, e)), chunksize=chunksize
                )

        return Stream(wrapper())


class FuncWrapper:
    def __getattr__(self, name):
        return lambda e: getattr(e, name)()


fn = FuncWrapper()
