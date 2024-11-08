from time import perf_counter


def test_dataset(
    self,
    dataset_constructor,
    dataset_copy,
    dataset_constructor_args,
    acq_constructor,
    version_copy,
):
    testName = "Dataset binding"
    print("\n--Test %s BEGIN--" % testName)

    # Check default CTOR
    dataset = dataset_constructor()
    self.assertEqual(dataset.acquisition, acq_constructor())
    self.assertEqual(dataset.version, version_copy())

    acq = acq_constructor()
    acq.description = "Hello"

    v = version_copy()
    v.major = 42

    # Check copy CTOR and referencing object
    dataset_2 = dataset_copy(dataset)
    self.assertEqual(dataset, dataset_2)
    dataset_2.acquisition = acq
    self.assertNotEqual(dataset, dataset_2)
    dataset_ref = dataset
    dataset_ref.acquisition = acq
    self.assertEqual(dataset, dataset_ref)

    # Check CTOR with all parameters
    dataset = dataset_constructor_args(acq, v)
    self.assertEqual(dataset.acquisition, acq)
    self.assertEqual(dataset.version, v)
    dataset_2 = dataset_copy(dataset)

    # Reference is possible for acquisition (Acquisition)
    self.assertEqual(dataset.acquisition, acq)
    acq_ref = dataset.acquisition
    acq_ref.description = "World"
    self.assertEqual(dataset.acquisition, acq_ref)
    self.assertNotEqual(dataset, dataset_2)
    # Check assignment
    dataset.acquisition = acq
    self.assertEqual(dataset.acquisition, acq_ref)
    self.assertEqual(dataset.acquisition, acq)
    self.assertEqual(dataset, dataset_2)

    # Reference is possible for version (Version)
    self.assertEqual(dataset.version, v)
    v_ref = dataset.version
    v_ref.major = 24
    self.assertEqual(dataset.version, v_ref)
    self.assertNotEqual(dataset, dataset_2)
    # Check assignment
    dataset.version = v
    self.assertEqual(dataset.version, v_ref)
    self.assertEqual(dataset.version, v)
    self.assertEqual(dataset, dataset_2)

    print("--Test %s END--" % testName)
