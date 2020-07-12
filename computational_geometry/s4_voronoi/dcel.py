class DCEL:
    class HalfEdge:
        def __init__(self):
            # The corresponding half-edge, on the opposite side & direction
            self.twin = None
            # The point front which the half-edge proceeds
            self.origin = None
            # The face to the left
            self.face = None
            # The line preceding this one along the border of its left face
            self.pred = None
            # The line succeeding this one along the border of its left face
            self.succ = None

    class Vertex:
        def __init__(self, point):
            self.coord = point
            # The first outgoing incident half-edge
            self.inc = None

    class Face:
        def __init__(self):
            # A reference to one of the edges of the face
            self.inc = None
            # A load that can be used for any number of things
            self.load = None

    @classmethod
    def generate_half_edge_pair(cls, phi, rho):
        """
        Return a pair of edges from p0 to p1, with appropriate origin and twinning.
        """
        pr = DCEL.HalfEdge()
        rp = DCEL.HalfEdge()
        pr.twin = rp
        rp.twin = pr
        pr.origin = phi
        rp.origin = rho
        return pr, rp
