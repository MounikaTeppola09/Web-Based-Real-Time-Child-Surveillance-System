import numpy as np

class Detection(object):

    def __init__(self, tlwh, confidence, feature):
        self.tlwh = np.asarray(tlwh, dtype=float)
        self.confidence = float(confidence) 
        self.feature = np.asarray(feature, dtype=np.float32)

    def to_tlbr(self):
        """to bounding box with format (top-left bottom-right)
        Convert bounding box to format (min x, min y, max x, max y)
        """
        ret = self.tlwh.copy()
        ret[2:] += ret[:2]
        return ret

    def to_xyah(self):
        """to bounding box with format (center x, center y, aspect ratio, height)
                                    aspect ratio == `width / height`.
        """
        ret = self.tlwh.copy()
        ret[:2] += ret[2:] / 2
        ret[2] /= ret[3]
        return ret
