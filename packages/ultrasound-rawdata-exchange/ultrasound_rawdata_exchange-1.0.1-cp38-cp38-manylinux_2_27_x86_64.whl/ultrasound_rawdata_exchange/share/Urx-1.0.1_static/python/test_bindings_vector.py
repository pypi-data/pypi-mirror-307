def test_vector2d(
    self,
    vector2d_constructor,
    vector2d_copy,
    vector2d_args,
):
    testName = "Vector2D binding"
    print("\n--Test %s BEGIN--" % testName)

    # Check default CTOR
    v = vector2d_constructor()
    v_2 = vector2d_args(1, 2)
    self.assertEqual(v.x, 0)
    self.assertEqual(v.y, 0)

    # Check copy CTOR and referencing object
    v_2 = vector2d_copy(v)
    self.assertEqual(v, v_2)
    v_2.x = 42
    self.assertNotEqual(v, v_2)
    v_ref = v
    v_ref.x = 42
    self.assertEqual(v, v_ref)

    # Check CTOR with all parameters
    v = vector2d_args(1, 2)
    self.assertEqual(v.x, 1)
    self.assertEqual(v.y, 2)

    print("--Test %s END--" % testName)


def test_vector3d(
    self,
    vector3d_constructor,
    vector3d_copy,
    vector3d_args,
):
    testName = "Vector3D binding"
    print("\n--Test %s BEGIN--" % testName)

    # Check default CTOR
    v = vector3d_constructor()
    self.assertEqual(v.x, 0)
    self.assertEqual(v.y, 0)
    self.assertEqual(v.z, 0)

    # Check copy CTOR and referencing object
    v_2 = vector3d_copy(v)
    self.assertEqual(v, v_2)
    v_2.x = 42
    self.assertNotEqual(v, v_2)
    v_ref = v
    v_ref.x = 42
    self.assertEqual(v, v_ref)

    # Check CTOR with all parameters
    v = vector3d_args(1, 2, 3)
    self.assertEqual(v.x, 1)
    self.assertEqual(v.y, 2)
    self.assertEqual(v.z, 3)

    print("--Test %s END--" % testName)
