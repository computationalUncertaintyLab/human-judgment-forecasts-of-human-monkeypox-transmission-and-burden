#mcandrew

class interpolator(object):
    def __init__(self,xs=None,ys=None,client=None):
        if xs is None or ys is None:
            self.xs = client.xs
            self.ys = cliet.ys
        elif client is None:
            self.xs = xs
            self.ys = ys
        self.buildInterpolator()

    def __call__(self,xs):
        return self.interp(xs)

    def padd(self,x):
        import numpy as np
        eps = np.finfo(float).eps

        x[0]  = x[0]+eps
        x[-1] = x[-1]+eps
        return x
    
    def buildInterpolator(self,kind="linear"):
        from scipy.interpolate import interp1d

        padded_xs = self.padd(self.xs)
        f = interp1d(padded_xs,self.ys,kind=kind)
        self.f = f
        return f

    def interp(self,xs):
        return self.f(xs)

if __name__ == "__main__":
    pass
