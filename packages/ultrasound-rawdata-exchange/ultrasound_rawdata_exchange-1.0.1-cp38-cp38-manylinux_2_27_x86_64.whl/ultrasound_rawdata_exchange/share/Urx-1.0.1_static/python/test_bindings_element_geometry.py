def test_element_geometry(
    self,
    vector3d_constructor,
    vector3d_args,
    element_geometry_constructor,
    element_geometry_copy,
    element_geometry_args,
    vec_vector3d_args,
):
    testName = "ElementGeometry binding"
    print("\n--Test %s BEGIN--" % testName)

    eg = element_geometry_constructor()
    eg_2 = element_geometry_constructor()

    v = vector3d_constructor()
    v_2 = vector3d_args(1, 2, 3)
    v_3 = vector3d_args(4, 5, 6)

    self.assertEqual(len(eg.perimeter), 0)
    self.assertEqual(eg, eg_2)

    # Possible to affect a list to perimeter
    eg.perimeter = [v, v_2]
    self.assertNotEqual(eg, eg_2)

    # Possible to create ElementGeometry from urx.VecVector3D
    vec_v = vec_vector3d_args([v, v_2])
    eg_2 = element_geometry_copy(vec_v)
    self.assertEqual(eg, eg_2)

    # Possible to affect a urx.VecVector3D to perimeter
    eg.perimeter = vec_vector3d_args([v_2, v])
    self.assertNotEqual(eg, eg_2)

    # Possible to create ElementGeometry from urx.VecVector3D
    eg = element_geometry_args([v, v_2])
    self.assertEqual(eg, eg_2)

    # Possible to create ElementGeometry from urx.VecVector3D
    eg = element_geometry_copy(eg_2)
    self.assertEqual(eg, eg_2)

    eg.perimeter[0] = v_3
    self.assertEqual(eg.perimeter[0], v_3)
    self.assertEqual(eg, element_geometry_args([v_3, v_2]))
    eg.perimeter.append(v_3)
    self.assertEqual(eg, element_geometry_args([v_3, v_2, v_3]))

    eg_ref = eg
    eg_3 = element_geometry_args(eg.perimeter)
    self.assertEqual(eg, eg_ref)
    self.assertEqual(eg, eg_3)

    # It is possible to get reference from an element of a C++ vector
    v_4 = eg.perimeter[0]
    eg.perimeter[0].x = 951
    # v_4 is modified since it references the first element from eg.perimeter
    self.assertEqual(eg.perimeter[0], v_4)

    # v_3 has been used to compose eg.perimeter, however it has been copied when passed to eg.perimeter. It is not affected by modification made to eg.perimeter[0]
    self.assertNotEqual(eg.perimeter[0], v_3)

    # Since v_4 references the first element of eg.perimeter, if v_4 is modified so is eg.perimeter[0]
    v_4.y = 753
    self.assertEqual(eg.perimeter[0], v_4)

    # eg_ref is a reference of eg, while eg_3 is a completly different python object even if it has been created from eg.perimeter. Thus eg_3 has not been impacted by the modifications made to eg
    self.assertEqual(eg, eg_ref)
    self.assertNotEqual(eg, eg_3)

    print("--Test %s END--" % testName)
