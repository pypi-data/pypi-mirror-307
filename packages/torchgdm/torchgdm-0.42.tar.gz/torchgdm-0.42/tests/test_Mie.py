# encoding=utf-8
# %%
import unittest
import warnings

import torch

import torchgdm as tg


class TestDimensionMatching(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing Mie polarizabilities simulation...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # setup test cases
        self.test_cases = [
            dict(
                wl=700.0,
                radii=[80, 80],
                materials=[16, 16],
                eps_env=1.0,
            ),
            dict(
                wl=900.0,
                radii=[50, 70],
                materials=[12.0 + 0.1j, 9.0],
                eps_env=1.3**2,
            ),
            dict(
                wl=500.0,
                radii=[30, 30],
                materials=[-16.0959 + 0.4438j, -16.0959 + 0.4438j],
                eps_env=1.0,
            ),
            dict(
                wl=600.0,
                radii=[50, 70],
                materials=[-16.0959 + 0.4438j, 16],
                eps_env=1.0,
            ),
            dict(
                wl=650.0,
                radii=[70, 90],
                materials=[9.0, -16.0959 + 0.4438j],
                eps_env=1.5,
            ),
        ]

    def test_calculate_E_H(self):
        import numpy as np

        # try importing external packages
        try:
            # ignore import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import pymiecs
        except ModuleNotFoundError:
            if self.verbose:
                print(
                    "Mie tests require package `pymiecs`. "
                    + "Please install via `pip install pymiecs`."
                )
            return
        try:
            # ignore import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import treams
        except ModuleNotFoundError:
            if self.verbose:
                print(
                    "Mie tests require package `treams`. "
                    + "Please install via `pip install treams`."
                )
            return

        # - the actual test
        for device in self.devices:
            # ignore warnings temporarily:
            warnings.simplefilter("ignore")
            for conf in self.test_cases:
                wl = conf["wl"]
                k0 = 2 * np.pi / wl
                radii = conf["radii"]
                materials = conf["materials"]
                eps_env = conf["eps_env"]

                # external Mie toolkit
                res_mie = pymiecs.main.Q(
                    tg.to_np(k0),
                    r_core=radii[0],
                    n_core=materials[0] ** 0.5,
                    r_shell=radii[1],
                    n_shell=materials[1] ** 0.5,
                    n_max=1,
                    n_env=tg.to_np(eps_env)**0.5,
                )
                ecs_mie = res_mie["cs_geo"] * res_mie["qext"]
                scs_mie = res_mie["cs_geo"] * res_mie["qsca"]

                # torchGDM using treams-Mie
                env = tg.env.EnvHomogeneous3D(eps_env)
                struct_mie = tg.struct.StructMieSphereEffPola3D(
                    wavelengths=wl, environment=env, radii=radii, materials=materials
                )
                e_inc = tg.env.freespace_3d.PlaneWave()
                sim_tg_mie = tg.Simulation(
                    structures=struct_mie,
                    environment=env,
                    illumination_fields=e_inc,
                    wavelengths=wl,
                    device=device,
                )
                sim_tg_mie.run(verbose=False, progress_bar=False)
                cs_a_mie = sim_tg_mie.get_crosssections(progress_bar=False)

                # test if results match
                np.testing.assert_allclose(
                    ecs_mie[0], tg.to_np(cs_a_mie["ecs"][0]), atol=1e-2, rtol=1e-5
                )
                
                # absorption and thus scattering are not accurate, increase tolerance
                np.testing.assert_allclose(
                    scs_mie[0], tg.to_np(cs_a_mie["scs"][0]), atol=1e-1, rtol=1e-2
                )
                
                if self.verbose:
                    print("  - {}: Mie test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing Mie polarizabilities...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
