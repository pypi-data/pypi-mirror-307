import gc


def test_receive_setup(
    self,
    receive_setup_constructor,
    receive_setup_copy,
    receive_setup_args,
    probe_constructor,
    probe_copy,
    transform_constructor,
    transform_args,
    double_nan_constructor,
    double_nan_args,
    vec_vec_uint32_constructor,
    vec_float64_constructor,
    vector3d_constructor,
    vector3d_args,
):
    testName = "ReceiveSetup"
    print("\n--Test %s binding BEGIN--" % testName)

    # Check default CTOR
    rs = receive_setup_constructor()
    self.assertEqual(rs.probe, None)
    self.assertEqual(rs.probe_transform, transform_constructor())
    self.assertEqual(rs.sampling_frequency, double_nan_constructor())
    self.assertEqual(rs.number_samples, 0)
    self.assertEqual(rs.active_elements, vec_vec_uint32_constructor())
    self.assertEqual(rs.tgc_profile, vec_float64_constructor())
    self.assertEqual(rs.tgc_sampling_frequency, double_nan_constructor())
    self.assertEqual(rs.modulation_frequency, double_nan_constructor())
    self.assertEqual(rs.time_offset, double_nan_args(0))

    rs_2 = receive_setup_copy(rs)

    v = vector3d_constructor()
    v_2 = vector3d_args(1, 2, 3)

    t_2 = transform_args(v_2, v_2)

    # Check copy CTOR and referencing object
    self.assertEqual(rs, rs_2)
    rs_2.probe_transform = t_2
    self.assertNotEqual(rs, rs_2)
    rs_ref = rs
    rs_ref.probe_transform = t_2
    self.assertEqual(rs, rs_ref)

    # Check CTOR with all parameters
    rs = receive_setup_args(probe_constructor(), t_2, 1, 2, [[3]], [4], 5, 6, 7)
    self.assertEqual(rs.probe, None)

    probe = probe_constructor()
    probe_2 = probe_copy(probe)
    probe_2.description = "rca"
    self.assertNotEqual(probe, probe_2)

    rs = receive_setup_args(probe_2, t_2, 1, 2, [[3]], [4], 5, 6, 7)
    rs_2 = receive_setup_copy(rs)
    self.assertEqual(rs, rs_2)

    # Reference is not possible for string
    self.assertEqual(rs.probe, probe_2)
    # Check assignment
    probe_2.description = "linear"
    self.assertEqual(rs, rs_2)
    self.assertEqual(rs.probe, probe_2)
    del probe_2
    gc.collect()
    self.assertEqual(rs.probe, None)

    # Reference is possible for probe_transform
    self.assertEqual(rs.probe_transform, t_2)
    t_2.rotation = v
    self.assertEqual(rs, rs_2)
    self.assertEqual(rs.probe_transform, transform_args(v_2, v_2))
    self.assertNotEqual(rs.probe_transform, t_2)
    t_ref = rs.probe_transform
    t_ref.rotation = v
    self.assertEqual(rs.probe_transform, t_ref)
    self.assertNotEqual(rs, rs_2)
    # Check assignment
    rs.probe_transform = transform_args(v_2, v_2)
    self.assertEqual(rs.probe_transform, t_ref)
    self.assertEqual(rs.probe_transform, transform_args(v_2, v_2))
    self.assertEqual(rs, rs_2)

    # Reference is possible for sampling_frequency (DoubleNan)
    self.assertEqual(rs.sampling_frequency, 1)
    sampling_frequency_ref = rs.sampling_frequency
    sampling_frequency_ref.value = 123
    self.assertEqual(rs.sampling_frequency, sampling_frequency_ref)
    self.assertNotEqual(rs, rs_2)
    # Check assignment
    rs.sampling_frequency = double_nan_args(1)
    self.assertEqual(rs.sampling_frequency, sampling_frequency_ref)
    self.assertEqual(rs.sampling_frequency, 1)
    self.assertEqual(rs, rs_2)

    # Reference is not possible for number_samples since it is a primitive type (uint32)
    self.assertEqual(rs.number_samples, 2)
    number_samples_2 = rs.number_samples
    number_samples_2 = 123
    self.assertNotEqual(rs.number_samples, number_samples_2)
    self.assertEqual(rs.number_samples, 2)
    rs.number_samples = 123
    self.assertNotEqual(rs, rs_2)
    # Check assignment
    rs.number_samples = 2
    self.assertEqual(rs, rs_2)

    # Reference is possible for active_elements (VecVecUInt32)
    self.assertEqual(rs.active_elements, [[3]])
    channel_mapping_ref = rs.active_elements
    channel_mapping_ref[0] = [10, 11]
    self.assertEqual(rs.active_elements, channel_mapping_ref)
    self.assertNotEqual(rs, rs_2)
    # Check assignment
    rs.active_elements = [[3]]
    self.assertEqual(rs.active_elements, [[3]])
    self.assertEqual(rs, rs_2)

    # Reference is possible for tgc_profile (VecFloat64)
    self.assertEqual(rs.tgc_profile, [4])
    tgc_profile_ref = rs.tgc_profile
    tgc_profile_ref[0] = 123
    self.assertEqual(rs.tgc_profile, tgc_profile_ref)
    self.assertNotEqual(rs, rs_2)
    # Check assignment
    rs.tgc_profile = [4]
    self.assertEqual(rs.tgc_profile, [4])
    self.assertEqual(rs, rs_2)

    # Reference is possible for tgc_sampling_frequency (DoubleNan)
    self.assertEqual(rs.tgc_sampling_frequency, 5)
    tgc_sampling_frequency_ref = rs.tgc_sampling_frequency
    tgc_sampling_frequency_ref.value = 123
    self.assertEqual(rs.tgc_sampling_frequency, tgc_sampling_frequency_ref)
    self.assertNotEqual(rs, rs_2)
    # Check assignment
    rs.tgc_sampling_frequency = double_nan_args(5)
    self.assertEqual(rs.tgc_sampling_frequency, tgc_sampling_frequency_ref)
    self.assertEqual(rs.tgc_sampling_frequency, 5)
    self.assertEqual(rs, rs_2)

    # Reference is possible for tgc_sampling_frequency (DoubleNan)
    self.assertEqual(rs.modulation_frequency, 6)
    modulation_frequency_ref = rs.modulation_frequency
    modulation_frequency_ref.value = 123
    self.assertEqual(rs.modulation_frequency, modulation_frequency_ref)
    self.assertNotEqual(rs, rs_2)
    # Check assignment
    rs.modulation_frequency = double_nan_args(6)
    self.assertEqual(rs.modulation_frequency, modulation_frequency_ref)
    self.assertEqual(rs.modulation_frequency, 6)
    self.assertEqual(rs, rs_2)

    # Reference is possible for time_offset (DoubleNan)
    self.assertEqual(rs.time_offset, 7)
    time_offset_ref = rs.time_offset
    time_offset_ref.value = 123
    self.assertEqual(rs.time_offset, time_offset_ref)
    self.assertNotEqual(rs, rs_2)
    # Check assignment
    rs.time_offset = double_nan_args(7)
    self.assertEqual(rs.time_offset, time_offset_ref)
    self.assertEqual(rs.time_offset, 7)
    self.assertEqual(rs, rs_2)

    print("--Test %s END--" % testName)
