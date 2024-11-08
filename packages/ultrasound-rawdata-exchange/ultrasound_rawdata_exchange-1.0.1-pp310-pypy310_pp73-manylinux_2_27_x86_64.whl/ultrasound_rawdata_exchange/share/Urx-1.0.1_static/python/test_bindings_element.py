import numpy as np
import gc


def test_element(
    self,
    vector3d_constructor,
    vector3d_args,
    element_constructor,
    element_copy,
    element_args,
    transform_constructor,
    transform_args,
    element_geometry_constructor,
    element_geometry_args,
    impulse_response_constructor,
    impulse_response_args,
):
    testName = "Element binding"
    print("\n--Test %s BEGIN--" % testName)

    v = vector3d_constructor()
    v_2 = vector3d_args(1, 2, 3)
    v_3 = vector3d_args(4, 5, 6)

    # Check default CTOR
    elt = element_constructor()
    self.assertEqual(elt.transform, transform_constructor())
    self.assertEqual(elt.element_geometry, None)
    self.assertEqual(elt.impulse_response, None)

    # Check copy CTOR and referencing object
    elt_2 = element_copy(elt)
    self.assertEqual(elt, elt_2)
    elt_2.transform = transform_args(v_2, v_2)
    self.assertNotEqual(elt, elt_2)
    elt_ref = elt
    elt_ref.transform = transform_args(v_2, v_2)
    self.assertEqual(elt, elt_ref)

    t = transform_args(v_3, v_3)

    # Check CTOR with all parameters
    elt = element_args(t, element_geometry_constructor(), impulse_response_constructor())
    self.assertEqual(elt.element_geometry, None)
    self.assertEqual(elt.impulse_response, None)
    self.assertEqual(elt.transform, transform_args(v_3, v_3))
    t.rotation = v
    self.assertEqual(elt.transform, transform_args(v_3, v_3))
    self.assertNotEqual(elt.transform, t)

    t_ref = elt.transform
    t_ref.rotation = v
    self.assertEqual(elt.transform, t_ref)

    eg = element_geometry_args([v, v_2])

    # Reference is possible for element_geometry since it's a weak_ptr
    # Check assignment
    elt.element_geometry = eg
    self.assertEqual(elt.element_geometry, element_geometry_args([v, v_2]))
    eg.perimeter[0] = v_3
    self.assertEqual(elt.element_geometry, element_geometry_args([v_3, v_2]))
    eg_ref = elt.element_geometry
    eg_ref.perimeter[0] = v
    self.assertEqual(elt.element_geometry, eg)
    self.assertEqual(elt.element_geometry, eg_ref)
    del eg
    gc.collect()
    self.assertEqual(elt.element_geometry, eg_ref)
    del eg_ref
    gc.collect()
    # Check the weak_ptr does not reference anymore the deleted object
    self.assertEqual(elt.element_geometry, None)
    # Check None assign to weak_ptr
    elt.element_geometry = element_geometry_args([v, v_2])
    elt.element_geometry = None

    ir = impulse_response_args(42, np.nan, "sec", [3.14, -42])

    # Reference is possible for element_geometry since it's a weak_ptr
    # Check assignment
    elt.impulse_response = ir
    self.assertEqual(elt.impulse_response, impulse_response_args(42, np.nan, "sec", [3.14, -42]))
    ir.sampling_frequency.value = 123
    self.assertEqual(elt.impulse_response, impulse_response_args(123, np.nan, "sec", [3.14, -42]))
    ir_ref = elt.impulse_response
    ir_ref.sampling_frequency.value = np.nan
    self.assertEqual(elt.impulse_response, ir)
    self.assertEqual(elt.impulse_response, ir_ref)
    del ir
    gc.collect()
    self.assertEqual(elt.impulse_response, ir_ref)
    del ir_ref
    gc.collect()
    # Check the weak_ptr does not reference anymore the deleted object
    self.assertEqual(elt.impulse_response, None)

    print("--Test %s END--" % testName)
