class Validator:
    def __init__(self, context):
        self.context = context

    def validate(self, manifest_content):
        required_fields = []