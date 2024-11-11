import autopysta as ap
import unittest

class TestSimulation(unittest.TestCase):

    def setUp(self):
        # Initialize common parameters for multiple tests
        self.length = 1000
        self.initial_lanes = 3
        self.merge_position = 300
        self.diverge_position = 700
        self.total_time = 60
        self.time_step = 0.1
        self.verbose = False

        # Geometry object
        self.geometry = ap.Geometry(self.length, self.initial_lanes, self.merge_position, self.diverge_position)

        # Driving models
        self.idm_model = ap.idm()
        self.gipps_model = ap.gipps()

        # Vehicle creators
        self.lane_creators = [
            ap.FixedStateCreator(self.idm_model, 10, 15),
            ap.FixedDemandCreator(self.gipps_model, 0.5),
            ap.FixedStateCreator(self.gipps_model, 20, 10)
        ]

        # Lane-changing model
        self.lane_change_model = ap.lcm_gipps()

    def test_simulation_initialization(self):
        """Test if Simulation initializes without exceptions."""
        try:
            sim = ap.Simulation(
                self.lane_change_model,
                self.total_time,
                self.geometry,
                self.lane_creators,
                [],
                self.time_step,
                self.verbose
            )
            self.assertTrue(sim is not None)
        except Exception as e:
            self.fail(f"Simulation initialization failed with exception: {e}")

    def test_simulation_run(self):
        """Test the simulation run and check if results are returned."""
        sim = ap.Simulation(
            self.lane_change_model,
            self.total_time,
            self.geometry,
            self.lane_creators,
            [],
            self.time_step,
            self.verbose
        )
        results = sim.run()
        self.assertIsNotNone(results)
        self.assertTrue(len(results.get_all_trajectories()) > 0, "No trajectories returned from simulation.")

    def test_plotting(self):
        """Test if plotting functions work without error."""
        sim = ap.Simulation(
            self.lane_change_model,
            self.total_time,
            self.geometry,
            self.lane_creators,
            [],
            self.time_step,
            self.verbose
        )
        results = sim.run()
        
        try:
            results.plot_x_vs_t()  # Plot all lanes
            results.plot_x_vs_t(lane=1)
            results.plot_x_vs_t(lane=2)
            results.plot_x_vs_t(lane=3)
        except Exception as e:
            self.fail(f"Plotting failed with exception: {e}")

    def test_invalid_parameters(self):
        """Test if Simulation raises exceptions for invalid parameters."""
        with self.assertRaises(ap.AutopystaException):
            ap.Simulation(self.lane_change_model, -10, self.geometry, self.lane_creators, [], self.time_step)

        with self.assertRaises(ap.AutopystaException):
            ap.Simulation(self.lane_change_model, self.total_time, self.geometry, self.lane_creators, [], 0)

if __name__ == "__main__":
    unittest.main()
