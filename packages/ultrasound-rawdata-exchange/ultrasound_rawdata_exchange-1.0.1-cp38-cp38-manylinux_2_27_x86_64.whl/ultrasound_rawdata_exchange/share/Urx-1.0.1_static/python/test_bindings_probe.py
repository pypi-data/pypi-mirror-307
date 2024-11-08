import numpy as np
import gc


def test_probe(
    self,
    vector3d_constructor,
    vector3d_args,
    probe_constructor,
    probe_copy,
    probe_args,
    transform_constructor,
    transform_args,
    element_geometry_args,
    impulse_response_constructor,
    impulse_response_args,
    vec_element_geometry_ptr_constructor,
    vec_element_geometry_ptr_args,
    vec_impulse_response_ptr_constructor,
    vec_impulse_response_ptr_args,
    element_constructor,
    element_args,
    vec_element_constructor,
    vec_element_args,
    enum_probe,
):
    testName = "Probe binding"
    print("\n--Test %s BEGIN--" % testName)

    v = vector3d_constructor()
    v_2 = vector3d_args(1, 2, 3)
    v_3 = vector3d_args(4, 5, 6)

    # Check default CTOR
    p = probe_constructor()
    self.assertEqual(p.description, "")
    self.assertEqual(p.type, enum_probe().UNDEFINED)
    self.assertEqual(p.transform, transform_constructor())
    self.assertEqual(p.element_geometries, vec_element_geometry_ptr_constructor())
    self.assertEqual(p.impulse_responses, vec_impulse_response_ptr_constructor())
    self.assertEqual(p.elements, vec_element_constructor())

    t = transform_constructor()
    t_2 = transform_args(v_2, v_2)

    # Check copy CTOR and referencing object
    p_2 = probe_copy(p)
    self.assertEqual(p, p_2)
    p_2.transform = t_2
    self.assertNotEqual(p, p_2)
    p_ref = p
    p_ref.transform = t_2
    self.assertEqual(p, p_ref)

    eg = element_geometry_args([v, v])
    eg_2 = element_geometry_args([v_2, v_2])
    eg_3 = element_geometry_args([v_3, v_3])

    ir = impulse_response_constructor()
    ir_2 = impulse_response_args(42, np.nan, "s", [3.14, -42])
    ir_3 = impulse_response_args(123, 4.56, "ms", [1, 2, 3])

    elt = element_constructor()
    elt_2 = element_args(t_2, eg_2, ir_2)

    # Check CTOR with all parameters
    p_rca = probe_args(
        "rca probe",
        enum_probe().RCA,
        t,
        vec_element_geometry_ptr_args([eg, eg_2]),
        vec_impulse_response_ptr_args([ir, ir_2]),
        vec_element_args([elt, elt_2]),
    )
    p_rca = probe_args("rca probe", enum_probe().RCA, t, [eg, eg_2], [ir, ir_2], [elt, elt_2])

    # Instantiate second object to test == assertion
    p_rca_bis = probe_copy(p_rca)

    # element_geometries is a pointer vector, thus all modifications are shared
    self.assertEqual(p_rca.element_geometries[1], eg_2)
    self.assertEqual(p_rca.elements[1].element_geometry, eg_2)
    p_rca.element_geometries[1].perimeter[0] = v_3
    self.assertEqual(p_rca, p_rca_bis)
    self.assertEqual(p_rca.element_geometries[1], eg_2)
    self.assertEqual(p_rca.elements[1].element_geometry, eg_2)
    self.assertEqual(p_rca_bis.element_geometries[1], eg_2)
    self.assertEqual(p_rca_bis.elements[1].element_geometry, eg_2)

    # Reference is possible for shared pointers vector
    self.assertEqual(p_rca.element_geometries, [eg, eg_2])
    element_geometries_ref = p_rca.element_geometries
    element_geometries_ref[0] = eg_3
    self.assertEqual(p_rca.element_geometries, element_geometries_ref)
    self.assertNotEqual(p_rca, p_rca_bis)
    # Check assignment
    p_rca.element_geometries = [eg, eg_2]
    self.assertEqual(p_rca.element_geometries, element_geometries_ref)
    self.assertEqual(p_rca.element_geometries, [eg, eg_2])
    self.assertEqual(p_rca, p_rca_bis)

    # impulse_responses is a pointer vector, thus all modifications are shared
    p_rca.impulse_responses[1].sampling_frequency.value = 789.123
    self.assertEqual(p_rca, p_rca_bis)
    self.assertEqual(p_rca.impulse_responses[1], ir_2)
    self.assertEqual(p_rca_bis.impulse_responses[1], ir_2)

    # Reference is possible for shared pointers vector
    self.assertEqual(p_rca.impulse_responses, [ir, ir_2])
    impulse_responses_ref = p_rca.impulse_responses
    impulse_responses_ref[0] = ir_3
    self.assertEqual(p_rca.impulse_responses, impulse_responses_ref)
    self.assertNotEqual(p_rca, p_rca_bis)
    # Check assignment
    p_rca.impulse_responses = [ir, ir_2]
    self.assertEqual(p_rca.impulse_responses, impulse_responses_ref)
    self.assertEqual(p_rca.impulse_responses, [ir, ir_2])
    self.assertEqual(p_rca, p_rca_bis)

    # deleting the local variable does not impact the shared pointers vectors
    del eg_2
    del ir_2
    gc.collect()
    self.assertEqual(len(p_rca.element_geometries), 2)
    self.assertEqual(len(p_rca_bis.element_geometries), 2)
    self.assertEqual(len(p_rca.impulse_responses), 2)
    self.assertEqual(len(p_rca_bis.impulse_responses), 2)

    # deleting the pointers inside the vectors to check resize
    del p_rca.element_geometries[1]
    del p_rca_bis.element_geometries[1]
    del p_rca.impulse_responses[1]
    del p_rca_bis.impulse_responses[1]
    gc.collect()
    self.assertEqual(len(p_rca.element_geometries), 1)
    self.assertEqual(len(p_rca_bis.element_geometries), 1)
    self.assertEqual(len(p_rca.impulse_responses), 1)
    self.assertEqual(len(p_rca_bis.impulse_responses), 1)
    self.assertEqual(p_rca.elements[1].element_geometry, None)
    self.assertEqual(p_rca_bis.elements[1].element_geometry, None)
    self.assertEqual(p_rca.elements[1].impulse_response, None)
    self.assertEqual(p_rca_bis.elements[1].impulse_response, None)

    # Reference is not possible for enum
    self.assertEqual(p_rca.type, enum_probe().RCA)
    type_2 = p_rca.type
    type_2 = enum_probe().LINEAR
    self.assertNotEqual(p_rca.type, type_2)
    self.assertEqual(p_rca, p_rca_bis)
    # Check assignment
    p_rca.type = enum_probe().RCA
    self.assertEqual(p_rca.type, enum_probe().RCA)
    self.assertEqual(p_rca, p_rca_bis)

    # Reference is not possible for string
    self.assertEqual(p_rca.description, "rca probe")
    description_2 = p_rca.description
    description_2 = "Hello"
    self.assertNotEqual(p_rca.description, description_2)
    self.assertEqual(p_rca, p_rca_bis)
    # Check assignment
    p_rca.description = "rca probe"
    self.assertEqual(p_rca.description, "rca probe")
    self.assertEqual(p_rca, p_rca_bis)

    print("--Test %s END--" % testName)
