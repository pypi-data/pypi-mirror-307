"""Describes a DeterministicStateTransitionModel"""

from typing import Callable, NamedTuple, Optional, Tuple

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import reparameterization

from gemlib.distributions.continuous_markov import _total_flux

tfd = tfp.distributions

Tensor = tf.Tensor

__all__ = ["DeterministicStateTransitionModel"]


class Results(NamedTuple):
    times: Tensor
    states: Tensor


class DeterministicStateTransitionModel(tfd.Distribution):
    """Deterministic state transition model

    A deterministic (ODE) state transmission model represented by a set of ODEs
    specified by a state transition graph with nodes representing state, and
    transtion rates representing edges.

    This class provides a programmable implementation of the deterministic
    state transition model, compatible with TensorFlow Probability.

    Examples:
      A deterministic metapopulation SIR model::

        import numpy as np
        import tensorflow as tf
        from gemlib.distributions import \
DeterministicTimeStateTransitionModel

        initial_state = np.array([[99, 1, 0]], np.float32)

        incidence_matrix = np.array(
            [
                [-1,  0],
                [ 1, -1],
                [ 0,  1],
            ],
            dtype=np.float32,
        )

        def transition_rates(t, state):
            si_rate = 0.28 * state[:,1] / tf.reduce_sum(state, axis=-1)
            ir_rate = tf.constant([0.14], np.float32)
            return si_rate, ir_rate

        #Instantiate model
        sir = DeterministicStateTransitionModel(
                transition_rate_fn=transition_rates,
                incidence_matrix=incidence_matrix,
                initial_state=initial_state,
                num_steps=100,
                initial_time=0,
                time_delta=1.0,
                )

        #One realisation of the epidemic process
        sir_sim = sir.sample(seed=[0, 0])
    """

    def __init__(
        self,
        transition_rate_fn: Callable[[float, Tensor], Tuple[Tensor]],
        incidence_matrix: Tensor,
        initial_state: Tensor,
        num_steps: Optional[int] = None,
        initial_time: Optional[float] = 0.0,
        time_delta: Optional[float] = 1.0,
        times: Tensor = None,
        solver: Optional[str] = "DormandPrince",
        solver_kwargs: dict = None,
        validate_args: Optional[bool] = False,
        name: Optional[str] = "DeterministicStateTransitionModel",
    ):
        """A deterministic (ODE) state transition model.

        Args:
          transition_rate_fn: a callable taking arguments `t` and `state` and
            returning a tuple of transition rates that broadcast with the
            dimension of `state`.
          incidence_matrix: a `[S, R]` matrix describing the change in states
            `S` resulting from transitions `R`.
          initial_state: a `[...,N, S]` (batched) tensor with the state values
            for `N` units and `S` states.
          num_steps: python integer representing the size of the time step to be
            used.
          initial_time: float representing an offset giving the time `t` of
            the first time step in the model.
          time_delta: float representing the size of the time step to be used.
          times: a 1-D tensor of times for which the ODE solutions are required.
          solver: a string giving the ODE solver method to use.  Can be "rk45"
            (default) or "BDF".  See the `TensorFlow Probability documentation`_
            for details.
          solver_kwargs: a dictionary of keyword argument to supply to the
            solver. See the solver documentation for details.
          validate_args: check that the values of the parameters supplied to the
            constructor are all within the domain of the ODE function
          name: the name of this distribution.

        .. _TensorFlow Probability documentation:
           https://www.tensorflow.org/probability/api_docs/python/tfp/math/ode
        """

        parameters = dict(locals())

        if (num_steps is not None) and (times is not None):
            raise ValueError(
                "Must specify exactly one of `num_steps` or `times`"
            )

        if num_steps is not None:
            self._times = tf.range(
                initial_time, time_delta * num_steps, time_delta
            )
        elif times is not None:
            self._times = tf.convert_to_tensor(times)
        else:
            raise ValueError("Must specify either `num_steps` or `times`")

        dtype = Results(
            times=tf.convert_to_tensor(self._times).dtype,
            states=tf.convert_to_tensor(initial_state).dtype,
        )

        super().__init__(
            dtype=dtype,
            reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
            validate_args=validate_args,
            allow_nan_stats=True,
            parameters=parameters,
            name=name,
        )

        self._solution = self._solve()

    @property
    def transition_rate_fn(self):
        return self.parameters["transition_rate_fn"]

    @property
    def incidence_matrix(self):
        return self.parameters["incidence_matrix"]

    @property
    def initial_state(self):
        return self.parameters["initial_state"]

    @property
    def num_steps(self):
        return self.parameters["num_steps"]

    @property
    def initial_time(self):
        return self.parameters["initial_time"]

    @property
    def time_delta(self):
        return self.parameters["time_delta"]

    @property
    def times(self):
        return self.parameters["times"]

    @property
    def solver(self):
        return self.parameters["solver"]

    @property
    def solver_kwargs(self):
        return self.parameters["solver_kwargs"]

    def _event_shape(self):
        times = tf.convert_to_tensor(self._times)
        initial_state = tf.convert_to_tensor(self.initial_state)
        shape = Results(
            times=tf.TensorShape(times.shape),
            states=tf.TensorShape(times.shape + initial_state.shape),
        )

        return shape

    def _event_shape_tensor(self):
        times = tf.convert_to_tensor(self.times)
        initial_state = tf.convert_to_tensor(self.initial_state)

        return Results(
            times=tf.constant(times.shape, tf.int32),
            states=tf.constant(
                [
                    times.shape[-1],
                    initial_state.shape[-2],
                    initial_state.shape[-1],
                ],
                tf.int32,
            ),
        )

    def _batch_shape(self):
        return Results(
            times=tf.TensorShape(()),
            states=tf.TensorShape(()),
        )

    def _batch_shape_tensor(self):
        return Results(
            times=tf.constant(()),
            states=tf.constant(()),
        )

    def _solve(self):
        solver_kwargs = {} if self.solver_kwargs is None else self.solver_kwargs

        if self.solver == "DormandPrince":
            solver = tfp.math.ode.DormandPrince(**solver_kwargs)
        elif self.solver == "BDF":
            solver = tfp.math.ode.BDF(**solver_kwargs)
        else:
            raise ValueError("`solver` must be one of 'DormandPrince' or 'BDF'")

        def gradient_fn(t, state):
            rates = self.transition_rate_fn(t, state)
            flux = _total_flux(rates, state, self.incidence_matrix)  # [...,R,N]
            derivs = tf.linalg.matmul(self.incidence_matrix, flux)
            return tf.linalg.matrix_transpose(derivs)

        solver_results = solver.solve(
            ode_fn=gradient_fn,
            initial_time=tf.convert_to_tensor(self.initial_time),
            initial_state=tf.convert_to_tensor(self.initial_state),
            solution_times=tf.convert_to_tensor(self._times),
        )

        return Results(
            times=solver_results.times,
            states=solver_results.states,
        )

    def _sample_n(self, sample_shape=(), seed=None):
        # Batch sampling an ODE model will yield identical results
        # so we can just broadcast out instead.
        batch_results = tf.nest.map_structure(
            lambda x, s: tf.broadcast_to(x, tf.TensorShape(sample_shape) + s),
            self._solution,
            self.event_shape,
        )

        return batch_results

    def _log_prob(self, value, atol=1e-6, rtol=1e-6):
        value = tf.nest.map_structure(lambda x: tf.convert_to_tensor(x), value)

        def approx_equal(x, y):
            diff = x - y
            eps = atol + rtol * tf.abs(y)
            return tf.reduce_all(diff < eps)

        is_approx_equal = tf.math.logical_and(
            *tf.nest.map_structure(approx_equal, self._solution, value)
        )

        return tf.where(
            is_approx_equal,
            tf.zeros(is_approx_equal.shape, value.times.dtype),
            tf.fill(
                is_approx_equal.shape,
                -tf.convert_to_tensor(np.inf, value.times.dtype),
            ),
        )
