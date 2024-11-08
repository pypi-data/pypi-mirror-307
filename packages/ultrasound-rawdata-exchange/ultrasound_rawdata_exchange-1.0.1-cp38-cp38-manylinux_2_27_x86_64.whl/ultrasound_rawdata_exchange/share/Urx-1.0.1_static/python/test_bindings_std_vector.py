import numpy as np


def test_vec_float64(
    self,
    vec_float64_constructor,
    vec_float64_args,
):
    testName = "VecFloat64 binding"
    print("\n--Test %s BEGIN--" % testName)

    self.assertEqual(vec_float64_constructor(), [])
    self.assertEqual(vec_float64_args([1.23, 2.34]), [1.23, 2.34])
    self.assertTrue(np.array_equal(vec_float64_args([1.23, 2.34]), np.array([1.23, 2.34])))

    v = [1.23, 2.34]
    toto = v[0]
    toto += 1
    self.assertEqual(v, [1.23, 2.34])
    v_ref = v
    v_ref[0] += 1
    self.assertEqual(v, [2.23, 2.34])

    print("--Test %s END--" % testName)


def test_vec_uint32(
    self,
    vec_uint32_constructor,
    vec_uint32_args,
):
    testName = "VecUInt32 binding"
    print("\n--Test %s BEGIN--" % testName)

    self.assertEqual(vec_uint32_constructor(), [])
    self.assertEqual(vec_uint32_args([1, 2, 3]), [1, 2, 3])
    self.assertTrue(np.array_equal(vec_uint32_args([1, 2, 3]), np.array([1, 2, 3])))

    v = [1, 2, 3]
    toto = v[0]
    toto += 1
    self.assertEqual(v, [1, 2, 3])
    v_ref = v
    v_ref[0] += 1
    self.assertEqual(v, [2, 2, 3])

    print("--Test %s END--" % testName)


def test_vec_vec_uint32(
    self,
    vec_vec_uint32_constructor,
    vec_vec_uint32_args,
):
    testName = "VecVecUInt32 binding"
    print("\n--Test %s BEGIN--" % testName)

    self.assertEqual(vec_vec_uint32_constructor(), [])
    self.assertEqual(
        vec_vec_uint32_args([[1, 2, 3], [4, 5, 6, 7, 8, 9]]),
        [[1, 2, 3], [4, 5, 6, 7, 8, 9]],
    )

    v = vec_vec_uint32_args([[1, 2, 3], [4, 5, 6, 7, 8, 9]])
    toto = v[0][0]
    toto += 1
    self.assertEqual(v[0], [1, 2, 3])
    v0_ref = v[0]
    v0_ref[0] += 1
    self.assertEqual(v[0], [2, 2, 3])
    v_ref = v
    v_ref[0][0] += 1
    self.assertEqual(v[0], [3, 2, 3])
    v_ref.append([10, 11])
    self.assertEqual(v[2], [10, 11])

    print("--Test %s END--" % testName)


def test_vec_vec_float64(
    self,
    vec_vec_float64_constructor,
    vec_vec_float64_args,
):
    testName = "VecVecFloat64 binding"
    print("\n--Test %s BEGIN--" % testName)

    self.assertEqual(vec_vec_float64_constructor(), [])
    self.assertEqual(
        vec_vec_float64_args([[1, 2, 3], [4, 5, 6, 7, 8, 9]]),
        [[1, 2, 3], [4, 5, 6, 7, 8, 9]],
    )

    v = vec_vec_float64_args([[1, 2, 3], [4, 5, 6, 7, 8, 9]])
    toto = v[0][0]
    toto += 1
    self.assertEqual(v[0], [1, 2, 3])
    v0_ref = v[0]
    v0_ref[0] += 1
    self.assertEqual(v[0], [2, 2, 3])
    v_ref = v
    v_ref[0][0] += 1
    self.assertEqual(v[0], [3, 2, 3])
    v_ref.append([10, 11])
    self.assertEqual(v[2], [10, 11])

    print("--Test %s END--" % testName)


