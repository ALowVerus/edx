"""
Pre-processing time: nlogn
Storage cost: n^2
Query time: logn
Generally, this is a plane-sweep strategy.
At each point, generate the y-tree of trapezoids for a slab bounded by the next point.
Somehow, you should be able to get O(nlogn) space, despite having O(n^2) trapezoids.
Is he using the trap map trick? Removing unnecessary x-dividers?
"""