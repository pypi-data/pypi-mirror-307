# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestGlobalSizeScaling(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing global size scaling invariance...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        self.scale_factors = [1.0, 1.5]

        # --- setup a test case
        # - materials
        self.mat_struct = tg.materials.MatConstant(eps=16)
        self.mat_env = tg.materials.MatConstant(eps=1.33)
        # - environment
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=self.mat_env)

        # - illumination field(s)
        self.plane_wave = tg.env.freespace_3d.PlaneWave(e0p=0.7, e0s=-0.5)

    def test_calculate_E_H(self):
        for device in self.devices:
            Q_sc = []
            Q_ex = []
            for scale in self.scale_factors:

                # scale wavelengths
                wavelengths = torch.linspace(550.0, 750.0, 3) * scale

                # scale geometry
                step = 20 * scale
                structure = tg.struct.StructDiscretizedCubic3D(
                    tg.struct.volume.cube(l=150 * scale / step), step, self.mat_struct
                )
                cs_geo = tg.tools.geometry.get_geometric_crosssection(structure)

                # - define and run simulation
                sim = tg.Simulation(
                    structures=[structure],
                    illumination_fields=[self.plane_wave],
                    environment=self.env,
                    wavelengths=wavelengths,
                    device=device,
                )
                sim.run(verbose=False, progress_bar=False)
                cs_results = tg.tools.batch.calc_spectrum(
                    sim, tg.postproc.crosssect.total, progress_bar=False
                )
                Q_sc.append(cs_results["scs"] / cs_geo)
                Q_ex.append(cs_results["ecs"] / cs_geo)

            torch.testing.assert_close(Q_sc[0], Q_sc[1], rtol=1e-3, atol=0.01)
            torch.testing.assert_close(Q_ex[0], Q_ex[1], rtol=1e-3, atol=0.01)
            if self.verbose:
                print("  - {}: scaling test passed.".format(device))


