%module autopysta
%{
#define SWIG_FILE_WITH_INIT
static PyObject* pException;
#include "../include/misc.h"
#include "../include/random_generator.h"

#include "../include/params/params.h"
#include "../include/params/p_gipps.h"
#include "../include/params/p_idm.h"
#include "../include/params/p_linear.h"
#include "../include/params/p_martinez_jin_2020.h"
#include "../include/params/p_newell_random_acceleration.h"
#include "../include/params/p_newell.h"

#include "../include/point.h"
#include "../include/trajectory.h"

#include "../include/models/model.h"
#include "../include/models/gipps.h"
#include "../include/models/idm.h"
#include "../include/models/linear.h"
#include "../include/models/newell.h"
#include "../include/models/newell_constrained_timestep.h"
#include "../include/models/newell_random_acceleration.h"
#include "../include/models/martinez_jin_2020.h"
#include "../include/models/example_car.h"

#include "../include/lcm_gipps.h"
#include "../include/no_lch.h"
#include "../include/geometry.h"
#include "../include/vehicle.h"

#include "../include/creators/creator.h"
#include "../include/creators/creator_martinez_jin_2020.h"
#include "../include/creators/fixed_state_creator.h"
#include "../include/creators/fixed_demand_creator.h"
#include "../include/creators/creator_factory.h"

#include "../include/simulation.h"
#include "../include/results.h"
#include "../include/exception.h"
%}


%init %{
    pException = PyErr_NewException("_autopysta.Exception", NULL, NULL);
    Py_INCREF(pException);
    PyModule_AddObject(m, "Exception", pException);
%}

%include "stl.i"
%exception { 
    try {
        $action
    } catch (Exception &e) {
		PyErr_SetString(pException, (std::string("[autopysta module] [error #") + std::to_string(e.code()) + "]: " + e.what()).c_str());
        SWIG_fail;
    } catch (...) {
        SWIG_exception(SWIG_RuntimeError, "unknown exception");
    }
}

%include <std_vector.i>
%include <std_string.i>
%include "../include/misc.h"
%include "../include/random_generator.h"

%include "../include/params/params.h"
%include "../include/params/p_gipps.h"
%include "../include/params/p_idm.h"
%include "../include/params/p_linear.h"
%include "../include/params/p_martinez_jin_2020.h"
%include "../include/params/p_newell_random_acceleration.h"
%include "../include/params/p_newell.h"

%include "../include/point.h"
%include "../include/trajectory.h"
class Model {
public:
	virtual double free_flow_speed(params *p = (params*)nullptr) = 0;
	virtual Point *new_point(Point *leader, Point *follower, params *p = (params*)nullptr);
};
%include "../include/models/gipps.h"
%include "../include/models/idm.h"
%include "../include/models/newell.h"
%include "../include/models/newell_constrained_timestep.h"
%include "../include/models/newell_random_acceleration.h"
%include "../include/models/linear.h"

%include "../include/lcm_gipps.h"
%include "../include/no_lch.h"

%typemap(out) Creator* {
    if (dynamic_cast<FixedDemandCreator*>($1)) {
        $result = SWIG_NewPointerObj(dynamic_cast<FixedDemandCreator*>($1), SWIGTYPE_p_FixedDemandCreator, 0 |  0);
    } else if (dynamic_cast<FixedStateCreator*>($1)) {
        $result = SWIG_NewPointerObj(dynamic_cast<FixedStateCreator*>($1), SWIGTYPE_p_FixedStateCreator, 0 |  0);
    } else {
        $result = SWIG_NewPointerObj($1, SWIGTYPE_p_Creator, 0 |  0);
    }
}

%include "../include/creators/creator.h"
%include "../include/creators/creator_martinez_jin_2020.h"
%include "../include/creators/fixed_state_creator.h"
%include "../include/creators/fixed_demand_creator.h"
%include "../include/creators/creator_factory.h"
%include "../include/results.h"
%include "../include/exception.h"

namespace std
{
  %template(trajectories) vector<Trajectory*>;
  %template(vehvec) vector<Vehicle*>;
  %template(crtvec) vector<Creator*>;
  %template(pntvec) vector<Point*>;
  %template(fltvec) vector<double>;
  %template(fltvecvec) vector<vector<double>*>;
  %template() std::vector<int>;
}

%include "../include/geometry.h"
%include "../include/vehicle.h"
%include "../include/simulation.h"
%include "../include/trajectory.h"

%extend Trajectory {
	Point* __getitem__(unsigned int i){
		return (*($self)).get_point_at(i);
	}
	int __len__() {
		return (*($self)).size();
	}
}

%inline %{
// The -builtin SWIG option results in SWIGPYTHON_BUILTIN being defined
#ifdef SWIGPYTHON_BUILTIN
bool is_python_builtin() { return true; }
#else
bool is_python_builtin() { return false; }
#endif
%}



%pythonbegin %{
_autopystampl = False
try:
    import matplotlib.pyplot as plt
    _autopystampl=True
except:
    print("Error: matplotlib is not installed, drawing functions disabled")
%}

%pythoncode %{
def _autopysta_graph_trajectories(self, lane=-1):
    """
    Plot trajectories for all lanes or a specific lane.
    
    Args:
        lane (int): Lane number to plot. Default is -1 for all lanes.
    """
    colors = ['g-', 'r-', 'b-', 'k-', 'c-', 'm-', 'y-']
    plt.figure()
    if lane == -1:
        trys = self.get_all_trajectories_by_lane()
        plt.title("All lanes")
    else:
        trys = self.get_trajectories_by_lane(lane)
        plt.title(f"Lane {lane}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Position (meters)")
    for pi in range(len(trys)):
        pd = trys[pi]
        lane_num = pd[0].LANE()
        times = [pd[i].T() for i in range(len(pd))]
        positions = [pd[i].X() for i in range(len(pd))]
        plt.plot(times, positions, colors[lane_num % len(colors)])
    plt.show()

def _autopysta_graph_velocities(self, lane=-1):
    """
    Plot velocities for all lanes or a specific lane.
    
    Args:
        lane (int): Lane number to plot. Default is -1 for all lanes.
    """
    colors = ['g-', 'r-', 'b-', 'k-', 'c-', 'm-', 'y-']
    plt.figure()
    if(lane == -1):
        trys = self.get_all_trajectories_by_lane()
        plt.title("All lanes")
    else:
        trys = self.get_trajectories_by_lane(lane)
        plt.title(f"Lane {lane}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Velocity (m/s)")    
    for pi in range(len(trys)):
        pd = trys[pi]
        lane_num = pd[0].LANE()
        times = [pd[i].T() for i in range(len(pd))]
        velocities = [pd[i].V() for i in range(len(pd))]
        plt.plot(times, velocities, colors[lane_num % len(colors)])
    plt.show()
	
Results.plot_x_vs_t = _autopysta_graph_trajectories
Results.plot_v_vs_t = _autopysta_graph_velocities

class AutopystaException(BaseException):
    """
    Custom exception class for Autopysta errors.

    Attributes:
        code (int): The error code associated with the exception, representing the specific type of error.
        message (str): Detailed error message providing additional context for the exception.

    Methods:
        code(): Returns the error code associated with the exception.
        message(): Returns the error message describing the exception.

    Example usage in Python:
    ```python
    import autopysta as ap

    try:
        // Call a function that may raise an exception
        ap.some_function()
    except ap.AutopystaException as e:
        print(e)
    ```
    """
    def __init__(self):
        BaseException.__init__(self)
        self.myexc = Exception()

AutopystaException = _autopysta.Exception
%}
