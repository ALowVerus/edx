"""
Pre-processing time: nlogn
Storage cost: nlogn
Query time: logn
Using trees and node rotations, you can reduce your storage space to O(n) while increasing search time in O((logn)^2).
Basically: Make a Git-style version controller, where you have an ordered list of all changes to the heirarchy over time.
On each search, find the node status at a given timestamp (logn) for each node (logn) as you traverse the tree.
"""