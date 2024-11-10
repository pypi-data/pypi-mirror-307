# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestComplexGreen3D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print(
                "testing Green's function postprocessing with discretized 3D-simulation..."
            )

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        self.wavelength = 550.0
        self.r_source = torch.as_tensor([[-50, 0, 40], [10, 0, -40]])
        self.r_probe = tg.tools.geometry.coordinate_map_2d_square(100, 5, r3=50)

        # --- setup test case simulation
        # - environment
        eps_env = 1.33
        mat_env = tg.materials.MatConstant(eps_env)
        env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - dummy illumination field
        wavelengths = torch.tensor([self.wavelength])
        e_inc_dummy = tg.env.freespace_3d.NullField()

        # - first structure: volume discretization
        l = w = h = 3
        step = 20.0
        mat_struct = tg.materials.MatConstant(eps=14.0)

        struct_mesh = tg.struct.StructDiscretizedCubic3D(
            tg.struct.volume.cuboid(l, w, h), step, mat_struct
        )
        struct_mesh.set_center_of_mass([0, 0, 0])

        # - full simulation
        self.sim = tg.simulation.Simulation(
            structures=[struct_mesh],
            environment=env,
            illumination_fields=[e_inc_dummy],
            wavelengths=wavelengths,
        )

    def test_green_implemenetations_equality(self):
        for device in self.devices:
            self.sim.set_device(device)

            G_6x6_1 = tg.postproc.green._G_direct(
                self.sim,
                r_probe=self.r_probe,
                r_source=self.r_source,
                wavelength=self.wavelength,
                progress_bar=False,
            )
            G_results = tg.postproc.green.G(
                self.sim,
                wavelength=self.wavelength,
                r_probe=self.r_probe,
                r_source=self.r_source,
                progress_bar=False,
                verbose=False,
            )
            G_6x6_2 = G_results["G_6x6"]

            torch.testing.assert_close(G_6x6_1, G_6x6_2)

    def test_green_far_from_structures(self):
        for device in self.devices:
            self.sim.set_device(device)

            # source and probe far from structure
            dx, dy = 10000, 15000
            r_source = torch.as_tensor(
                [dx, dy, 35], dtype=torch.float32, device=device
            )
            r_probe = tg.tools.geometry.coordinate_map_2d_square(
                500, 5, delta1=dx, delta2=dy, r3=40
            )["r_probe"].to(device)

            G_results = tg.postproc.green.G(
                self.sim,
                wavelength=self.wavelength,
                r_probe=r_probe,
                r_source=r_source,
                progress_bar=False,
                verbose=False,
            )
            G_sim = G_results["G_6x6"][0]  # first source position (of one...)

            G_vac = self.sim.environment.get_G_6x6(r_probe, r_source, self.wavelength)

            torch.testing.assert_close(G_sim, G_vac, rtol=1e-7, atol=1e-7)

    def test_green_output_consistency(self):
        for device in self.devices:
            self.sim.set_device(device)

            G_results = tg.postproc.green.G(
                self.sim,
                wavelength=self.wavelength,
                r_probe=self.r_probe,
                r_source=self.r_source,
                progress_bar=False,
                verbose=False,
            )

            torch.testing.assert_close(
                G_results["G_6x6"][..., :3, :3], G_results["G_Ep"]
            )
            torch.testing.assert_close(
                G_results["G_6x6"][..., 3:, 3:], G_results["G_Hm"]
            )
            torch.testing.assert_close(
                G_results["G_6x6"][..., 3:, :3], G_results["G_Hp"]
            )
            torch.testing.assert_close(
                G_results["G_6x6"][..., :3, 3:], G_results["G_Em"]
            )

    def test_green_on_sample(self):
        for device in self.devices:
            self.sim.set_device(device)

            G_results = tg.postproc.green.G(
                self.sim,
                wavelength=self.wavelength,
                r_probe=self.r_probe,
                r_source=self.r_source,
                progress_bar=False,
                verbose=False,
            )
            G_6x6 = G_results["G_6x6"][1, [7, 15]]
            # print(G_6x6)

            G_6x6_ref = torch.as_tensor(
                [
                    [
                        [
                            -1.0886665e-06 + 3.4371817e-07j,
                            1.9067019e-07 + 1.4734553e-08j,
                            -3.1135608e-07 - 2.2034816e-07j,
                            7.8117388e-09 - 7.9646398e-08j,
                            -9.4577649e-07 + 9.5512132e-07j,
                            -4.0747094e-07 + 9.6144527e-07j,
                        ],
                        [
                            4.4389697e-07 + 3.4053393e-08j,
                            -1.7907624e-08 + 4.4039223e-07j,
                            -3.1159952e-06 - 5.4947202e-07j,
                            1.1503031e-06 - 1.7255561e-06j,
                            3.4392386e-08 - 1.6531759e-07j,
                            1.6279989e-07 - 2.4089610e-07j,
                        ],
                        [
                            -4.3981481e-07 - 1.1056457e-07j,
                            -9.5553878e-07 - 2.3271329e-07j,
                            2.5345098e-06 + 1.8447427e-06j,
                            1.7052392e-07 + 1.4413263e-07j,
                            -1.4393464e-07 + 2.4122363e-07j,
                            -4.3346702e-08 + 2.1297481e-07j,
                        ],
                        [
                            -4.5305676e-08 + 2.0207312e-07j,
                            6.2416444e-07 - 4.5764466e-07j,
                            8.8299618e-07 - 1.8992670e-06j,
                            -1.5808587e-06 + 4.8191225e-07j,
                            2.4335304e-07 + 4.8928911e-08j,
                            -3.7928774e-07 - 7.7906037e-08j,
                        ],
                        [
                            -7.2510016e-07 + 1.1805100e-06j,
                            -1.2150139e-09 + 1.2138926e-08j,
                            -1.8058941e-09 - 5.1080988e-08j,
                            1.9038019e-07 + 1.0075015e-08j,
                            -8.2802069e-07 + 5.4201143e-07j,
                            -1.5086823e-06 - 1.0375794e-07j,
                        ],
                        [
                            -3.1773121e-07 + 4.1915200e-08j,
                            7.0668015e-08 - 6.8113444e-08j,
                            1.3259778e-07 - 4.7104811e-07j,
                            -3.4099307e-07 - 5.0336610e-08j,
                            -1.9207364e-06 - 3.6182652e-07j,
                            1.6083627e-06 + 1.0215560e-06j,
                        ],
                    ],
                    [
                        [
                            -2.6855030e-08 + 3.6664164e-07j,
                            -1.8608105e-07 - 7.7725915e-08j,
                            -1.0681069e-06 - 4.9962375e-07j,
                            -7.1662441e-08 + 2.0746609e-07j,
                            -8.4293180e-07 + 5.1455959e-07j,
                            3.0324927e-07 - 2.3444996e-07j,
                        ],
                        [
                            -2.2717860e-07 - 8.7862361e-08j,
                            -4.0295907e-07 + 1.5908353e-07j,
                            5.7338218e-07 + 1.7160788e-07j,
                            7.4529407e-07 - 2.1550466e-07j,
                            5.8602843e-08 - 1.8308809e-07j,
                            7.2966486e-07 - 5.4695380e-07j,
                        ],
                        [
                            -4.3967685e-07 - 2.8341822e-07j,
                            1.9003964e-07 + 9.7208570e-08j,
                            -3.8460701e-07 + 9.4305631e-07j,
                            -2.6108958e-07 + 1.2258243e-07j,
                            -6.1210079e-07 + 2.5809229e-07j,
                            8.2391143e-09 - 1.9775118e-08j,
                        ],
                        [
                            4.7302962e-08 - 1.3970885e-07j,
                            4.5206298e-07 - 2.6617460e-07j,
                            -5.6532929e-07 + 4.4056014e-07j,
                            -1.3186141e-07 + 4.3942893e-07j,
                            -3.5422531e-07 - 1.1052117e-07j,
                            -6.6941493e-07 - 2.0041207e-07j,
                        ],
                        [
                            -4.2451379e-07 + 8.1479044e-08j,
                            -1.5656733e-08 + 8.7590564e-08j,
                            -1.1492109e-06 + 8.7112801e-07j,
                            -3.4184518e-07 - 8.9863313e-08j,
                            -7.7181198e-07 + 2.4102647e-07j,
                            2.9585524e-07 + 7.4918162e-08j,
                        ],
                        [
                            1.9843461e-07 - 7.7167357e-08j,
                            3.8585475e-07 - 1.2949488e-07j,
                            -8.5867455e-08 + 1.0114601e-07j,
                            -8.7262913e-07 - 4.8787035e-07j,
                            4.0747955e-07 + 2.2172523e-07j,
                            -2.8789901e-07 + 5.4970485e-07j,
                        ],
                    ],
                ],
                dtype=torch.complex64,
                device=device,
            )
            torch.testing.assert_close(G_6x6, G_6x6_ref)


