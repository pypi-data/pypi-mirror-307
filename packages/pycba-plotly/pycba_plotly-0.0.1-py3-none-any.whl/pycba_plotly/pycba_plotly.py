import numpy as np
from collections import namedtuple

import pycba as cba  # The main package
from plotly import graph_objects as go
from plotly.subplots import make_subplots


def sum_envelopes(env1: cba.Envelopes, env2: cba.Envelopes):
    """
    Augments this set of envelopes with another compatible set, making this the
    envelopes of the two sets of envelopes.

    All envelopes must be from the same :class:`pycba.bridge.BridgeAnalysis` object.

    If the envelopes have a different number of analyses (due to differing vehicle
    lengths, for example), then only the reaction extreme are retained, and not
    the entire reaction history.

    Parameters
    ----------
    env2 : Envelopes
        A compatible :class:`pycba.results.Envelopes` object.

    Raises
    ------
    ValueError
        All envelopes must be for the same bridge.

    Returns
    -------
    None.
    """

    if env1.npts != env2.npts or env1.nsup != env2.nsup:
        raise ValueError("Cannot sum two inconsistent envelope")

    env = cba.Envelopes.zero_like(env1)

    env.Vmax = env1.Vmax + env2.Vmax
    env.Vmin = env1.Vmin + env2.Vmin

    env.Mmax = env1.Mmax + env2.Mmax
    env.Mmin = env1.Mmin + env2.Mmin

    env.Rmaxval = env1.Rmaxval + env2.Rmaxval
    env.Rminval = env1.Rminval + env2.Rminval

    if env1.nres == env2.nres:
        env.Rmax = env1.Rmax + env2.Rmax
        env.Rmin = env1.Rmin + env2.Rmin
    else:
        # Ensure no misleading results returned
        env.Rmax = np.zeros((env1.nsup, env1.nres))
        env.Rmin = np.zeros((env1.nsup, env1.nres))

    return env


def get_envelope_D(env):
    Dmax = np.zeros(env.npts)
    Dmin = np.zeros(env.npts)
    for res in env.vResults:
        Dmax = np.maximum(Dmax, res.results.D)
        Dmin = np.minimum(Dmin, res.results.D)
    return Dmin, Dmax


def get_beam_analysis(spans, EI, m=0, q=0, deadload_factor=1.0, liveload_factor=1.0):
    n = len(spans)
    beam_analysis = cba.BeamAnalysis(
        np.array([l / 1000 for l in spans]),
        EI / 1e9 * np.ones(n),
        np.array((n + 1) * [-1, 0]))

    dl = m * deadload_factor * 9810
    q = q * liveload_factor
    for i in range(n):
        beam_analysis.add_udl(i_span=i + 1, w=dl + q)

    return beam_analysis


def get_load_pattern(spans, EI, m=0, q=0, deadload_factor=1.0, liveload_factor=1.0):
    def load_matrix(n, q):
        LM = []
        for i in range(n):
            LM.append([i + 1, 1, q, 0, 0])
            # first number: span, second numbe: ?, third number: dead load in kN/m, fourtg/fifth number: ?
        return LM

    n = len(spans)
    beam_analysis = cba.BeamAnalysis([l / 1000 for l in spans], EI / 1e9 * np.ones(n), (n + 1) * [-1, 0])

    load_pattern = cba.LoadPattern(beam_analysis)

    if m is not None and m > 0:
        # Dead load
        lf_min, lf_max = 1.0, deadload_factor  # TODO, add disburdening (< 1)
        load_pattern.set_dead_loads(load_matrix(n, m * 9810), lf_max, lf_min)

    if q is not None and q > 0:
        # Live load
        lf_min, lf_max = 0.0, liveload_factor
        load_pattern.set_live_loads(load_matrix(n, q), lf_max, lf_min)

    return load_pattern


Vehicle = namedtuple("Vehicle", "axle_spacings axle_weights")


def get_vehicle_envelope(spans, EI, vehicle, liveload_factor=1.0):
    n = len(spans)
    bridge_analysis = cba.BridgeAnalysis()
    bridge_analysis.add_bridge([l / 1000 for l in spans], EI / 1e9 * np.ones(n), (n + 1) * [-1, 0])

    bridge_analysis.add_vehicle(
        np.array([x / 1000 for x in vehicle.axle_spacings]),  # mm -> m
        np.array([liveload_factor * al / 1000 for al in vehicle.axle_weights])
        # N -> kN
    )

    return bridge_analysis


