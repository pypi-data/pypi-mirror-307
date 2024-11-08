def test_event(
    self,
    event_constructor,
    event_copy,
    event_args,
    transmit_setup_constructor,
    transmit_setup_args,
    receive_setup_constructor,
    receive_setup_args,
    probe_constructor,
    wave_constructor,
    transform_constructor,
):
    testName = "Event"
    print("\n--Test %s binding BEGIN--" % testName)

    # Check default CTOR
    evt = event_constructor()
    self.assertEqual(evt.transmit_setup, transmit_setup_constructor())
    self.assertEqual(evt.receive_setup, receive_setup_constructor())

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

    # Check copy CTOR and referencing object
    evt_2 = event_copy(evt)
    self.assertEqual(evt, evt_2)
    evt_2.receive_setup = rs
    self.assertNotEqual(evt, evt_2)
    evt_ref = evt
    evt_ref.receive_setup = rs
    self.assertEqual(evt, evt_ref)

    # Check CTOR with all parameters
    evt = event_args(ts, rs)
    self.assertEqual(evt.transmit_setup, ts)
    self.assertEqual(evt.receive_setup, rs)
    evt_2 = event_copy(evt)

    # Reference is possible for transmit_setup (TransmitSetup)
    self.assertEqual(evt.transmit_setup, ts)
    ts_ref = evt.transmit_setup
    probe_2 = probe_constructor()
    probe_2.description = "rca"
    ts_ref.probe = probe_2
    self.assertEqual(evt.transmit_setup, ts_ref)
    self.assertNotEqual(evt, evt_2)
    # Check assignment
    evt.transmit_setup = ts
    self.assertEqual(evt.transmit_setup, ts_ref)
    self.assertEqual(evt.transmit_setup, ts)
    self.assertEqual(evt, evt_2)

    # Reference is possible for receive_setup (ReceiveSetup)
    self.assertEqual(evt.receive_setup, rs)
    rs_ref = evt.receive_setup
    rs_ref.probe = probe_2
    self.assertEqual(evt.receive_setup, rs_ref)
    self.assertNotEqual(evt, evt_2)
    # Check assignment
    evt.receive_setup = rs
    self.assertEqual(evt.receive_setup, rs_ref)
    self.assertEqual(evt.receive_setup, rs)
    self.assertEqual(evt, evt_2)

    print("--Test %s END--" % testName)
