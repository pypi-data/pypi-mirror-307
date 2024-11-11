"""Describes a DiscreteTimeStateTransitionModel."""

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import (
    dtype_util,
    reparameterization,
    samplers,
)

from gemlib.distributions.discrete_markov import (
    compute_state,
    discrete_markov_log_prob,
    discrete_markov_simulation,
)
from gemlib.util import batch_gather, transition_coords

Tensor = tf.Tensor
tla = tf.linalg
tfd = tfp.distributions


class DiscreteTimeStateTransitionModel(tfd.Distribution):
    """Discrete-time state transition model

    A discrete-time state transition model assumes a population of
    individuals is divided into a number of mutually exclusive states,
    where transitions between states occur according to a Markov process.
    Such models are commonly found in epidemiological and ecological
    applications, where rapid implementation and modification is necessary.

    This class provides a programmable implementation of the discrete-time
    state transition model, compatible with TensorFlow Probability.


    Example
    -------
    A homogeneously mixing SIR model implementation::

        import numpy as np
        import tensorflow as tf
        from gemlib.distributions import DiscreteTimeStateTransitionModel

        # Initial state, counts per compartment (S, I, R), for one
        #   population
        initial_state = np.array([[99, 1, 0]], np.float32)

        incidence_matrix = np.array(
            [
                [-1, 0],
                [1, -1],
                [0, 1],
            ],
            dtype=np.float32,
        )


        def txrates(t, state):
            si = 0.28 * state[:, 1] / tf.reduce_sum(state, axis=-1)
            ir = tf.constant([0.14], np.float32)
            return si, ir


        # Instantiate model
        sir = DiscreteTimeStateTransitionModel(
            transition_rate_fn=txrates,
            incidence_matrix=incidence_matrix,
            initial_state=initial_state,
            num_steps=100,
        )

        # One realisation of the epidemic process
        sim = sir.sample(seed=[0, 0])

    Note
    ----
      See http://gitlab.com/gem-epidemics/gemlib/distributions/discrete_time_state_transition_model_examples.py
      for further examples.
    """

    def __init__(
        self,
        transition_rate_fn,
        incidence_matrix,
        initial_state,
        num_steps,
        initial_step=0,
        time_delta=1.0,
        validate_args=False,
        allow_nan_stats=True,
        name="DiscreteTimeStateTransitionModel",
    ):
        """Initialise a discrete-time state transition model.

        Args
        ----
          transition_rate_fn: Python callable of the form `fn(t, state)` taking
            the current time `t` (Python float) and state tensor `state`. This
            function returns a tensor which broadcasts to the first dimension of
            `incidence_matrix`.
          incidence_matrix: `Tensor` representing the stochiometry matrix for
            the state transition model where rows represent the transitions and
            columns states.
          initial_state: `Tensor` representing an initial state of counts per
            compartment.  The inner dimension is equal to the first dimension
            of `incidence_matrix`.
          initial_step: Python float representing an offset giving the time `t`
            of the first time step in the model.
          time_delta: Python float representing the size of the time step to be
                      used.
          num_steps: Python integer representing the number of time steps across
             which the model runs.

        """
        parameters = dict(locals())
        with tf.name_scope(name) as name:
            self._transition_rate_fn = transition_rate_fn
            self._incidence_matrix = tf.convert_to_tensor(
                incidence_matrix, dtype=initial_state.dtype
            )
            self._source_states = _compute_source_states(incidence_matrix)
            self._initial_state = initial_state
            self._initial_step = initial_step
            self._time_delta = time_delta
            self._num_steps = num_steps

            super().__init__(
                dtype=initial_state.dtype,
                reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
                parameters=parameters,
                name=name,
            )

        self.dtype = initial_state.dtype

    @property
    def transition_rate_fn(self):
        return self._transition_rate_fn

    @property
    def incidence_matrix(self):
        return self._incidence_matrix

    @property
    def initial_state(self):
        return self._initial_state

    @property
    def initial_step(self):
        return self._initial_step

    @property
    def source_states(self):
        return self._source_states

    @property
    def time_delta(self):
        return self._time_delta

    @property
    def num_steps(self):
        return self._num_steps

    @property
    def num_units(self):
        return self._initial_state.shape[-2]

    def _batch_shape(self):
        return tf.TensorShape([])

    def _event_shape(self):
        shape = tf.TensorShape(
            [
                tf.get_static_value(self._num_steps),  # T
                self.initial_state.shape[0],  # M
                self.incidence_matrix.shape[1],  # S
            ]
        )
        return shape

    def compute_state(
        self, events: Tensor, include_final_state: bool = False
    ) -> Tensor:
        """Computes a state timeseries given a transition events

        Args
        ----
            events: a `[self.num_steps, self.num_units, self.num_events]`
                    shaped tensor of events
            include_final_state: should the result include the final state?  If
                                 `False` (default), then `result.shape[1] ==
                                 events.shape[1]`.  If `True`, then
                                 `results.shape[1] == events.shape[1]  + 1`.

        Returns
        -------
            A tensor of shape `[self.num_meta, self.num_steps, self.num_states]`
            giving the number of individuals in each state at each time point in
             each unit.
        """
        return compute_state(
            incidence_matrix=self.incidence_matrix,
            initial_state=self.initial_state,
            events=events,
            closed=include_final_state,
        )

    def _sample_n(self, n, seed=None):
        """Runs a simulation from the epidemic model

        :param param: a dictionary of model parameters
        :param state_init: the initial state
        :returns: a tuple of times and simulated states.
        """
        n = tf.convert_to_tensor(n)
        seeds = samplers.split_seed(
            seed, n=n, salt="DiscreteTimeStateTransitionModel"
        )

        def one_sample(seed):
            _, events = discrete_markov_simulation(
                hazard_fn=self.transition_rate_fn,
                state=self.initial_state,
                start=self.initial_step,
                end=self.initial_step + self.num_steps * self.time_delta,
                time_step=self.time_delta,
                incidence_matrix=self.incidence_matrix,
                seed=seed,
            )
            return events

        sim = tf.map_fn(
            one_sample,
            elems=seeds,
            parallel_iterations=16,
            fn_output_signature=self.dtype,
        )
        # `sim` is `[T, M, S, S]`, and we need to pick out
        # elements `[..., i, j]` for all our relevant transitions
        # `i->j`.  `batch_gather` computes these coordinates and
        # invokes tf.gather.
        indices = transition_coords(self.incidence_matrix)
        sim = batch_gather(sim, indices)

        # `sim` is now `[T, M, R]` structure for T times,
        # M population units, and R transitions.
        return sim

    def _log_prob(self, y, **kwargs):
        dtype = dtype_util.common_dtype(
            [y, self.initial_state], dtype_hint=self.dtype
        )
        y = tf.convert_to_tensor(y, dtype)

        batch_shape = tf.shape(y)[:-3]
        flat_shape = tf.concat(
            [[tf.reduce_prod(batch_shape)], self.event_shape_tensor()], axis=0
        )
        y = tf.reshape(y, flat_shape)

        def one_log_prob(y):
            return discrete_markov_log_prob(
                events=y,
                init_state=tf.convert_to_tensor(self.initial_state, y.dtype),
                init_step=tf.convert_to_tensor(self.initial_step, y.dtype),
                time_delta=tf.convert_to_tensor(self.time_delta, y.dtype),
                hazard_fn=self.transition_rate_fn,
                incidence_matrix=tf.convert_to_tensor(
                    self.incidence_matrix, y.dtype
                ),
            )

        log_probs = tf.vectorized_map(
            one_log_prob,
            elems=y,  # fn_output_signature=y.dtype
        )

        return tf.reshape(log_probs, batch_shape)


def _compute_source_states(incidence_matrix, dtype=tf.int32):
    """Computes the indices of the source states for each
       transition in a state transition model.

    :param incidence_matrix: incidence matrix in `[S, R]` orientation
                          for `S` states and `R` transitions.
    :returns: a tensor of shape `(R,)` containing source state indices.
    """
    incidence_matrix = tf.transpose(incidence_matrix)

    source_states = tf.reduce_sum(
        tf.cumsum(
            tf.clip_by_value(
                -incidence_matrix, clip_value_min=0, clip_value_max=1
            ),
            axis=-1,
            reverse=True,
            exclusive=True,
        ),
        axis=-1,
    )

    return tf.cast(source_states, dtype)
