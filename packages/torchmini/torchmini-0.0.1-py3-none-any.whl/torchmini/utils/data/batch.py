class Batch:
    def __init__(self, examples):
        self.inputs, self.labels = zip(*examples)
    
    def __len__(self):
        return len(self.inputs)
    
    def __getitem__(self, item):
        return self.inputs[item], self.labels[item]  