def test_vec_vector3d(
    self,
    vector3d_constructor,
    vector3d_copy,
    vector3d_args,
    vec_vector3d_args,
):
    testName = "VecVector3D binding"
    print("\n--Test %s BEGIN--" % testName)
    v = vector3d_constructor()
    v_2 = vector3d_args(1, 2, 3)
    v_3 = vector3d_args(4, 5, 6)

    # List
    v_list = [v, v_2]
    self.assertEqual(len(v_list), 2)
    self.assertEqual(v_list, [v, v_2])
    v_list[0] = v_3
    self.assertEqual(v_list[0], v_3)
    self.assertEqual(v_list, [v_3, v_2])
    v_3.x = 42
    self.assertEqual(v_list[0].x, v_3.x)
    self.assertEqual(v_list[0], v_3)
    self.assertEqual(v_list, [v_3, v_2])
    v_list.append(v_3)
    self.assertEqual(len(v_list), 3)
    self.assertEqual(v_list, [v_3, v_2, v_3])

    # np.array
    v_arr = np.array([v, v_2])
    self.assertEqual(len(v_arr), 2)
    self.assertTrue(np.array_equal(v_arr, np.array([v, v_2])))
    v_arr[0] = v_3
    self.assertEqual(v_arr[0], v_3)
    self.assertTrue(np.array_equal(v_arr, np.array([v_3, v_2])))
    v_3.y = 42
    self.assertEqual(v_arr[0].y, v_3.y)
    self.assertEqual(v_arr[0], v_3)
    self.assertTrue(np.array_equal(v_arr, np.array([v_3, v_2])))
    v_arr = np.append(v_arr, v_3)
    self.assertEqual(len(v_arr), 3)
    self.assertTrue(np.array_equal(v_arr, np.array([v_3, v_2, v_3])))

    # VecVector3D
    vec = vec_vector3d_args([v, v_2])
    vec_2 = vec_vector3d_args(np.array([v, v_2]))
    self.assertEqual(len(vec), 2)
    self.assertEqual(len(vec_2), 2)
    self.assertEqual(vec, vec_2)
    vec[0] = v_3
    self.assertEqual(vec[0], v_3)
    self.assertEqual(vec, vec_vector3d_args([v_3, v_2]))

    # Modify v_3 does not affect C++ vector since it has been copied into it
    v_3.z = 42
    self.assertNotEqual(vec[0].z, v_3.z)
    self.assertNotEqual(vec[0], v_3)
    self.assertNotEqual(vec, vec_vector3d_args([v_3, v_2]))

    # v_ref is a reference to first element of C++ vector
    v_ref = vec[0]
    # Modify v_ref affects C++ vector
    v_ref.z = 42
    self.assertEqual(vec[0].z, v_ref.z)
    self.assertEqual(vec[0], v_ref)
    self.assertEqual(vec, vec_vector3d_args([v_ref, v_2]))
    self.assertEqual(vec, [v_ref, v_2])
    v_5 = vector3d_copy(v_ref)

    # v_ref is deallocated during the reallocation caused by the append
    vec.append(v_3)
    self.assertEqual(len(vec), 3)
    self.assertEqual(vec[0], v_5)
    self.assertEqual(vec[1], v_2)
    self.assertEqual(vec[2], v_3)
    self.assertEqual(vec, [v_5, v_2, v_3])
    self.assertEqual(vec, vec_vector3d_args([v_5, v_2, v_3]))

    print("--Test %s END--" % testName)


def test_vec_element_geometry_ptr(
    self,
    vector3d_constructor,
    vector3d_args,
    element_geometry_args,
    vec_element_geometry_ptr_args,
):
    testName = "VecElementGeometryPtr binding"
    print("\n--Test %s BEGIN--" % testName)

    v = vector3d_constructor()
    v_2 = vector3d_args(1, 2, 3)
    v_3 = vector3d_args(4, 5, 6)

    eg = element_geometry_args([v, v])
    eg_2 = element_geometry_args([v_2, v_2])
    eg_3 = element_geometry_args([v_3, v_3])

    # List
    eg_list = [eg, eg_2]
    # VecElementGeometryPtr
    vec = vec_element_geometry_ptr_args(eg_list)
    vec_2 = vec_element_geometry_ptr_args(np.array(eg_list))
    self.assertEqual(len(vec), 2)
    self.assertEqual(len(vec_2), 2)
    self.assertEqual(vec, vec_2)
    vec[0] = eg_3
    self.assertEqual(vec[0], eg_3)
    self.assertEqual(vec, vec_element_geometry_ptr_args([eg_3, eg_2]))

    # Modify eg_3 DOES affect C++ since the vector holds pointers
    eg_3.perimeter[0] = v
    self.assertEqual(vec[0], eg_3)
    self.assertEqual(vec, vec_element_geometry_ptr_args([eg_3, eg_2]))

    # eg_ref is a reference to first element of C++ vector
    eg_ref = vec[0]
    # Modify eg_ref affects C++ vector
    eg_ref.perimeter[0] = v
    self.assertEqual(vec[0], eg_ref)
    self.assertEqual(vec, vec_element_geometry_ptr_args([eg_ref, eg_2]))
    self.assertEqual(vec, [eg_ref, eg_2])
    eg_5 = element_geometry_args(eg_ref)

    # eg_ref is not deallocated during the reallocation caused by the append since it is a pointer
    vec.append(eg_3)
    self.assertEqual(len(vec), 3)
    self.assertEqual(vec[0], eg_5)
    self.assertEqual(vec[0], eg_ref)
    self.assertEqual(vec[1], eg_2)
    self.assertEqual(vec[2], eg_3)
    self.assertEqual(vec, [eg_5, eg_2, eg_3])
    self.assertEqual(vec, vec_element_geometry_ptr_args([eg_5, eg_2, eg_3]))

    print("--Test %s END--" % testName)


