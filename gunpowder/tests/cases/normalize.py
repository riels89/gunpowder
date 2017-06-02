from .provider_test import ProviderTest
from gunpowder import *

class TestNormalize(ProviderTest):

    def test_output(self):

        pipeline = self.test_source + Normalize()

        with build(pipeline):
            batch = pipeline.request_batch(self.test_request)

            raw = batch.volumes[VolumeType.RAW]
            self.assertTrue(raw.data.min() >= 0)
            self.assertTrue(raw.data.max() <= 1)