class TestLDOS3D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing LDOS with discretized 3D-simulation...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        self.wavelength = 550.0
        self.r_probe = tg.tools.geometry.coordinate_map_2d_square(100, 5, r3=50)

        # --- setup test case simulation
        # - environment
        eps_env = 1.33
        mat_env = tg.materials.MatConstant(eps_env)
        env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - dummy illumination field
        wavelengths = torch.tensor([self.wavelength])
        e_inc_dummy = tg.env.freespace_3d.NullField()

        # - first structure: volume discretization
        l = w = h = 3
        step = 20.0
        mat_struct = tg.materials.MatConstant(eps=14.0)

        struct_mesh = tg.struct.StructDiscretizedCubic3D(
            tg.struct.volume.cuboid(l, w, h), step, mat_struct
        )
        struct_mesh.set_center_of_mass([0, 0, 0])

        # - full simulation
        self.sim = tg.simulation.Simulation(
            structures=[struct_mesh],
            environment=env,
            illumination_fields=[e_inc_dummy],
            wavelengths=wavelengths,
        )

    def test_ldos_vs_green(self):
        for device in self.devices:
            self.sim.set_device(device)

            ldos_results = tg.postproc.green.ldos(
                self.sim,
                r_probe=self.r_probe,
                wavelength=self.wavelength,
                progress_bar=False,
            )

            G_ii_1 = ldos_results["G_ii"]

            G_results = tg.postproc.green.G(
                self.sim,
                wavelength=self.wavelength,
                r_probe=self.r_probe,
                r_source=self.r_probe,
                progress_bar=False,
                verbose=False,
            )

            G_6x6 = G_results["G_6x6"]

            G_ii_2 = G_6x6[
                torch.arange(G_6x6.shape[0]), torch.arange(G_6x6.shape[1]), ...
            ]

            torch.testing.assert_close(G_ii_1, G_ii_2)

    def test_ldos_far_from_structures(self):
        for device in self.devices:
            self.sim.set_device(device)

            # relative ldos far from structure (should be one)
            dx, dy = 10000, 15000
            r_probe = tg.tools.geometry.coordinate_map_2d_square(
                1000, 5, delta1=dx, delta2=dy, r3=50
            )["r_probe"].to(device)

            ldos_results = tg.postproc.green.ldos(
                self.sim,
                r_probe=r_probe,
                wavelength=self.wavelength,
                progress_bar=False,
            )

            ldos_p = ldos_results["ldos_partial"]
            ldos_e = ldos_results["ldos_e"]
            ldos_m = ldos_results["ldos_m"]
            
            ones_p = torch.ones_like(ldos_p)
            ones = torch.ones_like(ldos_e)

            torch.testing.assert_close(ldos_p, ones_p)
            torch.testing.assert_close(ldos_e, ones)
            torch.testing.assert_close(ldos_m, ones)

    def test_ldos_output_consistency(self):
        for device in self.devices:
            self.sim.set_device(device)

            ldos_results = tg.postproc.green.ldos(
                self.sim,
                r_probe=self.r_probe,
                wavelength=self.wavelength,
                progress_bar=False,
            )

            ldos_p = ldos_results["ldos_partial"]
            ldos_e = ldos_results["ldos_e"]
            ldos_m = ldos_results["ldos_m"]

            torch.testing.assert_close(ldos_e, 1 + torch.sum(ldos_p[:, :3] - 1, dim=-1))
            torch.testing.assert_close(ldos_m, 1 + torch.sum(ldos_p[:, 3:] - 1, dim=-1))

    def test_ldos_on_sample(self):
        for device in self.devices:
            self.sim.set_device(device)

            ldos_results = tg.postproc.green.ldos(
                self.sim,
                r_probe=self.r_probe,
                wavelength=self.wavelength,
                progress_bar=False,
            )
            ldos_p = ldos_results["ldos_partial"][::4]
            # print(ldos_p)

            ldos_p_ref = torch.as_tensor(
                [
                    [1.0114026, 1.0114026, 0.9800825, 1.0430276, 1.0430276, 1.0649197],
                    [1.0114025, 1.0114026, 0.9800825, 1.0430276, 1.0430276, 1.0649198],
                    [1.1013016, 1.1013016, 1.1013016, 1.1343262, 1.1343262, 1.1343262],
                    [0.5307579, 0.5307579, 2.5567667, 1.3563178, 1.3563179, 1.1544354],
                    [1.1013016, 1.1013014, 1.1013016, 1.1343262, 1.1343262, 1.1343262],
                    [1.0114026, 1.0114025, 0.9800825, 1.0430276, 1.0430276, 1.0649197],
                    [1.0114026, 1.0114026, 0.9800825, 1.0430276, 1.0430276, 1.0649198],
                ],
                dtype=torch.float32,
                device=device,
            )
            torch.testing.assert_close(ldos_p, ldos_p_ref)


# %%

# %%

# %%
if __name__ == "__main__":
    print(
        "testing Green's function calc. in complex environment structure Greens tensor and LDOS calculation..."
    ), torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