class TestGlobalWavelengthAndMaterialScaling(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing global wavelength / material scaling invariance...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # test case
        # test case setup
        self.r_sphere = 80.0  # nm
        self.step = 25.0

        self.n_environment = 1.3
        self.n_sphere = 4.0

        # set up environments and structures with non-vacuum environment and
        # an equivalent case which instead uses the scaling n=n/n_env and
        # wavelength=wavelength/n_env
        self.n_env1 = self.n_environment
        self.n_sph1 = self.n_sphere
        self.wls1 = torch.linspace(600.0, 800.0, 3)
        self.r_probe = tg.tools.geometry.coordinate_map_2d_square(
            500, 15, r3=0, delta2=750
        )

        self.n_env2 = 1.0
        self.n_sph2 = self.n_sphere / self.n_environment
        self.wls2 = self.wls1 / self.n_environment

        self.mat_env1 = tg.materials.MatConstant(self.n_env1**2)
        self.mat_env2 = tg.materials.MatConstant(self.n_env2**2)
        self.env1 = tg.env.freespace_3d.EnvHomogeneous3D(env_material=self.mat_env1)
        self.env2 = tg.env.freespace_3d.EnvHomogeneous3D(env_material=self.mat_env2)

        # - illumination field
        self.e_inc = tg.env.freespace_3d.PlaneWave(e0p=1, e0s=0)

        # - test-structure: sphere
        self.mat1 = tg.materials.MatConstant(eps=self.n_sph1**2)
        self.s_mesh1 = tg.struct.volume.StructDiscretizedCubic3D(
            tg.struct.volume.geometries.sphere(self.r_sphere / self.step),
            self.step,
            self.mat1,
        )
        self.s_mesh1.set_center_of_mass([0, 0, 0])

        self.mat2 = tg.materials.MatConstant(eps=self.n_sph2**2)
        self.s_mesh2 = tg.struct.volume.StructDiscretizedCubic3D(
            tg.struct.volume.geometries.sphere(self.r_sphere / self.step),
            self.step,
            self.mat2,
        )
        self.s_mesh2.set_center_of_mass([0, 0, 0])

    def test_full_sim(self):
        for device in self.devices:
            # test polarizabilities
            self.s_mesh1.set_device(device)
            self.s_mesh2.set_device(device)
            for i_wl in range(len(self.wls1)):
                a_m1 = self.s_mesh1.get_polarizability_6x6(self.wls1[i_wl], self.env1)
                a_m2 = self.s_mesh2.get_polarizability_6x6(self.wls2[i_wl], self.env2)
                torch.testing.assert_close(
                    ((a_m1[0, 0, 0] / a_m2[0, 0, 0]) ** 0.5).real,
                    torch.as_tensor(self.n_environment, device=a_m1.device),
                )
                torch.testing.assert_close(
                    ((a_m1[0, 0, 0] / a_m2[0, 0, 0]) ** 0.5).imag,
                    torch.as_tensor(0.0, device=a_m1.device),
                )

            # test sim. results
            sim_f1 = tg.Simulation(
                structures=[self.s_mesh1],
                environment=self.env1,
                illumination_fields=self.e_inc,
                wavelengths=self.wls1,
            )
            sim_f1.run(verbose=False, progress_bar=False)
            sim_f2 = tg.Simulation(
                structures=[self.s_mesh2],
                environment=self.env2,
                illumination_fields=self.e_inc,
                wavelengths=self.wls2,
            )
            sim_f2.run(verbose=False, progress_bar=False)

            # test cross sections
            cs_1 = sim_f1.get_crosssections(progress_bar=False)
            cs_2 = sim_f2.get_crosssections(progress_bar=False)

            torch.testing.assert_close(cs_1["ecs"], cs_2["ecs"], atol=10, rtol=1e-5)
            torch.testing.assert_close(cs_1["acs"], cs_2["acs"], atol=10, rtol=1e-5)
            torch.testing.assert_close(cs_1["scs"], cs_2["scs"], atol=10, rtol=1e-5)

            # test fields
            for i_wl in range(len(self.wls1)):
                nf1 = sim_f1.get_nearfield(
                    self.wls1[i_wl], r_probe=self.r_probe, progress_bar=False
                )
                nf2 = sim_f2.get_nearfield(
                    self.wls2[i_wl], r_probe=self.r_probe, progress_bar=False
                )

                for which in ["sca", "tot", "inc"]:
                    torch.testing.assert_close(
                        nf1[which].get_efield(),
                        nf2[which].get_efield(),
                        atol=0.001,
                        rtol=1e-4,
                    )
                    torch.testing.assert_close(
                        nf1[which].get_hfield(),
                        nf2[which].get_hfield() * self.n_environment,
                        atol=0.001,
                        rtol=1e-4,
                    )

            if self.verbose:
                print(
                    "  - {}: full sim environment index scaling test passed.".format(
                        device
                    )
                )

    def test_eff_pola(self):
        for device in self.devices:
            # eff. pola model
            self.s_mesh1.set_device(device)
            self.s_mesh2.set_device(device)
            self.s_eff1 = self.s_mesh1.convert_to_effective_polarizability_pair(
                environment=self.env1,
                wavelengths=self.wls1,
                progress_bar=False,
                verbose=False,
            )
            self.s_eff2 = self.s_mesh2.convert_to_effective_polarizability_pair(
                environment=self.env2,
                wavelengths=self.wls2,
                progress_bar=False,
                verbose=False,
            )

            # test polarizabilities
            torch.testing.assert_close(
                self.s_eff1.alpha_data[..., 0, 0],
                self.s_eff2.alpha_data[..., 0, 0] * self.n_environment**2,
                atol=10,
                rtol=1e-5,
            )
            torch.testing.assert_close(
                self.s_eff1.alpha_data[..., 3, 3],
                self.s_eff2.alpha_data[..., 3, 3] * self.n_environment,
                atol=10,
                rtol=1e-5,
            )

            # test sim. results
            sim_eff1 = tg.Simulation(
                structures=[self.s_eff1],
                environment=self.env1,
                illumination_fields=self.e_inc,
                wavelengths=self.wls1,
            )
            sim_eff1.run(verbose=False, progress_bar=False)
            sim_eff2 = tg.Simulation(
                structures=[self.s_eff2],
                environment=self.env2,
                illumination_fields=self.e_inc,
                wavelengths=self.wls2,
            )
            sim_eff2.run(verbose=False, progress_bar=False)

            # test cross sections
            cs_a1 = sim_eff1.get_crosssections(progress_bar=False)
            cs_a2 = sim_eff2.get_crosssections(progress_bar=False)

            torch.testing.assert_close(cs_a1["ecs"], cs_a2["ecs"], atol=10, rtol=1e-5)
            torch.testing.assert_close(cs_a1["scs"], cs_a2["scs"], atol=1000, rtol=1e-2)

            # test fields
            for i_wl in range(len(self.wls1)):
                nf_eff1 = sim_eff1.get_nearfield(
                    self.wls1[i_wl], r_probe=self.r_probe, progress_bar=False
                )
                nf_eff2 = sim_eff2.get_nearfield(
                    self.wls2[i_wl], r_probe=self.r_probe, progress_bar=False
                )

                for which in ["sca", "tot", "inc"]:
                    torch.testing.assert_close(
                        nf_eff1[which].get_efield(),
                        nf_eff2[which].get_efield(),
                        atol=0.1,
                        rtol=1e-1,
                    )
                    torch.testing.assert_close(
                        nf_eff1[which].get_hfield(),
                        nf_eff2[which].get_hfield() * self.n_environment,
                        atol=0.1,
                        rtol=1e-1,
                    )

            if self.verbose:
                print(
                    "  - {}: effective polarizabilities env. index scaling test passed.".format(
                        device
                    )
                )

    def test_mie_pola(self):
        for device in self.devices:
            # Mie eff. pola
            self.r_sphere_mie = self.r_sphere

            self.s_mie1 = tg.struct.StructMieSphereEffPola3D(
                wavelengths=self.wls1,
                environment=self.env1,
                radii=self.r_sphere_mie,
                materials=self.mat1,
                device=device,
            )

            self.s_mie2 = tg.struct.StructMieSphereEffPola3D(
                wavelengths=self.wls2,
                environment=self.env2,
                radii=self.r_sphere_mie,
                materials=self.mat2,
                device=device,
            )

            # test polarizabilities
            torch.testing.assert_close(
                self.s_mie1.alpha_data[..., 0, 0],
                self.s_mie2.alpha_data[..., 0, 0] * self.n_environment**2,
                atol=10,
                rtol=1e-5,
            )
            torch.testing.assert_close(
                self.s_mie1.alpha_data[..., 3, 3],
                self.s_mie2.alpha_data[..., 3, 3] * self.n_environment,
                atol=10,
                rtol=1e-5,
            )

            # test sim. results
            sim_mie1 = tg.Simulation(
                structures=[self.s_mie1],
                environment=self.env1,
                illumination_fields=self.e_inc,
                wavelengths=self.wls1,
            )
            sim_mie1.run(verbose=False, progress_bar=False)
            sim_mie2 = tg.Simulation(
                structures=[self.s_mie2],
                environment=self.env2,
                illumination_fields=self.e_inc,
                wavelengths=self.wls2,
            )
            sim_mie2.run(verbose=False, progress_bar=False)

            # test cross sections
            cs_mie1 = sim_mie1.get_crosssections(progress_bar=False)
            cs_mie2 = sim_mie2.get_crosssections(progress_bar=False)

            torch.testing.assert_close(
                cs_mie1["ecs"], cs_mie2["ecs"], atol=10, rtol=1e-5
            )
            torch.testing.assert_close(
                cs_mie1["scs"], cs_mie2["scs"], atol=1000, rtol=1e-2
            )

            # test fields
            for i_wl in range(len(self.wls1)):
                nf_mie1 = sim_mie1.get_nearfield(
                    self.wls1[i_wl], r_probe=self.r_probe, progress_bar=False
                )
                nf_mie2 = sim_mie2.get_nearfield(
                    self.wls2[i_wl], r_probe=self.r_probe, progress_bar=False
                )

                for which in ["sca", "tot", "inc"]:
                    torch.testing.assert_close(
                        nf_mie1[which].get_efield(),
                        nf_mie2[which].get_efield(),
                        atol=0.1,
                        rtol=1e-1,
                    )
                    torch.testing.assert_close(
                        nf_mie1[which].get_hfield(),
                        nf_mie2[which].get_hfield() * self.n_environment,
                        atol=0.1,
                        rtol=1e-1,
                    )

            if self.verbose:
                print(
                    "  - {}: mie effective polarizabilities env. index scaling test passed.".format(
                        device
                    )
                )


# %%
if __name__ == "__main__":
    print("testing global scaling invariance...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
