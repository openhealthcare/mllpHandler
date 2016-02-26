from unittest import TestCase
import hl7

from gloss.ohc_receiver import OhcReceiver
from gloss.process_message import MSH
from test_messages import PATIENT_UPDATE, read_message
from txHL7.receiver import HL7MessageContainer

class TestOhcReceiverTestCase(TestCase):
    def test_ack_message(self):
        container = HL7MessageContainer(PATIENT_UPDATE.replace("\n", "\r"))
        ohc_receiver = OhcReceiver()
        ack = ohc_receiver.handleMessage(container).result
        msh = MSH(hl7.parse(ack).segment("MSH"))
        self.assertEqual(msh.sending_application, "ELCID")
        self.assertEqual(msh.sending_facility, "UCLH")