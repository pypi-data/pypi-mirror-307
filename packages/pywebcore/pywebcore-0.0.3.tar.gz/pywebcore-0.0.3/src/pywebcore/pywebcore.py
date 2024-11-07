from collections import namedtuple
from itertools import pairwise

import math

import shapely as shp
import sectionproperties.pre as sppre
from sectionproperties import analysis as spana

CoordinateSystem = namedtuple("CoordinateSystem", "name u v")
SectionMaterial = namedtuple("SectionMaterial", "name elastic_modulus poissons_ratio shear_modulus yield_strength density color")

HORIZONTAL = CoordinateSystem('horizontal', u=(1, 0, 0), v=(0, 1, 0))
VERTICAL = CoordinateSystem('vertical', u=(1, 0, 0), v=(0, 0, 1))

class Point:
    __index = 0

    def __init__(self, y, z, index=None):
        self.y = y
        self.z = z
        if index is None:
            self.index = Point.__index
            Point.__index += 1
        else:
            self.index = index

    @staticmethod
    def reset_index():
        Point.__index = 0

    @property
    def name(self):
        return f"p{self.index}"

    def translate(self, dy, dz):
        return Point(self.y + dy, self.z + dz)

    @property
    def mirror(self):
        return Point(-self.y, self.z)


class Line:
    __index = 0

    def __init__(self, p1, p2, index=None, divs=None):
        self.p1 = p1
        self.p2 = p2
        self.divs = divs

        if index is None:
            self.index = Line.__index
            Line.__index += 1
        else:
            self.index = index

    @staticmethod
    def reset_index():
        Line.__index = 0

    @property
    def name(self):
        return f"l{self.index}"


