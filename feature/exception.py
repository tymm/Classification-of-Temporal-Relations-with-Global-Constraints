class FailedProcessingFeature(Exception):
    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return repr("Failed processing feature: %s. Therefore skipping this relation." % self.feature)
