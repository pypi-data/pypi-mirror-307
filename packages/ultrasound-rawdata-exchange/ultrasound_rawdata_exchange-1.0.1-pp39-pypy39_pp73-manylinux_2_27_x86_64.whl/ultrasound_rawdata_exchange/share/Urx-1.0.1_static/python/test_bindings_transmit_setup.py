import numpy as np
import gc


def test_transmit_setup(
    self,
    transmit_setup_constructor,
    transmit_setup_copy,
    transmit_setup_args,
    vec_vec_uint32_constructor,
    vec_excitation_ptr_constructor,
    vec_float64_constructor,
    transform_constructor,
    transform_args,
    double_nan_args,
    vector3d_constructor,
    vector3d_args,
    excitation_copy,
    excitation_args,
    probe_constructor,
    probe_copy,
    wave_constructor,
    wave_copy,
    enum_wave,
):
    testName = "TransmitSetup"
    print("\n--Test %s binding BEGIN--" % testName)

    # Check default CTOR
    ts = transmit_setup_constructor()
    self.assertEqual(ts.probe, None)
    self.assertEqual(ts.active_elements, vec_vec_uint32_constructor())
    self.assertEqual(ts.excitations, vec_excitation_ptr_constructor())
    self.assertEqual(ts.delays, vec_float64_constructor())
    self.assertEqual(ts.probe_transform, transform_constructor())
    self.assertEqual(ts.time_offset, double_nan_args(0))

    v = vector3d_constructor()
    v_2 = vector3d_args(1, 2, 3)

    t_2 = transform_args(v_2, v_2)

    # Check copy CTOR and referencing object
    ts_2 = transmit_setup_copy(ts)
    self.assertEqual(ts, ts_2)
    ts_2.probe_transform = t_2
    self.assertNotEqual(ts, ts_2)
    ts_ref = ts
    ts_ref.probe_transform = t_2
    self.assertEqual(ts, ts_ref)

    ex = excitation_args("linear", double_nan_args(42), np.nan, [3.14, -42])
    ex_2 = excitation_copy(ex)

    ex_3 = excitation_args("linear", 123, 456, [111, 222])
    ex_4 = excitation_copy(ex)

    # Check CTOR with all parameters
    ts = transmit_setup_args(
        probe_constructor(),
        wave_constructor(),
        [[1, 2, 3], [4, 5, 6, 7, 8, 9]],
        [ex, ex_2],
        [3.14, 42],
        t_2,
        42,
    )
    ts_2 = transmit_setup_copy(ts)
    self.assertEqual(ts.probe, None)
    self.assertEqual(ts.active_elements, [[1, 2, 3], [4, 5, 6, 7, 8, 9]])
    self.assertEqual(ts.excitations, [ex, ex_2])
    self.assertEqual(ts.delays, [3.14, 42])

    probe = probe_constructor()
    wave = wave_constructor()
    probe_2 = probe_copy(probe)
    probe_2.description = "rca"
    self.assertNotEqual(probe, probe_2)

    wave_2 = wave_copy(wave)
    wave_2.type = enum_wave().PLANE_WAVE
    self.assertNotEqual(wave, wave_2)

    ts = transmit_setup_args(
        probe_2,
        wave_2,
        [[1, 2, 3], [4, 5, 6, 7, 8, 9]],
        [ex, ex_2],
        [3.14, 42],
        t_2,
        42,
    )
    self.assertEqual(ts.probe, probe_2)
    self.assertEqual(ts.wave, wave_2)
    self.assertEqual(ts.probe_transform, t_2)
    self.assertEqual(ts.time_offset, 42)

    ts = transmit_setup_args(
        probe,
        wave,
        [[1, 2, 3], [4, 5, 6, 7, 8, 9]],
        [ex, ex_2],
        [3.14, 42],
        t_2,
        42,
    )

    # probe is a pointer and thus shared between objects
    self.assertEqual(ts.probe, probe)
    ts.probe = probe_2
    self.assertEqual(ts.probe, probe_2)
    probe_2.description = "linear"
    self.assertEqual(ts.probe, probe_2)
    del probe_2
    gc.collect()
    self.assertEqual(ts.probe, None)

    # wave is not a pointer
    self.assertEqual(ts.wave, wave)
    ts.wave = wave_2
    self.assertEqual(ts.wave, wave_2)
    wave_2.type = enum_wave().DIVERGING_WAVE
    self.assertNotEqual(ts.wave, wave_2)
    del wave_2
    gc.collect()
    ts_2.wave.type = enum_wave().PLANE_WAVE

    # Reference is possible for active_elements (VecVecUInt32)
    self.assertEqual(ts.active_elements, [[1, 2, 3], [4, 5, 6, 7, 8, 9]])
    channel_mapping_ref = ts.active_elements
    channel_mapping_ref[0] = [10, 11]
    self.assertEqual(ts.active_elements, channel_mapping_ref)
    self.assertNotEqual(ts, ts_2)
    # Check assignment
    ts.active_elements = [[1, 2, 3], [4, 5, 6, 7, 8, 9]]
    self.assertEqual(ts.active_elements, [[1, 2, 3], [4, 5, 6, 7, 8, 9]])
    self.assertEqual(ts, ts_2)

    # Vector of weak pointers cannot be referenced, thus a copy is made
    self.assertEqual(ts.excitations, [ex, ex_2])
    channel_excitations_2 = ts.excitations
    channel_excitations_2[0] = ex_3
    self.assertNotEqual(ts.excitations, channel_excitations_2)
    self.assertEqual(ts, ts_2)
    # Check assignment
    ts.excitations = [ex_3, ex_4, ex_2]
    self.assertEqual(ts.excitations, [ex_3, ex_4, ex_2])
    self.assertNotEqual(ts, ts_2)
    ts_2 = transmit_setup_copy(ts)
    self.assertEqual(ts, ts_2)

    del ex_4
    gc.collect()

    self.assertEqual(len(ts.excitations), 3)
    self.assertEqual(len(ts_2.excitations), 3)

    self.assertIsNone(ts.excitations[1])
    self.assertIsNone(ts_2.excitations[1])

    # Reference is possible for delays (VecFloat64)
    self.assertEqual(ts.delays, [3.14, 42])
    channel_delays_ref = ts.delays
    channel_delays_ref[0] = 123
    self.assertEqual(ts.delays, channel_delays_ref)
    self.assertNotEqual(ts, ts_2)
    # Check assignment
    ts.delays = [3.14, 42]
    self.assertEqual(ts.delays, [3.14, 42])
    self.assertEqual(ts, ts_2)

    # Reference is possible for probe_transform
    ts_2 = transmit_setup_copy(ts)
    self.assertEqual(ts.probe_transform, t_2)
    t_2.rotation = v
    self.assertEqual(ts, ts_2)
    self.assertEqual(ts.probe_transform, transform_args(v_2, v_2))
    self.assertNotEqual(ts.probe_transform, t_2)
    t_ref = ts.probe_transform
    t_ref.rotation = v
    self.assertEqual(ts.probe_transform, t_ref)
    self.assertNotEqual(ts, ts_2)
    # Check assignment
    ts.probe_transform = transform_args(v_2, v_2)
    self.assertEqual(ts.probe_transform, t_ref)
    self.assertEqual(ts.probe_transform, transform_args(v_2, v_2))
    self.assertEqual(ts, ts_2)

    # Reference is possible for time_offset (DoubleNan)
    self.assertEqual(ts.time_offset, 42)
    time_offset_ref = ts.time_offset
    time_offset_ref.value = 123
    self.assertEqual(ts.time_offset, time_offset_ref)
    self.assertNotEqual(ts, ts_2)
    # Check assignment
    ts.time_offset = double_nan_args(42)
    self.assertEqual(ts.time_offset, time_offset_ref)
    self.assertEqual(ts.time_offset, 42)
    self.assertEqual(ts, ts_2)

    print("--Test %s END--" % testName)
