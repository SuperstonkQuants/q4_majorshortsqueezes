from q4_majorshortsqueezes.filter import (
    RingbufferWithAutomaticFIFORemoval,
    SortedFIFOCache,
)


class TestRingbufferWithAutomaticFIFORemoval:
    def test_enqueue(self):
        size = 3
        buffer = RingbufferWithAutomaticFIFORemoval[int](size=size)

        # First returned items are always None:
        for i in range(0, size):
            removed = buffer.enqueue(i)
            assert removed is None

        # Afterwards, elements are removed according to FIFO:
        for i in range(0, size):
            removed = buffer.enqueue(i + 10)
            assert removed == i


class TestSortedFIFOCache:
    def test_add(self):
        size = 3
        cache = SortedFIFOCache(size=size, sort_key_func=lambda x: x)

        cache.add(1)
        assert cache.get_first() == 1
        cache.add(2)
        assert cache.get_first() == 1
        cache.add(3)
        assert cache.get_first() == 1
        # Now 1 should be removed and 2 is the next value based on asc order
        cache.add(4)
        assert cache.get_first() == 2
        cache.add(5)
        assert cache.get_first() == 3

    def test_get_first_return_none_when_cache_empty(self):
        cache = SortedFIFOCache(size=1, sort_key_func=lambda x: x)
        assert cache.get_first() is None
