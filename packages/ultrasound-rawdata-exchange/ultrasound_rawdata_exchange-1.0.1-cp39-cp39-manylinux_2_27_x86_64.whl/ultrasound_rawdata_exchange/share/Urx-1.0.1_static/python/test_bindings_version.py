def test_version(
    self,
    version_constructor,
    version_copy,
    version_args,
    default_major,
    default_minor,
    default_patch,
):
    testName = "Version binding"
    print("\n--Test %s BEGIN--" % testName)

    v = version_constructor()
    v_2 = version_constructor()

    self.assertEqual(v.major, default_major)
    self.assertEqual(v.minor, default_minor)
    self.assertEqual(v.patch, default_patch)
    self.assertEqual(v, v_2)

    v = version_args(1, 2, 3)
    self.assertNotEqual(v, v_2)
    v_2 = version_args(1, 2, 3)
    self.assertEqual(v, v_2)

    # Check copy CTOR and referencing object
    v_2 = version_copy(v)
    self.assertEqual(v, v_2)
    v_2.minor = 42
    self.assertNotEqual(v, v_2)
    v_ref = v
    v_ref.minor = 42
    self.assertEqual(v, v_ref)

    print("--Test %s END--" % testName)
