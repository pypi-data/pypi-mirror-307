# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestSim3DVacuumPlanWave(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing 3D discretized simulation, plane wave illumination...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        eps_env = 1.0
        mat_env = tg.materials.MatConstant(eps_env)
        env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - illumination field(s)
        self.wl = 550.0
        wavelengths = torch.tensor([self.wl])
        e_inc_list = [
            tg.env.freespace_3d.PlaneWave(e0p=1.0, e0s=0.6, inc_angle=torch.pi),
        ]

        # - structure
        step = 25.0
        mat_struct = tg.materials.MatConstant(eps=10.0)
        struct1 = tg.struct.StructDiscretizedCubic3D(
            tg.struct.volume.cuboid(l=3, w=2, h=4),
            step,
            mat_struct,
            radiative_correction=False,
        )

        self.sim = tg.simulation.Simulation(
            structures=[struct1],
            environment=env,
            illumination_fields=e_inc_list,
            wavelengths=wavelengths,
        )

    def test_calculate_E_H(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(calc_missing=True, verbose=False, progress_bar=False)

            # compare random e-field
            E_test = self.sim.fields_inside[self.wl].efield[0][7]
            # print(E_test)
            E_truth = torch.as_tensor(
                [
                    0.13236962 - 0.2889568j,
                    0.04079278 - 0.11384597j,
                    -0.06021021 - 0.00766215j,
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )
            torch.testing.assert_close(E_test, E_truth, rtol=1e-5, atol=0)

            # compare random h-field
            H_test = self.sim.fields_inside[self.wl].hfield[0][2]
            # print(H_test)
            H_truth = torch.as_tensor(
                [
                    0.49382266 - 0.44141245j,
                    -0.8956885 + 0.8145405j,
                    0.05164324 + 0.07042729j,
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )
            torch.testing.assert_close(H_test, H_truth, rtol=1e-5, atol=0)
            if self.verbose:
                print("  - {}: 3D sim E, H field test passed.".format(device))


class TestSim2DVacuumPlanWave(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing 2D discretized simulation, plane wave illumination...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        eps_env = 2.25
        mat_env = tg.materials.MatConstant(eps_env)
        env = tg.env.freespace_2d.EnvHomogeneous2D(env_material=mat_env)

        # - illumination field(s)
        self.wl = 550.0
        wavelengths = torch.tensor([self.wl])
        e_inc_list = [
            tg.env.freespace_2d.PlaneWave(e0p=1.0, e0s=0.6, inc_angle=torch.pi / 3),
        ]

        # - structure
        step = 25.0
        mat_struct = tg.materials.MatConstant(eps=6.0)
        struct1 = tg.struct.StructDiscretizedSquare2D(
            tg.struct.surface_2d.rectangle(l=3, h=2), step, mat_struct
        )

        self.sim = tg.simulation.Simulation(
            structures=[struct1],
            environment=env,
            illumination_fields=e_inc_list,
            wavelengths=wavelengths,
        )

    def test_calculate_E_H(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(calc_missing=True, verbose=False, progress_bar=False)

            # compare random e-field
            E_test = self.sim.fields_inside[self.wl].efield[0][3]
            # print(E_test)
            E_truth = torch.as_tensor(
                [
                    -0.2927338 - 0.2186406j,
                    0.5191928 + 0.5264899j,
                    -0.4140966 - 0.1886911j,
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )
            torch.testing.assert_close(E_test, E_truth, rtol=1e-2, atol=1e-5)

            # compare random h-field
            H_test = self.sim.fields_inside[self.wl].hfield[0][4]
            # print(H_test)
            H_truth = torch.as_tensor(
                [
                    -0.5955392 + 0.2554660j,
                    -1.6774530 + 0.6361306j,
                    -1.0642812 + 0.3601927j,
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )
            torch.testing.assert_close(H_test, H_truth, rtol=1e-2, atol=1e-5)
            if self.verbose:
                print("  - {}: 2D sim E, H field test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing discretization simulation...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