def test_vec_impulse_response_ptr(
    self,
    impulse_response_constructor,
    impulse_response_copy,
    impulse_response_args,
    vec_impulse_response_ptr_args,
):
    testName = "VecImpulseResponsePtr binding"
    print("\n--Test %s BEGIN--" % testName)

    ir = impulse_response_constructor()
    ir_2 = impulse_response_args(42, np.nan, "sec", [3.14, -42])
    ir_3 = impulse_response_args(123, 456, "ms", [1, 2, 3])

    # List
    ir_list = [ir, ir_2]
    # VecImpulseResponsePtr
    vec = vec_impulse_response_ptr_args(ir_list)
    vec_2 = vec_impulse_response_ptr_args(np.array(ir_list))
    self.assertEqual(len(vec), 2)
    self.assertEqual(len(vec_2), 2)
    self.assertEqual(vec, vec_2)
    vec[0] = ir_3
    self.assertEqual(vec[0], ir_3)
    self.assertEqual(vec, vec_impulse_response_ptr_args([ir_3, ir_2]))

    # Modify ir_3 DOES affect C++ since the vector holds pointers
    ir_3.time_offset.value = 123.456
    self.assertEqual(vec[0], ir_3)
    self.assertEqual(vec, vec_impulse_response_ptr_args([ir_3, ir_2]))

    # ir_ref is a reference to first element of C++ vector
    ir_ref = vec[0]
    # Modify ir_ref affects C++ vector
    ir_ref.time_offset.value = 3.14
    self.assertEqual(vec[0], ir_ref)
    self.assertEqual(vec, vec_impulse_response_ptr_args([ir_ref, ir_2]))
    self.assertEqual(vec, [ir_ref, ir_2])
    ir_5 = impulse_response_copy(ir_ref)

    # ir_ref is not deallocated during the reallocation caused by the append since it is a pointer
    vec.append(ir_3)
    self.assertEqual(len(vec), 3)
    self.assertEqual(vec[0], ir_5)
    self.assertEqual(vec[0], ir_ref)
    self.assertEqual(vec[1], ir_2)
    self.assertEqual(vec[2], ir_3)
    self.assertEqual(vec, [ir_5, ir_2, ir_3])
    self.assertEqual(vec, vec_impulse_response_ptr_args([ir_5, ir_2, ir_3]))

    print("--Test %s END--" % testName)


def test_vec_element(
    self,
    vector3d_constructor,
    vector3d_args,
    element_constructor,
    element_copy,
    transform_args,
    vec_element_args,
):
    testName = "VecElement binding"
    print("\n--Test %s BEGIN--" % testName)

    v = vector3d_constructor()
    v_2 = vector3d_args(1, 2, 3)
    v_3 = vector3d_args(4, 5, 6)

    elt = element_constructor()
    elt_2 = element_constructor()
    elt_2.transform = transform_args(v_2, v_2)
    elt_3 = element_constructor()
    elt_3.transform = transform_args(v_3, v_3)
    self.assertNotEqual(elt, elt_2)
    self.assertNotEqual(elt, elt_3)
    self.assertNotEqual(elt_2, elt_3)

    # List
    elt_list = [elt, elt_2]
    # VecElement
    vec = vec_element_args(elt_list)
    vec_2 = vec_element_args(np.array(elt_list))
    self.assertEqual(len(vec), 2)
    self.assertEqual(len(vec_2), 2)
    self.assertEqual(vec, vec_2)
    vec[0] = elt_3
    self.assertEqual(vec[0], elt_3)
    self.assertEqual(vec, vec_element_args([elt_3, elt_2]))

    # Modify elt_3 does not affect C++ vector since it has been copied into it
    elt_3.transform = transform_args(v_2, v_3)
    self.assertNotEqual(vec[0], elt_3)
    self.assertNotEqual(vec, vec_element_args([elt_3, elt_2]))

    # elt_ref is a reference to first element of C++ vector
    elt_ref = vec[0]
    # Modify elt_ref affects C++ vector
    elt_ref.transform.rotation = v
    self.assertEqual(vec[0], elt_ref)
    self.assertEqual(vec, vec_element_args([elt_ref, elt_2]))
    self.assertEqual(vec, [elt_ref, elt_2])
    elt_5 = element_copy(elt_ref)

    # elt_ref is deallocated during the reallocation caused by the append
    vec.append(elt_3)
    self.assertEqual(len(vec), 3)
    self.assertEqual(vec[0], elt_5)
    self.assertEqual(vec[1], elt_2)
    self.assertEqual(vec[2], elt_3)
    self.assertEqual(vec, [elt_5, elt_2, elt_3])
    self.assertEqual(vec, vec_element_args([elt_5, elt_2, elt_3]))

    print("--Test %s END--" % testName)


