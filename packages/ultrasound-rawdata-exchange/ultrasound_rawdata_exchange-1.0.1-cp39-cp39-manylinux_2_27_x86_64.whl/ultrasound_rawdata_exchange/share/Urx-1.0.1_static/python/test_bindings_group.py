import numpy as np


def test_group(
    self,
    event_constructor,
    event_args,
    vec_event_constructor,
    enum_sampling,
    enum_data,
    group_constructor,
    group_copy,
    group_args,
    receive_setup_args,
    transmit_setup_args,
    probe_constructor,
    wave_constructor,
    transform_constructor,
    double_nan_constructor,
    double_nan_copy,
):
    testName = "Group binding"
    print("\n--Test %s BEGIN--" % testName)

    # Check default CTOR
    g = group_constructor()
    self.assertEqual(g.sampling_type, enum_sampling().UNDEFINED)
    self.assertEqual(g.data_type, enum_data().UNDEFINED)
    self.assertEqual(g.description, "")
    self.assertTrue(np.isnan(g.sound_speed.value))
    self.assertEqual(g.sound_speed, double_nan_constructor())
    self.assertEqual(g.sequence, vec_event_constructor())

    # Check copy CTOR and referencing object
    g_2 = group_copy(g)
    self.assertEqual(g, g_2)
    g_2.description = "Hello"
    self.assertNotEqual(g, g_2)
    g_ref = g
    g_ref.description = "Hello"
    self.assertEqual(g, g_ref)

    rs = receive_setup_args(probe_constructor(), transform_constructor(), 1, 2, [[3]], [4], 5, 6, 7)
    ts = transmit_setup_args(
        probe_constructor(),
        wave_constructor(),
        [],
        [],
        [],
        transform_constructor(),
        42,
    )
    evt = event_constructor()
    evt_2 = event_args(ts, rs)

    # Check CTOR with all parameters
    g = group_args(enum_sampling().RF, enum_data().INT32, "BMode", 1500, [evt, evt_2])
    self.assertEqual(g.sampling_type, enum_sampling().RF)
    self.assertEqual(g.data_type, enum_data().INT32)
    self.assertEqual(g.description, "BMode")
    self.assertEqual(g.sound_speed, 1500)
    self.assertEqual(g.sequence, [evt, evt_2])
    g_2 = group_copy(g)

    # Reference is not possible for enum
    self.assertEqual(g.sampling_type, enum_sampling().RF)
    sampling_type_2 = g.sampling_type
    sampling_type_2 = enum_sampling().IQ
    self.assertNotEqual(g.sampling_type, sampling_type_2)
    self.assertEqual(g, g_2)
    # Check assignment
    g.sampling_type = enum_sampling().RF
    self.assertEqual(g.sampling_type, enum_sampling().RF)
    self.assertEqual(g, g_2)

    # Reference is not possible for enum
    self.assertEqual(g.data_type, enum_data().INT32)
    data_type_2 = g.data_type
    data_type_2 = enum_data().DOUBLE
    self.assertNotEqual(g.data_type, data_type_2)
    self.assertEqual(g, g_2)
    # Check assignment
    g.data_type = enum_data().INT32
    self.assertEqual(g.data_type, enum_data().INT32)
    self.assertEqual(g, g_2)

    # Reference is not possible for string
    self.assertEqual(g.description, "BMode")
    description_2 = g.description
    description_2 = "PW"
    self.assertNotEqual(g.description, description_2)
    self.assertEqual(g, g_2)
    # Check assignment
    g.description = "BMode"
    self.assertEqual(g.description, "BMode")
    self.assertEqual(g, g_2)

    # Reference is possible for sound_speed (DoubleNan)
    self.assertEqual(g, g_2)
    self.assertEqual(g.sound_speed, 1500)
    sound_speed_ref = g.sound_speed
    self.assertEqual(sound_speed_ref, g.sound_speed)
    self.assertEqual(sound_speed_ref, 1500)
    self.assertNotEqual(sound_speed_ref.value, np.nan)
    # Check assignment
    g.sound_speed = double_nan_copy(10)
    self.assertEqual(sound_speed_ref, g.sound_speed)
    sound_speed_ref += 12
    self.assertEqual(sound_speed_ref, g.sound_speed)
    sound_speed_ref -= 12
    self.assertEqual(sound_speed_ref, g.sound_speed)
    sound_speed_ref *= 12
    self.assertEqual(sound_speed_ref, g.sound_speed)
    sound_speed_ref /= 12
    self.assertEqual(sound_speed_ref, g.sound_speed)
    sound_speed_ref = 123
    self.assertNotEqual(sound_speed_ref, g.sound_speed)
    self.assertNotEqual(g, g_2)

    # Reference is possible for sequence (VecEvent)
    g_2 = group_copy(g)
    self.assertEqual(g.sequence, [evt, evt_2])
    seq_ref = g.sequence
    seq_ref.append(evt_2)
    self.assertEqual(g.sequence, seq_ref)
    self.assertNotEqual(g, g_2)
    # Check assignment
    g.sequence = [evt, evt_2]
    self.assertEqual(g.sequence, seq_ref)
    self.assertEqual(g.sequence, [evt, evt_2])
    self.assertEqual(g, g_2)

    print("--Test %s END--" % testName)
