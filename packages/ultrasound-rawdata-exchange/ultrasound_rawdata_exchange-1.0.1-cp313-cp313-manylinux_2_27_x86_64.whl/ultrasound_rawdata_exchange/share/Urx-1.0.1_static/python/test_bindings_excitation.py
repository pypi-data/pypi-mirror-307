import numpy as np


def test_excitation(
    self,
    excitation_constructor,
    excitation_copy,
    excitation_args,
    double_nan_constructor,
    double_nan_copy,
    vec_float64_args,
):
    testName = "Excitation binding"
    print("\n--Test %s BEGIN--" % testName)

    # Check default CTOR
    ex = excitation_constructor()
    self.assertEqual(ex.pulse_shape, "")
    self.assertTrue(np.isnan(ex.transmit_frequency.value))
    self.assertTrue(np.isnan(ex.sampling_frequency.value))
    self.assertEqual(len(ex.waveform), 0)

    # Check copy CTOR and referencing object
    ex_2 = excitation_copy(ex)
    self.assertEqual(ex, ex_2)
    ex_2.pulse_shape = "Hello"
    self.assertNotEqual(ex, ex_2)
    ex_ref = ex
    ex_ref.pulse_shape = "Hello"
    self.assertEqual(ex, ex_ref)

    # Check CTOR with all parameters
    ex = excitation_args("linear", 42, np.nan, vec_float64_args([3.14, -42]))
    self.assertEqual(ex, excitation_args("linear", 42.0, np.nan, [3.14, -42]))
    ex_2 = excitation_copy(ex)
    self.assertEqual(ex, ex_2)

    # Check CTOR with all parameters varying double and DoubleNan
    ex = excitation_args("linear", double_nan_copy(42), np.nan, [3.14, -42])
    self.assertEqual(ex, ex_2)
    ex = excitation_args("linear", 42.0, double_nan_copy(np.nan), [3.14, -42])
    self.assertEqual(ex, ex_2)
    ex = excitation_args(
        "linear",
        double_nan_copy(42),
        double_nan_copy(np.nan),
        vec_float64_args([3.14, -42]),
    )
    self.assertEqual(ex, ex_2)

    # Reference is possible for waveform (VecFloat64)
    self.assertEqual(ex, ex_2)
    waveform_ref = ex.waveform
    self.assertEqual(waveform_ref, [3.14, -42])
    waveform_ref[0] = 123.456
    self.assertEqual(waveform_ref, ex.waveform)
    waveform_ref.append(987)
    self.assertEqual(waveform_ref, ex.waveform)
    ex.waveform.append(852)
    self.assertEqual(waveform_ref, ex.waveform)
    self.assertNotEqual(ex, ex_2)
    # Check assignment
    ex.waveform = [3.14, -42]
    self.assertEqual(waveform_ref, [3.14, -42])

    # Reference is possible for transmit_frequency (DoubleNan)
    self.assertEqual(ex, ex_2)
    ex.transmit_frequency = double_nan_copy(np.nan)
    transmit_frequency_ref = ex.transmit_frequency
    self.assertEqual(transmit_frequency_ref, ex.transmit_frequency)
    self.assertEqual(transmit_frequency_ref, double_nan_copy(np.nan))
    self.assertNotEqual(transmit_frequency_ref.value, np.nan)
    # Check assignment
    ex.transmit_frequency = double_nan_copy(10)
    self.assertEqual(transmit_frequency_ref, ex.transmit_frequency)
    transmit_frequency_ref += 12
    self.assertEqual(transmit_frequency_ref, ex.transmit_frequency)
    transmit_frequency_ref -= 12
    self.assertEqual(transmit_frequency_ref, ex.transmit_frequency)
    transmit_frequency_ref *= 12
    self.assertEqual(transmit_frequency_ref, ex.transmit_frequency)
    transmit_frequency_ref /= 12
    self.assertEqual(transmit_frequency_ref, ex.transmit_frequency)
    transmit_frequency_ref = 123
    self.assertNotEqual(transmit_frequency_ref, ex.transmit_frequency)
    self.assertNotEqual(ex, ex_2)
    ex.transmit_frequency = double_nan_copy(42)

    # Reference is possible for sampling_frequency (DoubleNan)
    self.assertEqual(ex, ex_2)
    ex.sampling_frequency = double_nan_copy(np.nan)
    sampling_frequency_ref = ex.sampling_frequency
    self.assertEqual(sampling_frequency_ref, ex.sampling_frequency)
    self.assertEqual(sampling_frequency_ref, double_nan_copy(np.nan))
    self.assertNotEqual(sampling_frequency_ref.value, np.nan)
    # Check assignment
    ex.sampling_frequency.value = 10
    self.assertEqual(sampling_frequency_ref, ex.sampling_frequency)
    sampling_frequency_ref += 12
    self.assertEqual(sampling_frequency_ref, ex.sampling_frequency)
    sampling_frequency_ref -= 12
    self.assertEqual(sampling_frequency_ref, ex.sampling_frequency)
    sampling_frequency_ref *= 12
    self.assertEqual(sampling_frequency_ref, ex.sampling_frequency)
    sampling_frequency_ref /= 12
    self.assertEqual(sampling_frequency_ref, ex.sampling_frequency)
    sampling_frequency_ref = double_nan_copy(123)
    self.assertNotEqual(sampling_frequency_ref, ex.sampling_frequency)
    self.assertNotEqual(ex, ex_2)
    ex.sampling_frequency = double_nan_constructor()

    # Reference is not possible for pulse_shape (string)
    self.assertEqual(ex, ex_2)
    pulse_shape = ex.pulse_shape
    self.assertEqual(pulse_shape, ex.pulse_shape)
    ex.pulse_shape = "Hello"
    self.assertNotEqual(pulse_shape, ex.pulse_shape)

    print("--Test %s END--" % testName)
