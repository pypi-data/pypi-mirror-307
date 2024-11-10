# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestSimCrossSections(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing cross section calculation with discretized simulation...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        eps_env = 1.33
        mat_env = tg.materials.MatConstant(eps_env)
        env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - illumination field(s)
        wavelengths = torch.linspace(500, 800, 5)
        e_inc_list = [
            tg.env.freespace_3d.PlaneWave(e0p=1.0, e0s=0.6, inc_angle=torch.pi),
        ]

        # - structure
        step = 20.0
        mat_struct = tg.materials.MatConstant(eps=7.0 + 0.15j)
        struct1 = tg.struct.StructDiscretizedCubic3D(
            tg.struct.volume.cuboid(l=2, w=4, h=3), step, mat_struct
        )

        self.sim = tg.simulation.Simulation(
            structures=[struct1],
            environment=env,
            illumination_fields=e_inc_list,
            wavelengths=wavelengths,
        )

    def test_calculate_cs_spectra(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            # calculate spectra and compare with reference

            # via private API
            spec_ext_private = tg.tools.batch.calc_spectrum(
                self.sim, tg.postproc.crosssect.ecs, progress_bar=False
            )["ecs"].squeeze()
            spec_abs_private = tg.tools.batch.calc_spectrum(
                self.sim, tg.postproc.crosssect.acs, progress_bar=False
            )["acs"].squeeze()

            # via public API
            res_full = tg.tools.batch.calc_spectrum(
                self.sim, tg.postproc.crosssect.total, progress_bar=False
            )
            spec_scs = res_full["scs"].squeeze()
            spec_ext = res_full["ecs"].squeeze()
            spec_abs = res_full["acs"].squeeze()

            # print(spec_ext)
            # print(spec_scs)
            # print(spec_abs)

            # compare to pre-calculated reference
            spec_ext_truth = torch.as_tensor(
               [453.8657837, 279.2537231, 187.5266266, 134.9423523, 102.5867004],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )
            spec_scs_truth = torch.as_tensor(
                [380.5903320, 213.5857544, 128.9793243,  82.4661942,  55.1847038],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )
            spec_abs_truth = torch.as_tensor(
                [73.2754517, 65.6679688, 58.5473061, 52.4761581, 47.4019966],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )

            torch.testing.assert_close(spec_ext, spec_ext_truth, rtol=1e-3, atol=1e-3)
            torch.testing.assert_close(spec_scs, spec_scs_truth, rtol=1e-3, atol=1e-3)
            torch.testing.assert_close(spec_abs, spec_abs_truth, rtol=1e-3, atol=1e-3)

            # the individual functions must yield same result as the combined `scattering` function
            torch.testing.assert_close(spec_ext_private, spec_ext)
            torch.testing.assert_close(spec_abs_private, spec_abs)

            if self.verbose:
                print(
                    "  - {}: cross-section spectra (extinct./abs./scat.) test passed.".format(
                        device
                    )
                )


# %%

# %%
if __name__ == "__main__":
    print("testing cross section calculation...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