def test_vec_event(
    self,
    transmit_setup_args,
    receive_setup_args,
    probe_constructor,
    wave_constructor,
    transform_constructor,
    event_constructor,
    event_copy,
    event_args,
    vec_event_args,
):
    testName = "VecEvent binding"
    print("\n--Test %s BEGIN--" % testName)

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
    evt_3 = event_copy(evt)
    evt_3.transmit_setup = ts
    self.assertNotEqual(evt, evt_2)
    self.assertNotEqual(evt, evt_3)
    self.assertNotEqual(evt_2, evt_3)

    # List
    evt_list = [evt, evt_2]
    # VecEvent
    vec = vec_event_args(evt_list)
    vec_2 = vec_event_args(np.array(evt_list))
    self.assertEqual(len(vec), 2)
    self.assertEqual(len(vec_2), 2)
    self.assertEqual(vec, vec_2)
    vec[0] = evt_3
    self.assertEqual(vec[0], evt_3)
    self.assertEqual(vec, vec_event_args([evt_3, evt_2]))

    # Modify evt_3 does not affect C++ vector since it has been copied into it
    evt_3.transmit_setup.time_offset.value = 123
    self.assertNotEqual(vec[0], evt_3)
    self.assertNotEqual(vec, vec_event_args([evt_3, evt_2]))

    # evt_ref is a reference to first element of C++ vector
    evt_ref = vec[0]
    # Modify evt_ref affects C++ vector
    evt_ref.transmit_setup.time_offset.value = 123
    self.assertEqual(vec[0], evt_ref)
    self.assertEqual(vec, vec_event_args([evt_ref, evt_2]))
    self.assertEqual(vec, [evt_ref, evt_2])
    evt_5 = event_copy(evt_ref)

    # evt_ref is deallocated during the reallocation caused by the append
    vec.append(evt_3)
    self.assertEqual(len(vec), 3)
    self.assertEqual(vec[0], evt_5)
    self.assertEqual(vec[1], evt_2)
    self.assertEqual(vec[2], evt_3)
    self.assertEqual(vec, [evt_5, evt_2, evt_3])
    self.assertEqual(vec, vec_event_args([evt_5, evt_2, evt_3]))

    print("--Test %s END--" % testName)


def test_vec_excitation_ptr(
    self,
    excitation_copy,
    excitation_args,
    vec_excitation_ptr_args,
    double_nan_args,
):
    testName = "VecExcitationPtr binding"
    print("\n--Test %s BEGIN--" % testName)

    ex = excitation_args("linear", 42, double_nan_args(np.nan), [3.14, -42])
    ex_2 = excitation_args("linear", 123, 456, [789])
    ex_3 = excitation_args("linear", 987, 654, [321])

    # List
    ex_list = [ex, ex_2]
    # VecElement
    vec = vec_excitation_ptr_args(ex_list)
    vec_2 = vec_excitation_ptr_args(np.array(ex_list))
    self.assertEqual(len(vec), 2)
    self.assertEqual(len(vec_2), 2)
    self.assertEqual(vec, vec_2)
    vec[0] = ex_3
    self.assertEqual(vec[0], ex_3)
    self.assertEqual(vec, vec_excitation_ptr_args([ex_3, ex_2]))

    # Modify ex_3 DOES affect C++ vector since the vector holds pointers
    ex_3.sampling_frequency.value = 456.123
    self.assertEqual(vec[0], ex_3)
    self.assertEqual(vec, vec_excitation_ptr_args([ex_3, ex_2]))

    # ex_ref is a reference to first element of C++ vector
    ex_ref = vec[0]
    # Modify ex_ref affects C++ vector
    ex_ref.pulse_shape = "diverging"
    self.assertEqual(vec[0], ex_ref)
    self.assertEqual(vec, vec_excitation_ptr_args([ex_ref, ex_2]))
    self.assertEqual(vec, [ex_ref, ex_2])
    ex_5 = excitation_copy(ex_ref)

    # ex_ref is deallocated during the reallocation caused by the append
    vec.append(ex_3)
    self.assertEqual(len(vec), 3)
    self.assertEqual(vec[0], ex_5)
    self.assertEqual(vec[0], ex_ref)
    self.assertEqual(vec[1], ex_2)
    self.assertEqual(vec[2], ex_3)
    self.assertEqual(vec, [ex_5, ex_2, ex_3])
    self.assertEqual(vec, vec_excitation_ptr_args([ex_5, ex_2, ex_3]))

    print("--Test %s END--" % testName)
