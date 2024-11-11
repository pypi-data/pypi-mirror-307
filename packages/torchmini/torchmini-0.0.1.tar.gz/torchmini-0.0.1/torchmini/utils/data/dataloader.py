from .batch import Batch
import torchmini

class DataLoader:
    def __init__(self, dataset, batch_size, sampler=None):
        self.dataset = dataset
        self.batch_size = batch_size
        self.sampler = sampler

    # def __iter__(self):
    #     indices = list(iter(self.sampler)) if self.sampler else list(range(len(self.dataset)))
        
    #     for i in range(0, len(indices), self.batch_size):
    #         batch_indices = indices[i:i + self.batch_size]
    #         batch_data = [self.dataset[idx] for idx in batch_indices]
    #         batch = Batch(batch_data)  # Create a Batch object
    #         # Debugging: Print the structure of batch inputs and labels
    #         # print(f"Batch {i // self.batch_size + 1}: inputs - {batch.inputs}, labels - {batch.labels}")
    #         print(type(batch.inputs), type(batch.labels))
    #         print(len(batch.inputs), len(batch.labels))
    #         yield batch.inputs, batch.labels

    def __iter__(self):
        indices = list(iter(self.sampler)) if self.sampler else list(range(len(self.dataset)))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            batch_data = [self.dataset[idx][0] for idx in batch_indices]  # Extract images only for batch
            batch_labels = [self.dataset[idx][1] for idx in batch_indices]  # Extract labels for batch

            # print(type(batch_data), type(batch_labels))
            # print(len(batch_data), len(batch_labels))
            # print(type(batch_data[0]), type(batch_labels[0]))

            # Stack all images into a single tensor of shape (batch_size, 1, 28, 28)
            # print(batch_data[0])
            # print(type(batch_data[0]))
            batch_data = torchmini.stack(batch_data, axis=0)  # Use torchmini stack function if available
            batch_labels = torchmini.tensor.Tensor(batch_labels)  # Convert labels to a single tensor

            yield batch_data, batch_labels

    def __len__(self):
        return (len(self.sampler) if self.sampler else len(self.dataset)) // self.batch_size