def get_extremes(envelope):
    envelope.Dmin, envelope.Dmax = get_envelope_D(envelope)
    Dmin, Dmax = np.min(envelope.Dmin), np.max(envelope.Dmax)
    Vmin, Vmax = np.min(envelope.Vmin), np.max(envelope.Vmax)
    Mmin, Mmax = np.min(envelope.Mmin), np.max(envelope.Mmax)
    return ((1000 * Dmin, 1000 * Dmax), (1000 * min(envelope.Rminval), 1000 * max(envelope.Rmaxval)),
            (1000 * Vmin, 1000 * Vmax), (1e6 * Mmin, 1e6 * Mmax))


def get_envelopes(spans, EI, m=None, q=None, vehicle=None, deadload_factor=1.0, liveload_factor=1.0, step=500):
    if q is None or m is None or q == 0 or m == 0:  # no load patterning required
        beam_analysis = get_beam_analysis(spans, EI, m, q, deadload_factor, liveload_factor)
        beam_analysis.analyze()
        env = cba.Envelopes([beam_analysis.beam_results])
    else:
        load_pattern = get_load_pattern(spans, EI, m, q, deadload_factor, liveload_factor)
        env = load_pattern.analyze()

    if vehicle is not None:
        bridge_analysis = get_vehicle_envelope(spans, EI, vehicle, liveload_factor)
        env = sum_envelopes(env, bridge_analysis.run_vehicle(step / 1000))

    return env


fillmax = dict(mode='lines', line=dict(color='red'), fill='tozeroy', fillcolor='lightsalmon',
               fillpattern=dict(shape='/', size=5, fgcolor='white'))
fillmin = dict(mode='lines', line=dict(color='blue'), fill='tozeroy', fillcolor='lightblue',
               fillpattern=dict(shape='/', size=5, fgcolor='white'))


def plot_envelopes(env: cba.Envelopes, deformation_multiplier=1.0, each=False):
    env.Dmin, env.Dmax = get_envelope_D(env)  # missing in pycba
    f = 1000 * deformation_multiplier

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
    for row, (ymin, ymax, axis_title) in enumerate(
            ((-env.Mmin, -env.Mmax, "M (kNm)"),
             (env.Vmin, env.Vmax, "V (kN)"),
             (f * env.Dmin, f * env.Dmax, "D (mm)"))):
        fig.add_trace(go.Scatter(x=env.x, y=ymax, **fillmax), row=row + 1, col=1)
        fig.add_trace(go.Scatter(x=env.x, y=ymin, **fillmin), row=row + 1, col=1)
        fig.update_yaxes(title_text=axis_title, row=row + 1, col=1)
        fig.update_xaxes(title_text="x (m)", row=row + 1, col=1)

    # Adding conditional plots if 'each' is True
    if each:
        for res in env.vResults:
            fig.add_trace(go.Scatter(x=env.x, y=res.results.M, mode='lines', line=dict(color='red', width=0.5)), row=1,
                          col=1)
            fig.add_trace(go.Scatter(x=env.x, y=res.results.V, mode='lines', line=dict(color='blue', width=0.5)), row=2,
                          col=1)

    fig.layout.title = "Beam Envelope results"
    fig.layout.showlegend = False
    return fig


def plot_results(ba: cba.BeamAnalysis, deformation_multiplier=1.0):
    res = ba._beam_results.results
    f = 1000 * deformation_multiplier

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
    for row, (y, axis_title) in enumerate(
            ((-res.M, "M (kNm)"),
             (res.V, "V (kN)"),
             (f * res.D, "D (mm)"))):
        fig.add_trace(go.Scatter(x=res.x, y=y, **fillmax), row=row + 1, col=1)
        fig.update_yaxes(title_text=axis_title, row=row + 1, col=1)
        fig.update_xaxes(title_text="x (m)", row=row + 1, col=1)

    fig.layout.title = 'Beam Analysis Results'
    fig.layout.showlegend = False
    return fig


def plot(obj, deformation_multiplier=1.0):
    if isinstance(obj, cba.BeamAnalysis):
        return plot_results(obj, deformation_multiplier)
    else:
        return plot_envelopes(obj, deformation_multiplier)
