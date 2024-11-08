import numpy as np


def test_impulse_response(
    self,
    impulse_response_constructor,
    impulse_response_copy,
    impulse_response_args,
    double_nan_constructor,
    double_nan_args,
    vec_float64_args,
):
    testName = "ImpulseResponse binding"
    print("\n--Test %s BEGIN--" % testName)

    # Check default CTOR
    ir = impulse_response_constructor()
    self.assertTrue(np.isnan(ir.sampling_frequency.value))
    self.assertEqual(ir.time_offset.value, 0)
    self.assertEqual(ir.units, "")
    self.assertEqual(len(ir.data), 0)

    # Check copy CTOR and referencing object
    ir_2 = impulse_response_copy(ir)
    self.assertEqual(ir, ir_2)
    ir_2.units = "Hello"
    self.assertNotEqual(ir, ir_2)
    ir_ref = ir
    ir_ref.units = "Hello"
    self.assertEqual(ir, ir_ref)

    # Check CTOR with all parameters
    ir = impulse_response_args(42, np.nan, "sec", vec_float64_args([3.14, -42]))
    self.assertEqual(ir, impulse_response_args(42, np.nan, "sec", [3.14, -42]))
    ir_2 = impulse_response_copy(ir)
    self.assertEqual(ir, ir_2)

    ir = impulse_response_args(double_nan_args(42), np.nan, "sec", [3.14, -42])
    self.assertEqual(ir, ir_2)
    ir = impulse_response_args(42.0, double_nan_args(np.nan), "sec", [3.14, -42])
    self.assertEqual(ir, ir_2)
    ir = impulse_response_args(
        double_nan_args(42),
        double_nan_args(np.nan),
        "sec",
        vec_float64_args([3.14, -42]),
    )
    self.assertEqual(ir, ir_2)

    # Reference is possible for data (VecFloat64)
    self.assertEqual(ir, ir_2)
    data_ref = ir.data
    self.assertEqual(data_ref, [3.14, -42])
    data_ref[0] = 123.456
    self.assertEqual(data_ref, ir.data)
    data_ref.append(987)
    self.assertEqual(data_ref, ir.data)
    ir.data.append(852)
    self.assertEqual(data_ref, ir.data)
    self.assertNotEqual(ir, ir_2)
    # Check assignment
    ir.data = [3.14, -42]
    self.assertEqual(data_ref, [3.14, -42])
    self.assertEqual(ir, ir_2)

    # Reference is possible for sampling_frequency (DoubleNan)
    ir.sampling_frequency = double_nan_args(np.nan)
    sampling_frequency_ref = ir.sampling_frequency
    self.assertEqual(sampling_frequency_ref, ir.sampling_frequency)
    self.assertEqual(sampling_frequency_ref, double_nan_args(np.nan))
    self.assertNotEqual(sampling_frequency_ref.value, np.nan)
    # Check assignment
    ir.sampling_frequency = double_nan_args(10)
    self.assertEqual(sampling_frequency_ref, ir.sampling_frequency)
    sampling_frequency_ref += 12
    self.assertEqual(sampling_frequency_ref, ir.sampling_frequency)
    sampling_frequency_ref -= 12
    self.assertEqual(sampling_frequency_ref, ir.sampling_frequency)
    sampling_frequency_ref *= 12
    self.assertEqual(sampling_frequency_ref, ir.sampling_frequency)
    sampling_frequency_ref /= 12
    self.assertEqual(sampling_frequency_ref, ir.sampling_frequency)
    sampling_frequency_ref = 123
    self.assertNotEqual(sampling_frequency_ref, ir.sampling_frequency)
    self.assertNotEqual(ir, ir_2)
    ir.sampling_frequency = double_nan_args(42)
    self.assertEqual(ir, ir_2)

    # Reference is possible for time_offset (DoubleNan)
    time_offset_ref = ir.time_offset
    self.assertEqual(time_offset_ref, ir.time_offset)
    self.assertEqual(time_offset_ref, double_nan_args(np.nan))
    self.assertNotEqual(time_offset_ref.value, np.nan)
    # Check assignment
    ir.time_offset = double_nan_args(10)
    self.assertEqual(time_offset_ref, ir.time_offset)
    time_offset_ref += 12
    self.assertEqual(time_offset_ref, ir.time_offset)
    time_offset_ref -= 12
    self.assertEqual(time_offset_ref, ir.time_offset)
    time_offset_ref *= 12
    self.assertEqual(time_offset_ref, ir.time_offset)
    time_offset_ref /= 12
    self.assertEqual(time_offset_ref, ir.time_offset)
    time_offset_ref = 123
    self.assertNotEqual(time_offset_ref, ir.time_offset)
    self.assertNotEqual(ir, ir_2)
    ir.time_offset = double_nan_constructor()
    self.assertEqual(ir, ir_2)

    # Reference is not possible for units (string)
    self.assertEqual(ir.units, "sec")
    units_2 = ir.units
    units_2 = "Hello"
    self.assertNotEqual(ir.units, units_2)
    self.assertEqual(ir, ir_2)
    # Check assignment
    ir.units = "sec"
    self.assertEqual(ir.units, "sec")
    self.assertEqual(ir, ir_2)

    print("--Test %s END--" % testName)
