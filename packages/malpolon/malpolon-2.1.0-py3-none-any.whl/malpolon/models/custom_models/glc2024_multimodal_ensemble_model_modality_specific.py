"""This module provides a Multimodal Ensemble model for GeoLifeCLEF2024 data.

Author: Lukas Picek <lukas.picek@inria.fr>
        Theo Larcher <theo.larcher@inria.fr>

License: GPLv3
Python version: 3.10.6
"""
from torch import nn
from torchvision import models


class MultimodalEnsemble(nn.Module):
    """Multimodal ensemble model processing Sentinel-2A, Landsat & Bioclimatic data.

    Inherits torch nn.Module.
    """
    def __init__(self,
                 num_classes: int = 11255,
                 pretrained: bool = False,
                 modality: str = None,
                 **kwargs):
        """Class constructor.

        Parameters
        ----------
        num_classes : int, optional
            numbre of classes, by default 11255
        pretrained : bool, optional
            if True, downloads the model's weights from our remote
            storage platform, by default False
        """
        super().__init__(**kwargs)
        self.pretrained = pretrained
        self.modality = modality
        self.landsat_model = models.resnet18(weights=None)
        self.landsat_norm = nn.LayerNorm([6, 4, 21])
        # Modify the first convolutional layer to accept 6 channels instead of 3
        self.landsat_model.conv1 = nn.Conv2d(6, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.landsat_model.maxpool = nn.Identity()

        self.bioclim_model = models.resnet18(weights=None)
        self.bioclim_norm = nn.LayerNorm([4, 19, 12])
        # Modify the first convolutional layer to accept 4 channels instead of 3
        self.bioclim_model.conv1 = nn.Conv2d(4, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bioclim_model.maxpool = nn.Identity()

        self.sentinel_model = models.swin_t(weights="IMAGENET1K_V1")
        # Modify the first layer to accept 4 channels instead of 3
        self.sentinel_model.features[0][0] = nn.Conv2d(4, 96, kernel_size=(4, 4), stride=(4, 4))
        self.sentinel_model.head = nn.Identity()

        self.ln1 = nn.LayerNorm(1000)
        self.ln2 = nn.LayerNorm(1000)
        self.fc1 = nn.Linear(1000, 4096)
        self.fc2 = nn.Linear(768, 4096)
        self.fc3 = nn.Linear(4096, num_classes)

        self.dropout = nn.Dropout(p=0.1)

    def forward(self, x, y, z):  # noqa: D102 pylint: disable=C0116
        if self.modality == 'landsat':
            x = self.landsat_norm(x)
            x = self.landsat_model(x)
            x = self.ln1(x)
            x = self.fc1(x)
        elif self.modality == 'bioclim':
            x = self.bioclim_norm(y)
            x = self.bioclim_model(x)
            x = self.ln2(x)
            x = self.fc1(x)
        elif self.modality == 'sentinel':
            x = self.sentinel_model(z)
            x = self.fc2(x)

        x = self.dropout(x)
        out = self.fc3(x)
        return out
