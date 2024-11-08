def test_wave(
    self,
    wave_constructor,
    wave_copy,
    wave_args,
    enum_wave,
    double_nan_constructor,
    double_nan_args,
    vector3d_constructor,
    vec_float64_constructor,
):
    testName = "Wave"
    print("\n--Test %s binding BEGIN--" % testName)

    # Check default CTOR
    w = wave_constructor()
    self.assertEqual(w.type, enum_wave().UNDEFINED)
    self.assertEqual(w.time_zero, double_nan_constructor())
    self.assertEqual(w.time_zero_reference_point, vector3d_constructor())
    self.assertEqual(w.parameters, vec_float64_constructor())

    # Check copy CTOR and referencing object
    w_2 = wave_copy(w)
    self.assertEqual(w, w_2)
    w_2.type = enum_wave().CONVERGING_WAVE
    self.assertNotEqual(w, w_2)
    p_ref = w
    p_ref.type = enum_wave().CONVERGING_WAVE
    self.assertEqual(w, p_ref)

    # Check CTOR with all parameters
    w = wave_args(enum_wave().CONVERGING_WAVE, 0, vector3d_constructor(), [12.34, 56.78])
    self.assertEqual(w.type, enum_wave().CONVERGING_WAVE)
    self.assertEqual(w.time_zero, 0)
    self.assertEqual(w.time_zero_reference_point, vector3d_constructor())
    self.assertEqual(w.parameters, [12.34, 56.78])
    w_2 = wave_copy(w)
    self.assertEqual(w, w_2)

    # Reference is not possible for enum
    self.assertEqual(w.type, enum_wave().CONVERGING_WAVE)
    type_2 = w.type
    type_2 = enum_wave().DIVERGING_WAVE
    self.assertNotEqual(w.type, type_2)
    self.assertEqual(w, w_2)
    # Check assignment
    w.type = enum_wave().CONVERGING_WAVE
    self.assertEqual(w.type, enum_wave().CONVERGING_WAVE)
    self.assertEqual(w, w_2)

    # Reference is possible for time_zero (DoubleNan)
    self.assertEqual(w.time_zero, 0)
    time_zero_ref = w.time_zero
    time_zero_ref.value = 123
    self.assertEqual(w.time_zero, time_zero_ref)
    self.assertNotEqual(w, w_2)
    # Check assignment
    w.time_zero = double_nan_args(132)
    self.assertEqual(w.time_zero, time_zero_ref)
    self.assertEqual(w.time_zero, 132)
    w.time_zero = double_nan_args(0)
    self.assertEqual(w, w_2)

    # Reference is possible for time_zero_reference_point (Vector3D)
    self.assertEqual(w.time_zero_reference_point, vector3d_constructor())
    time_zero_reference_point_ref = w.time_zero_reference_point
    time_zero_reference_point_ref.x = 123
    self.assertEqual(w.time_zero_reference_point, time_zero_reference_point_ref)
    self.assertNotEqual(w, w_2)
    # Check assignment
    w.time_zero_reference_point = vector3d_constructor()
    self.assertEqual(w.time_zero_reference_point, time_zero_reference_point_ref)
    self.assertEqual(w.time_zero_reference_point, vector3d_constructor())
    self.assertEqual(w, w_2)

    # Reference is possible for parameters (VecFloat64)
    self.assertEqual(w.parameters, [12.34, 56.78])
    parameters_ref = w.parameters
    parameters_ref[0] = 123
    self.assertEqual(w.parameters, parameters_ref)
    self.assertNotEqual(w, w_2)
    # Check assignment
    w.parameters = [12.34, 56.78]
    self.assertEqual(w.parameters, [12.34, 56.78])
    self.assertEqual(w, w_2)

    print("--Test %s END--" % testName)
