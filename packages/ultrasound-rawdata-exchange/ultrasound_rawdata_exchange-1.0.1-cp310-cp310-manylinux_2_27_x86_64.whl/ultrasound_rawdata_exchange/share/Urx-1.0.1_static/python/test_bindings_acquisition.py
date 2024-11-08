import numpy as np
import gc


def test_acquisition(
    self,
    acq_constructor,
    acq_copy,
    double_nan_constructor,
    double_nan_copy,
    probe_constructor,
    probe_copy,
    excitation_constructor,
    excitation_copy,
    group_constructor,
    group_copy,
    group_data_constructor,
    group_data_copy,
    enum_probe,
    enum_sampling,
):
    testName = "Acquisition binding"
    print("\n--Test %s BEGIN--" % testName)

    # Check default CTOR
    acq = acq_constructor()
    self.assertEqual(acq.authors, "")
    self.assertEqual(acq.description, "")
    self.assertEqual(acq.local_time, "")
    self.assertEqual(acq.country_code, "")
    self.assertEqual(acq.system, "")
    self.assertTrue(np.isnan(acq.timestamp.value))
    self.assertEqual(acq.timestamp, double_nan_constructor())
    self.assertEqual(acq.probes, [])
    self.assertEqual(acq.excitations, [])
    self.assertEqual(acq.groups, [])

    # Check copy CTOR and referencing object
    acq_2 = acq_copy(acq)
    self.assertEqual(acq, acq_2)
    acq_2.authors = "Hello"
    self.assertNotEqual(acq, acq_2)
    acq_ref = acq
    acq_ref.authors = "Hello"
    self.assertEqual(acq, acq_ref)

    acq = acq_constructor()
    acq_2 = acq_copy(acq)

    # Reference is not possible for authors (string)
    self.assertEqual(acq, acq_2)
    authors = acq.authors
    self.assertEqual(authors, acq.authors)
    # Check assignment
    acq.authors = "Hello"
    self.assertNotEqual(authors, acq.authors)
    self.assertNotEqual(acq, acq_2)
    acq_2 = acq_copy(acq)

    # Reference is not possible for description (string)
    self.assertEqual(acq, acq_2)
    description = acq.description
    self.assertEqual(authors, acq.description)
    # Check assignment
    acq.description = "Hello"
    self.assertNotEqual(authors, acq.description)
    self.assertNotEqual(acq, acq_2)
    acq_2 = acq_copy(acq)

    # Reference is not possible for local_time (string)
    self.assertEqual(acq, acq_2)
    local_time = acq.local_time
    self.assertEqual(authors, acq.local_time)
    # Check assignment
    acq.local_time = "Hello"
    self.assertNotEqual(local_time, acq.local_time)
    self.assertNotEqual(acq, acq_2)
    acq_2 = acq_copy(acq)

    # Reference is not possible for country_code (string)
    self.assertEqual(acq, acq_2)
    country_code = acq.country_code
    self.assertEqual(authors, acq.country_code)
    # Check assignment
    acq.country_code = "Hello"
    self.assertNotEqual(country_code, acq.country_code)
    self.assertNotEqual(acq, acq_2)
    acq_2 = acq_copy(acq)

    # Reference is not possible for system (string)
    self.assertEqual(acq, acq_2)
    system = acq.system
    self.assertEqual(system, acq.system)
    # Check assignment
    acq.system = "Hello"
    self.assertNotEqual(system, acq.system)
    self.assertNotEqual(acq, acq_2)
    acq_2 = acq_copy(acq)

    # Reference is possible for timestamp (DoubleNan)
    self.assertEqual(acq, acq_2)
    self.assertEqual(acq.timestamp, double_nan_constructor())
    timestamp_ref = acq.timestamp
    self.assertEqual(timestamp_ref, acq.timestamp)
    self.assertEqual(timestamp_ref, double_nan_constructor())
    self.assertNotEqual(timestamp_ref.value, np.nan)
    # Check assignment
    acq.timestamp = double_nan_copy(10)
    self.assertEqual(timestamp_ref, acq.timestamp)
    timestamp_ref += 12
    self.assertEqual(timestamp_ref, acq.timestamp)
    timestamp_ref -= 12
    self.assertEqual(timestamp_ref, acq.timestamp)
    timestamp_ref *= 12
    self.assertEqual(timestamp_ref, acq.timestamp)
    timestamp_ref /= 12
    self.assertEqual(timestamp_ref, acq.timestamp)
    timestamp_ref = 123
    self.assertNotEqual(timestamp_ref, acq.timestamp)
    self.assertNotEqual(acq, acq_2)

    # probes is a pointer vector, thus all modifications are shared
    p = probe_constructor()
    p_rca = probe_constructor()
    p_rca.type = enum_probe().RCA
    p_rca_bis = probe_copy(p_rca)
    acq.probes = [p, p_rca]
    acq_2 = acq_copy(acq)
    self.assertEqual(acq.probes[1], p_rca)
    self.assertEqual(acq, acq_2)

    p_rca.type = enum_probe().LINEAR
    self.assertEqual(acq.probes[1], p_rca)
    self.assertEqual(acq_2.probes[1], p_rca)
    p_rca.type = enum_probe().RCA

    # Reference is possible for shared pointers vector
    self.assertEqual(acq.probes, [p, p_rca])
    probes_ref = acq.probes
    probes_ref[0] = p_rca_bis
    self.assertEqual(acq.probes, probes_ref)
    self.assertNotEqual(acq, acq_2)
    # Check assignment
    acq.probes = [p, p_rca]
    self.assertEqual(acq.probes, probes_ref)
    self.assertEqual(acq.probes, [p, p_rca])
    self.assertEqual(acq, acq_2)

    # deleting the local variable does not impact the shared pointers vectors
    del p
    del p_rca
    gc.collect()
    self.assertEqual(len(acq.probes), 2)
    self.assertEqual(len(acq_2.probes), 2)

    # deleting the pointers inside the vectors to check resize
    del acq.probes[0]
    del acq_2.probes[0]
    gc.collect()
    self.assertEqual(len(acq.probes), 1)
    self.assertEqual(len(acq_2.probes), 1)
    self.assertRaises(IndexError, lambda acq: acq.probes[1], acq)
    self.assertEqual(acq.probes[0].type, enum_probe().RCA)

    # excitations is a pointer vector, thus all modifications are shared
    ex = excitation_constructor()
    ex_2 = excitation_constructor()
    ex_2.pulse_shape = "Hello"
    ex_3 = excitation_copy(ex_2)
    acq.excitations = [ex, ex_2]
    acq_2 = acq_copy(acq)
    self.assertEqual(acq.excitations[1], ex_2)
    self.assertEqual(acq, acq_2)

    ex_2.pulse_shape = "World"
    self.assertEqual(acq.excitations[1], ex_2)
    self.assertEqual(acq_2.excitations[1], ex_2)
    ex_2.pulse_shape = "Hello"

    # Reference is possible for shared pointers vector
    self.assertEqual(acq.excitations, [ex, ex_2])
    excitations_ref = acq.excitations
    excitations_ref[0] = ex_3
    self.assertEqual(acq.excitations, excitations_ref)
    self.assertNotEqual(acq, acq_2)
    # Check assignment
    acq.excitations = [ex, ex_2]
    self.assertEqual(acq.excitations, excitations_ref)
    self.assertEqual(acq.excitations, [ex, ex_2])
    self.assertEqual(acq, acq_2)

    # deleting the local variable does not impact the shared pointers vectors
    del ex
    del ex_2
    gc.collect()
    self.assertEqual(len(acq.excitations), 2)
    self.assertEqual(len(acq_2.excitations), 2)

    # deleting the pointers inside the vectors to check resize
    del acq.excitations[0]
    del acq_2.excitations[0]
    gc.collect()
    self.assertEqual(len(acq.excitations), 1)
    self.assertEqual(len(acq_2.excitations), 1)
    self.assertRaises(IndexError, lambda acq: acq.excitations[1], acq)
    self.assertEqual(acq.excitations[0].pulse_shape, "Hello")

    # groups is a pointer vector, thus all modifications are shared
    g = group_constructor()
    g_2 = group_constructor()
    g_2.sampling_type = enum_sampling().RF
    g_3 = group_copy(g_2)
    acq.groups = [g, g_2]
    acq_2 = acq_copy(acq)
    self.assertEqual(acq.groups[1], g_2)
    self.assertEqual(acq, acq_2)

    g_2.sampling_type = enum_sampling().IQ
    self.assertEqual(acq.groups[1], g_2)
    self.assertEqual(acq_2.groups[1], g_2)
    g_2.sampling_type = enum_sampling().RF

    # Reference is possible for shared pointers vector
    self.assertEqual(acq.groups, [g, g_2])
    groups_ref = acq.groups
    groups_ref[0] = g_3
    self.assertEqual(acq.groups, groups_ref)
    self.assertNotEqual(acq, acq_2)
    # Check assignment
    acq.groups = [g, g_2]
    self.assertEqual(acq.groups, groups_ref)
    self.assertEqual(acq.groups, [g, g_2])
    self.assertEqual(acq, acq_2)

    # deleting the local variable does not impact the shared pointers vectors
    del g
    del g_2
    gc.collect()
    self.assertEqual(len(acq.groups), 2)
    self.assertEqual(len(acq_2.groups), 2)

    # deleting the pointers inside the vectors to check resize
    del acq.groups[0]
    del acq_2.groups[0]
    gc.collect()
    self.assertEqual(len(acq.groups), 1)
    self.assertEqual(len(acq_2.groups), 1)
    self.assertRaises(IndexError, lambda acq: acq.groups[1], acq)
    self.assertEqual(acq.groups[0].sampling_type, enum_sampling().RF)

    # groups_data is a pointer vector, thus all modifications are shared
    if group_data_constructor is not None and group_data_copy is not None:
        gd = group_data_constructor()
        gd_2 = group_data_constructor()
        gd_2.group_timestamp = double_nan_copy(42)
        gd_3 = group_data_copy(gd_2)
        gd_3.group_timestamp = double_nan_copy(24)
        acq.groups_data = [gd, gd_2]
        acq_2 = acq_copy(acq)
        self.assertEqual(acq.groups_data[1], gd_2)
        self.assertEqual(acq, acq_2)

        # gd_2 is a copy. Not a shared_ptr.
        # gd_2.group_timestamp = double_nan_copy(99)
        # self.assertEqual(acq.groups_data[1], gd_2)
        # self.assertEqual(acq_2.groups_data[1], gd_2)
        # gd_2.group_timestamp = double_nan_copy(42)

        # Reference is possible for GroupData vector
        self.assertEqual(acq.groups_data, [gd, gd_2])
        groups_data_ref = acq.groups_data
        groups_data_ref[0] = gd_3
        self.assertEqual(acq.groups_data, groups_data_ref)
        self.assertNotEqual(acq, acq_2)
        # Check assignment
        acq.groups_data = [gd, gd_2]
        self.assertEqual(acq.groups_data, groups_data_ref)
        self.assertEqual(acq.groups_data, [gd, gd_2])
        self.assertEqual(acq, acq_2)

        # deleting the local variable does not impact the shared pointers vectors
        del gd
        del gd_2
        gc.collect()
        self.assertEqual(len(acq.groups_data), 2)
        self.assertEqual(len(acq_2.groups_data), 2)

        # deleting the pointers inside the vectors to check resize
        del acq.groups_data[0]
        del acq_2.groups_data[0]
        gc.collect()
        self.assertEqual(len(acq.groups_data), 1)
        self.assertEqual(len(acq_2.groups_data), 1)
        self.assertRaises(IndexError, lambda acq: acq.groups_data[1], acq)
        self.assertEqual(acq.groups_data[0].group_timestamp, double_nan_copy(42))

    print("--Test %s END--" % testName)