class PolygonMember:
    def __init__(self, name, material, points, t=None, shear_factor=0, divs=None, orientation=None):
        self.name = name
        self.material = material
        self.points = points
        self.shear_factor = shear_factor
        self.divs = divs
        self.orientation = orientation
        if t is None and hasattr(material, "t"):
            t = material.t
        self.t = t

        p1, p2 = points[0], points[-1]
        if (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2 > 1e-3:
            self.points.append(points[0])

        if divs is None:
            divs = len(self.points) * [None]
        self.lines = [Line(p1, p2, divs=d) for (p1, p2), d in zip(pairwise(self.points), divs)]

        self.A = sum(p1.y * p2.z - p2.y * p1.z
                     for p1, p2
                     in pairwise(self.points)) / 2

        self.z = sum((p1.z + p2.z) * (p1.y * p2.z - p2.y * p1.z) for p1, p2 in pairwise(self.points)) / (
                6 * self.A)

        self.Iy = sum((p1.z ** 2 + p1.z * p2.z + p2.z ** 2) * (p1.y * p2.z - p2.y * p1.z) for p1, p2 in
                      pairwise(self.points)) / 12 - self.A * self.z ** 2

        print("A, z, Iy", self.name, self.A, self.z, self.Iy)
        try:
            self.E = self.material.Ex
        except AttributeError:
            self.E = self.material.E
        try:
            self.G = self.material.Gxy
        except AttributeError:
            self.G = self.material.G
        self.rho = self.material.rho
        self.m = self.rho * self.A
        self.As = self.shear_factor * self.A
        self.l = None if self.t is None else self.A / self.t


class Section:
    def __init__(self, laminates, W, foam=None):
        self.laminates = laminates
        self.foam = foam
        self.W = W

        self.H = 0
        self.z = 0  # neutral axis
        self.EI = 0  # bending stiffness
        self.GA = 0  # shear stiffness
        self.m = 0  # mass (T/mm)

    def create_members(self, element_size=None):
        raise NotImplementedError()

    def create_fea_section(self, meshsize, coarse=True):
        materials = {}
        for member in self.members:
            E = member.material.Ex
            rho = member.material.rho
            sigma = member.material.Sxf
            color = 'black'
            if member.orientation is HORIZONTAL:
                nu = member.material.nuxz
                G = member.material.Gxz
            else:
                nu = member.material.nuxy
                G = member.material.Gxy
            m = SectionMaterial(name=m.name, elastic_modulus=E, poissons_ratio=nu,
                                    shear_modulus=G, yield_strength=sigma, density=rho, color=color)
            materials[member] = m

        geoms = []
        for m in self.members:
            polygon = shp.Polygon([(p.y, p.z) for p in m.points])
            geoms.append(sppre.Geometry(polygon, material=materials[member]))

        geom = sppre.CompoundGeometry(geoms)
        geom.create_mesh(meshsize, coarse=coarse)
        section = spana.Section(geom)
        return section, geom

    def update(self, height=None, element_size=None, stiffness_factor=1.0):
        if height is not None:
            self.H = height
            self.members, self.outline = self.create_members(element_size=element_size)

        sf = stiffness_factor
        self.EA = sum(m.E * sf * m.A for m in self.members)
        self.EAz = sum(m.E * sf * m.A * m.z for m in self.members)
        self.z = self.EAz / self.EA
        self.EI = sum(m.E * sf * (m.Iy + m.A * (m.z - self.z) ** 2) for m in self.members)
        self.GA = sum(m.G * sf * m.As for m in self.members)
        self.m = sum(m.A * m.rho for m in self.members)
        return self

    def get_EI(self, height):
        members = self.create_members(element_size=False)
        z = sum(m.E * m.A * m.z for m in members) / sum(m.E * m.A for m in members)
        EI = sum(m.E * (m.Iy + m.A * z ** 2) for m in members)
        return EI

    def __str__(self):
        return f"<Section z={self.z}, EI={self.EI}>"


class WebcoreBridgeSection(Section):
    def __init__(self, laminates, W, hf, wf, theta, ctc, foam=None, H=None):
        super().__init__(laminates, W, foam)
        for pos in ["top", "bottom", "side", "flange", "web"]:
            if pos not in laminates:
                raise AttributeError(f"A laminate for positin '{pos}' should be defined")
        self.hf = hf
        self.wf = wf
        self.theta = theta
        self.ctc = ctc
        if H is not None:
            self.update(height=H)
    @property
    def width(self):
        return self.W

    @property
    def flange_width(self):
        return self.wf

    @property
    def flange_height(self):
        return self.hf

    @property
    def height(self):
        return self.H

    def get_copy(self):
        copy = WebcoreBridgeSection(laminates=self.laminates, foam=self.foam, W=self.W, hf=self.hf, wf=self.wf,
                                    theta=self.theta, ctc=self.ctc)
        copy.laminates = self.laminates
        return copy

    @property
    def nwebs(self):
        margin = 50
        Wts = self.W - 2 * self.wf
        Wbs = Wts - 2 * (self.H - self.laminates['top'].t - self.laminates['bottom'].t) * math.tan(
            math.radians(self.theta))
        return int((Wbs - margin) / self.ctc) + 1

    @property
    def web_positions(self):
        n, ctc = self.nwebs, self.ctc
        if n % 2 == 1:
            center = [0]
            offset = 0
        else:
            center = []
            offset = ctc / 2

        right = [offset + i * ctc for i in range(math.ceil(n / 2))]
        left = [-y for y in reversed(right)]
        if n % 2 == 1:
            return left + right[1:]
        else:
            return left + center + right

    def create_members(self, element_size=None):  # To generate FE elements, set elements to True
        W, H, wf, hf, theta, ctc = self.W, self.H, self.wf, self.hf, self.theta, self.ctc
        tt, tb, tw = self.laminates['top'].t, self.laminates['bottom'].t, self.laminates['web'].t
        te, tf = self.laminates['side'].t, self.laminates['flange'].t
        s, c, t = math.sin(math.radians(theta)), math.cos(math.radians(theta)), math.tan(math.radians(theta))
        he = H - tf
        hc = H - tb - tt

        Point.reset_index()  # reset point numbering
        Line.reset_index()  # reset point numbering
        # Surface.reset_index()  # reset point numbering
        if hf is None:
            hf = 0

        pA = Point(W / 2, 0)
        pAm = pA.mirror
        pA2 = pA.translate(0, -hf)
        pA2m = pA2.mirror
        pA3 = pA.translate(-tf, 0)
        pA3m = pA3.mirror
        pB = pA.translate(0, -tf)
        pBm = pB.mirror
        pB2 = pA2.translate(-tf, 0)
        pB2m = pB2.mirror
        pB3 = pB.translate(-tf, 0)
        pB3m = pB3.mirror
        pC = pB.translate(-wf, 0)
        pCm = pC.mirror
        pD = pC.translate(-he * t, -he)
        pDm = pD.mirror
        pD2 = pD.translate(tb * t, tb)
        pD2m = pD2.mirror
        pE = pD.translate(-te / c, 0)
        pEm = pE.mirror
        pF = pE.translate(tb * t, tb)
        pFm = pF.mirror
        pG = pF.translate(hc * t, hc)
        pGm = pG.mirror
        pH = Point(W / 2 - wf, 0)
        pHm = pH.mirror

        if hf > 1:
            outline = [pA, pA2, pB2, pB3, pC, pD, pDm, pCm, pB3m, pB2m, pA2m, pAm, pA]
        else:
            outline = [pA, pB, pC, pD, pDm, pCm, pBm, pAm, pA]

        ys, dt = self.web_positions, tw / 2  # left -> right

        def get_core_members():
            left_core = PolygonMember("foam0", self.foam,
                                      [pGm, pFm, Point(ys[0] - dt, -H + tb), Point(ys[0] - dt, -tt)],
                                      shear_factor=1, orientation=VERTICAL)
            center_cores = [PolygonMember(f"foam{i + 1}", self.foam,
                                          [Point(y + dt, -tt), Point(y + dt, -H + tb),
                                           Point(y + ctc - dt, -H + tb), Point(y + ctc - dt, -tt)],
                                          shear_factor=1, orientation=VERTICAL) for i, y in enumerate(ys[:-1])]
            right_core = PolygonMember(f"foam{len(ys)}", self.foam,
                                       [pF, pG, Point(ys[-1] + dt, -tt), Point(ys[-1] + dt, -H + tb)],
                                       shear_factor=1, orientation=VERTICAL)
            return [left_core] + center_cores + [right_core]

        elements = element_size is not None
        if elements:
            hdiv = max(int(H / element_size), 1)  # number of elements in z
            wdiv = max(int(ctc / element_size), 1)  # number of elements in y
        else:
            hdiv, wdiv = 1, 1

        members = []

        # Top skin
        if elements:
            tsweb = [
                PolygonMember(
                    f"tsweb{i + 1}", self.laminates['top'],
                    [Point(y - dt, 0), Point(y - dt, -tt), Point(y + dt, -tt), Point(y + dt, 0)],
                    divs=None, orientation=VERTICAL)
                for i, y in enumerate(ys)
            ]
            members += tsweb

            members.append(PolygonMember(
                "ts0", self.laminates['top'],
                [pHm, pGm, tsweb[0].points[1], tsweb[0].points[0]],
                divs=[None, wdiv, None, wdiv], orientation=HORIZONTAL))

            members.append(PolygonMember(
                f"ts{len(ys)}", self.laminates['top'],
                [tsweb[-1].points[3], tsweb[-1].points[2], pG, pH],
                divs=[None, wdiv, None, wdiv], orientation=HORIZONTAL))

            members += [
                PolygonMember(
                    f"ts{i + 1}", self.laminates['top'],
                    [tsweb[i].points[3], tsweb[i].points[2], tsweb[i + 1].points[1], tsweb[i + 1].points[0]],
                    divs=[None, wdiv, None, wdiv], orientation=HORIZONTAL)
                for i, y in enumerate(ys[:-1])
            ]
        else:
            members.append(
                PolygonMember("topskin", self.laminates['top'], [pHm, pGm, pG, pH], orientation=HORIZONTAL))

        # Bottom skin
        if elements:
            bsweb = [
                PolygonMember(
                    f"bsweb{i + 1}", self.laminates['bottom'],
                    [Point(y - dt, -H + tb), Point(y - dt, -H), Point(y + dt, -H),
                     Point(y + dt, -H + tb)],
                    divs=None, orientation=HORIZONTAL)
                for i, y in enumerate(ys)
            ]
            members += bsweb

            members.append(PolygonMember(
                "bs0", self.laminates['bottom'],
                [pFm, pEm, bsweb[0].points[1], bsweb[0].points[0]],
                divs=None, orientation=HORIZONTAL))

            members.append(PolygonMember(
                f"bs{len(ys)}", self.laminates['bottom'],
                [bsweb[-1].points[3], bsweb[-1].points[2], pE, pF],
                divs=None, orientation=HORIZONTAL))

            members += [
                PolygonMember(
                    f"bs{i + 1}", self.laminates['bottom'],
                    [bsweb[i].points[3], bsweb[i].points[2], bsweb[i + 1].points[1], bsweb[i + 1].points[0]],
                    divs=[None, wdiv, None, wdiv], orientation=HORIZONTAL)
                for i, y in enumerate(ys[:-1])
            ]
        else:
            members.append(
                PolygonMember("btmskin", self.laminates['bottom'], [pFm, pEm, pE, pF], orientation=HORIZONTAL))

        # Webs
        if elements:
            members += [
                PolygonMember(
                    f"web{i + 1}", self.laminates['web'],
                    [tsweb[i].points[1], bsweb[i].points[0], bsweb[i].points[3], tsweb[i].points[2]],
                    divs=[hdiv, None, hdiv, None],
                    shear_factor=1, orientation=HORIZONTAL
                )
                for i, y in enumerate(ys)
            ]
        else:
            members += [
                PolygonMember(
                    f"web{i + 1}", self.laminates['web'],
                    [Point(y - tw / 2, -tt), Point(y - tw / 2, -H + tb), Point(y + tw / 2, -H + tb),
                     Point(y + tw / 2, -tt)], orientation=VERTICAL
                    # ,
                    # divs=[hdiv, None, hdiv, None],
                    # shear_factor=1
                )
                for i, y in enumerate(ys)
            ]

        # Edges
        if elements:
            members += [
                PolygonMember("sideright", self.laminates['side'], [pC, pG, pF, pD2], shear_factor=c,
                              divs=[None, hdiv, None, hdiv], orientation=VERTICAL),
                PolygonMember("sideleft", self.laminates['side'], [pD2m, pFm, pGm, pCm], shear_factor=c,
                              divs=[None, hdiv, None, hdiv], orientation=VERTICAL),
                PolygonMember("sidertop", self.laminates['side'], [pH, pG, pC], divs=None, orientation=VERTICAL),
                PolygonMember("sideltop", self.laminates['side'], [pCm, pGm, pHm], divs=None, orientation=VERTICAL),
                PolygonMember("siderbtm", self.laminates['side'], [pD2, pF, pE, pD], divs=None, orientation=VERTICAL),
                PolygonMember("sidelbtm", self.laminates['side'], [pDm, pEm, pFm, pD2m], divs=None,
                              orientation=VERTICAL),
            ]
        else:
            members += [
                PolygonMember("sideright", self.laminates['side'], [pG, pF, pE, pD, pC, pH], shear_factor=c,
                              orientation=VERTICAL),
                PolygonMember("sideleft", self.laminates['side'], [pHm, pCm, pDm, pEm, pFm, pGm], shear_factor=c,
                              orientation=VERTICAL)
            ]

        # Horizontal flanges
        members += [
            PolygonMember("hfright", self.laminates['flange'], [pH, pC, pB3, pA3], divs=[None, wdiv, None, wdiv],
                          orientation=HORIZONTAL),
            PolygonMember("hfleft", self.laminates['flange'], [pA3m, pB3m, pCm, pHm], divs=[None, wdiv, None, wdiv],
                          orientation=HORIZONTAL),
            PolygonMember("hfrcorner", self.laminates['flange'], [pA3, pB3, pB, pA], divs=None, orientation=HORIZONTAL),
            PolygonMember("hflcorner", self.laminates['flange'], [pAm, pBm, pB3m, pA3m], divs=None,
                          orientation=HORIZONTAL),

        ]

        # Vertical flanges
        if hf > 1:
            members += [
                PolygonMember("vfright", self.laminates['flange'], [pB, pB3, pB2, pA2], shear_factor=1,
                              divs=[None, hdiv, None, hdiv], orientation=VERTICAL),
                PolygonMember("vfleft", self.laminates['flange'], [pA2m, pB2m, pB3m, pBm], shear_factor=1,
                              divs=[None, hdiv, None, hdiv], orientation=VERTICAL)
            ]

        return members, outline
