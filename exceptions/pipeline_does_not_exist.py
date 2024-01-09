class PipelineDoesNotExist(Exception):
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        super().__init__(f'Pipeline does not exist with name {self.pipeline_name}')
