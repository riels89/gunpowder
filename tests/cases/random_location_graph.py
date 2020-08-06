from .provider_test import ProviderTest
from gunpowder import (
    BatchProvider,
    Graph,
    Node,
    GraphSpec,
    GraphKey,
    GraphKeys,
    Roi,
    Batch,
    BatchRequest,
    RandomLocation,
    build,
)
import numpy as np
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestSourceRandomLocation(BatchProvider):
    def __init__(self):

        self.graph = Graph(
            [
                Node(id=1, location=np.array([1, 1, 1])),
                Node(id=2, location=np.array([500, 500, 500])),
                Node(id=3, location=np.array([550, 550, 550])),
            ],
            [],
            GraphSpec(roi=Roi((0, 0, 0), (1000, 1000, 1000))),
        )

    def setup(self):

        self.provides(GraphKeys.TEST_GRAPH, self.graph.spec)

    def provide(self, request):

        batch = Batch()

        roi = request[GraphKeys.TEST_GRAPH].roi
        batch[GraphKeys.TEST_GRAPH] = self.graph.crop(roi).trim(roi)

        return batch


class TestRandomLocationGraph(ProviderTest):

    def test_dim_size_1(self):

        GraphKey("TEST_GRAPH")

        pipeline = TestSourceRandomLocation() + RandomLocation(
            ensure_nonempty=GraphKeys.TEST_GRAPH
        )

        # count the number of times we get each node
        histogram = {}

        with build(pipeline):

            for i in range(5000):
                batch = pipeline.request_batch(
                    BatchRequest(
                        {
                            GraphKeys.TEST_GRAPH: GraphSpec(
                                roi=Roi((0, 0, 0), (1, 100, 100))
                            )
                        }
                    )
                )

                nodes = list(batch[GraphKeys.TEST_GRAPH].nodes)
                node_ids = [v.id for v in nodes]

                self.assertTrue(len(nodes) > 0)
                self.assertTrue(
                    (1 in node_ids) != (2 in node_ids or 3 in node_ids),
                    node_ids,
                )

                for node in batch[GraphKeys.TEST_GRAPH].nodes:
                    if node.id not in histogram:
                        histogram[node.id] = 1
                    else:
                        histogram[node.id] += 1

        total = sum(histogram.values())
        for k, v in histogram.items():
            histogram[k] = float(v) / total

        # we should get roughly the same count for each point
        for i in histogram.keys():
            for j in histogram.keys():
                self.assertAlmostEqual(histogram[i], histogram[j], 1)

    def test_req_full_roi(self):

        GraphKey("TEST_GRAPH")

        pipeline = TestSourceRandomLocation() + RandomLocation(
            ensure_nonempty=GraphKeys.TEST_GRAPH
        )

        # count the number of times we get each node
        histogram = {}

        with build(pipeline):

            for i in range(5000):
                batch = pipeline.request_batch(
                    BatchRequest(
                        {
                            GraphKeys.TEST_GRAPH: GraphSpec(
                                roi=Roi((0, 0, 0), (1000, 1000, 1000))
                            )
                        }
                    )
                )

                nodes = list(batch[GraphKeys.TEST_GRAPH].nodes)
                node_ids = [v.id for v in nodes]

                self.assertTrue(len(nodes) > 0)
                self.assertTrue(
                    len(node_ids) == 3,
                    node_ids,
                )

                for node in batch[GraphKeys.TEST_GRAPH].nodes:
                    if node.id not in histogram:
                        histogram[node.id] = 1
                    else:
                        histogram[node.id] += 1

        total = sum(histogram.values())
        for k, v in histogram.items():
            histogram[k] = float(v) / total

        # we should get roughly the same count for each point
        for i in histogram.keys():
            for j in histogram.keys():
                self.assertAlmostEqual(histogram[i], histogram[j], 1)

    def test_iso_roi(self):

        GraphKey("TEST_GRAPH")

        pipeline = TestSourceRandomLocation() + RandomLocation(
            ensure_nonempty=GraphKeys.TEST_GRAPH
        )

        # count the number of times we get each node
        histogram = {}

        with build(pipeline):

            for i in range(5000):
                batch = pipeline.request_batch(
                    BatchRequest(
                        {
                            GraphKeys.TEST_GRAPH: GraphSpec(
                                roi=Roi((0, 0, 0), (100, 100, 100))
                            )
                        }
                    )
                )

                nodes = list(batch[GraphKeys.TEST_GRAPH].nodes)
                node_ids = [v.id for v in nodes]

                self.assertTrue(len(nodes) > 0)
                self.assertTrue(
                    (1 in node_ids) != (2 in node_ids or 3 in node_ids),
                    node_ids,
                )

                for node in batch[GraphKeys.TEST_GRAPH].nodes:
                    if node.id not in histogram:
                        histogram[node.id] = 1
                    else:
                        histogram[node.id] += 1

        total = sum(histogram.values())
        for k, v in histogram.items():
            histogram[k] = float(v) / total

        # we should get roughly the same count for each point
        for i in histogram.keys():
            for j in histogram.keys():
                self.assertAlmostEqual(histogram[i], histogram[j], 1)
