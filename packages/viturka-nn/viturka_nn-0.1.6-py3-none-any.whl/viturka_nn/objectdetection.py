import torch
from torch.utils.data import DataLoader, Dataset
from torchvision.models.detection import ssdlite320_mobilenet_v3_large
from torch import nn
import torchvision.transforms as T
from PIL import Image
import os
from pycocotools.coco import COCO
import requests


class ObjectDetection:
    def __init__(self, num_classes=6, pretrained=True, device="cuda"):
        self.model = ssdlite320_mobilenet_v3_large(pretrained=pretrained)

        # Change classification head for the number of classes
        if num_classes != 91:
            self.model.head.classification_head.num_classes = num_classes

        # Replace BatchNorm with GroupNorm
        self.model = self._replace_batchnorm_with_groupnorm(self.model)

        self.device = device
        self.model.to(self.device)

    def _replace_batchnorm_with_groupnorm(self, model):
        for name, module in model.named_modules():
            if isinstance(module, nn.BatchNorm2d):
                num_features = module.num_features
                setattr(
                    model, name,
                    nn.GroupNorm(num_groups=4, num_channels=num_features)
                )
        return model

    def _default_transforms(self):
        return T.Compose([
            T.Resize((320, 320)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def load_data(self, images_dir, annotation_file, batch_size=4, transforms=None):
        if transforms is None:
            transforms = self._default_transforms()

        # Initialize dataset and dataloader
        dataset = CustomDataset(root_dir=images_dir, annotation_file=annotation_file, transforms=transforms)
        self.dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=lambda x: tuple(zip(*x)))
        return self.dataloader

    def train(self, num_epochs=10, lr=0.005):
        # Set up optimizer
        optimizer = torch.optim.SGD(self.model.parameters(), lr=lr, momentum=0.9, weight_decay=0.0005)

        # Training loop
        for epoch in range(num_epochs):
            self.model.train()
            total_loss = 0.0

            for images, targets in self.dataloader:
                images = [img.to(self.device) for img in images]
                targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

                optimizer.zero_grad()
                loss_dict = self.model(images, targets)
                loss = sum(loss for loss in loss_dict.values())
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {total_loss / len(self.dataloader):.4f}")

    def evaluate(self):
        self.model.eval()
        metrics = []
        with torch.no_grad():
            for images, targets in self.dataloader:
                images = [img.to(self.device) for img in images]
                preds = self.model(images)
                # Placeholder metrics calculation (e.g., IoU can be added here)
                metrics.append(self._calculate_metrics(preds, targets))
        return metrics

    def _calculate_metrics(self, preds, targets):
        # Implement detailed evaluation metrics here
        return {'iou': 0.75}  # Placeholder


class CustomDataset(Dataset):
    def __init__(self, root_dir, annotation_file, transforms=None):
        self.root_dir = root_dir
        self.coco = COCO(annotation_file)
        self.transforms = transforms
        self.ids = list(self.coco.imgs.keys())

    def __getitem__(self, index):
        img_id = self.ids[index]
        annotation_ids = self.coco.getAnnIds(imgIds=img_id)
        annotations = self.coco.loadAnns(annotation_ids)

        boxes = [ann['bbox'] for ann in annotations]
        labels = [ann['category_id'] for ann in annotations]
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        boxes[:, 2:] += boxes[:, :2]

        img_path = os.path.join(self.root_dir, self.coco.imgs[img_id]['file_name'])
        image = Image.open(img_path).convert("RGB")
        target = {'boxes': boxes, 'labels': torch.tensor(labels, dtype=torch.int64)}

        if self.transforms:
            image = self.transforms(image)

        return image, target

    def __len__(self):
        return len(self.ids)
